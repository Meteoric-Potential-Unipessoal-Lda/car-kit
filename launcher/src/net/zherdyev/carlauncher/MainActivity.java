/*
 * car-launcher — лёгкий рабочий стол для Android-магнитол (часть car-kit, GPL-3.0).
 * Плитки «Навигация / Музыка / Телефон / Радио / Все приложения», 6 избранных, часы и дата,
 * автозапуск навигации или музыки после включения и после сна. Без анимаций, обоев и виджетов —
 * чтобы на слабой магнитоле рабочий стол занимал десятки мегабайт, а не сотни.
 * Интерфейс собран в коде (без ресурсов), поэтому APK собирается одними aapt2 + javac + d8.
 */
package net.zherdyev.carlauncher;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.BroadcastReceiver;
import android.content.ComponentName;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.GradientDrawable;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.SystemClock;
import android.provider.Settings;
import android.util.LruCache;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.KeyEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.FrameLayout;
import android.widget.GridView;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextClock;
import android.widget.TextView;
import android.widget.Toast;

import java.text.Collator;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.regex.Pattern;

public class MainActivity extends Activity {

    static final String VERSION = "0.3";
    static final int BG = 0xFF0B1220, CARD = 0xFF172033, CARD_ON = 0xFF22304A, INK = 0xFFF3F5F8, MUTED = 0xFF98A2B3, ACCENT = 0xFF3B82F6;
    static final String[] SLOTS = {"nav", "music", "phone", "radio"};

    // Кого ставить на плитки по умолчанию: сначала точные пакеты, потом по шаблону имени
    static final String[][] KNOWN = {
        {"com.waze", "ru.yandex.yandexnavi", "ru.dublgis.dgismobile", "com.sygic.aura", "net.osmand.plus", "net.osmand", "app.organicmaps",
         "com.mapswithme.maps.pro", "com.navitel", "com.google.android.apps.maps", "ru.yandex.yandexmaps", "com.here.app.maps",
         "com.tomtom.gplay.navapp", "com.generalmagic.magicearth", "com.nng.igo.primong.igoworld"},
        {"com.spotify.music", "ru.yandex.music", "com.maxmpz.audioplayer", "com.google.android.apps.youtube.music", "com.deezer.android.app",
         "com.aspiro.tidal", "com.zvuk.music", "com.syu.music", "com.microntek.music", "com.tw.music", "com.android.music"},
        {"com.syu.bt", "com.qf.bluetooth", "com.microntek.bluetooth", "com.tw.bt", "com.hcn.bluetooth", "com.android.dialer", "com.google.android.dialer"},
        {"com.syu.radio", "com.syu.carradio", "com.microntek.radio", "com.tw.radio", "com.hcn.autoradio", "com.qf.radio", "com.android.fmradio"}
    };
    static final Pattern[] GUESS = {
        Pattern.compile("(?i)navi|maps|nav\\b|gps"),
        Pattern.compile("(?i)music|player|audio|mp3"),
        Pattern.compile("(?i)\\bbt\\b|bluetooth|phone|dialer|call|телефон"),
        Pattern.compile("(?i)radio|\\bfm\\b|радио")
    };

    static class App {
        String label; ComponentName cn;
        App(String l, ComponentName c) { label = l; cn = c; }
    }

    final Handler ui = new Handler(Looper.getMainLooper());
    final ExecutorService bg = Executors.newSingleThreadExecutor();
    final LruCache<String, Drawable> icons = new LruCache<>(80);
    final List<App> apps = new ArrayList<>();
    SharedPreferences prefs;
    LinearLayout tilesRow, favRow;
    FrameLayout drawer;
    GridView grid;
    BaseAdapter gridAdapter;
    String lang;

    // ------------------------------------------------------------------ тексты
    String t(String ru, String uk, String en) {
        if ("ru".equals(lang)) return ru;
        if ("uk".equals(lang)) return uk;
        return en;
    }
    String slotName(int i) {
        switch (i) {
            case 0: return t("Навигация", "Навігація", "Navigation");
            case 1: return t("Музыка", "Музика", "Music");
            case 2: return t("Телефон", "Телефон", "Phone");
            default: return t("Радио", "Радіо", "Radio");
        }
    }

    int dp(float v) { return (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, v, getResources().getDisplayMetrics()); }

    GradientDrawable round(int color, float r) {
        GradientDrawable g = new GradientDrawable();
        g.setColor(color); g.setCornerRadius(dp(r));
        return g;
    }

    // ------------------------------------------------------------------ жизненный цикл
    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        lang = Locale.getDefault().getLanguage();
        prefs = getSharedPreferences("car", MODE_PRIVATE);
        getWindow().getDecorView().setBackgroundColor(BG);
        setContentView(build());
        reloadApps();
        IntentFilter pf = new IntentFilter();
        pf.addAction(Intent.ACTION_PACKAGE_ADDED); pf.addAction(Intent.ACTION_PACKAGE_REMOVED); pf.addAction(Intent.ACTION_PACKAGE_CHANGED);
        pf.addDataScheme("package");
        registerReceiver(pkgReceiver, pf);
        registerReceiver(screenReceiver, new IntentFilter(Intent.ACTION_SCREEN_ON));
        checkBootAutostart();
    }

    @Override
    protected void onDestroy() {
        try { unregisterReceiver(pkgReceiver); } catch (Exception ignored) { }
        try { unregisterReceiver(screenReceiver); } catch (Exception ignored) { }
        bg.shutdownNow();
        super.onDestroy();
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        hideDrawer();   // кнопка «Домой» всегда возвращает на главный экран
    }

    @Override
    public void onBackPressed() {
        if (drawer.getVisibility() == View.VISIBLE) hideDrawer();   // рабочий стол не закрываем
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK) { onBackPressed(); return true; }
        return super.onKeyDown(keyCode, event);
    }

    final BroadcastReceiver pkgReceiver = new BroadcastReceiver() {
        @Override public void onReceive(Context c, Intent i) { reloadApps(); }
    };
    // После сна по ACC многие магнитолы только включают экран: тогда открываем выбранное приложение
    final BroadcastReceiver screenReceiver = new BroadcastReceiver() {
        @Override public void onReceive(Context c, Intent i) {
            if (!prefs.getBoolean("auto_wake", false)) return;
            final ComponentName cn = autoTarget();
            if (cn != null) ui.postDelayed(new Runnable() { public void run() { launch(cn, false); } }, 1500);
        }
    };

    // ------------------------------------------------------------------ автозапуск после загрузки
    void checkBootAutostart() {
        long bootAt = System.currentTimeMillis() - SystemClock.elapsedRealtime();
        long last = prefs.getLong("last_boot", 0);
        if (Math.abs(bootAt - last) < 120000) return;          // эта загрузка уже обработана
        prefs.edit().putLong("last_boot", bootAt).apply();
        if (SystemClock.elapsedRealtime() > 10 * 60 * 1000) return;   // рабочий стол перезапустился не после включения
        final ComponentName cn = autoTarget();
        if (cn != null) ui.postDelayed(new Runnable() { public void run() { launch(cn, false); } }, 2500);
    }

    ComponentName autoTarget() {
        String a = prefs.getString("auto_boot", "");
        if (a.length() == 0) return null;
        if (a.startsWith("slot:")) { int i = Integer.parseInt(a.substring(5)); return slotApp(i); }
        return ComponentName.unflattenFromString(a);
    }

    // ------------------------------------------------------------------ интерфейс
    View build() {
        FrameLayout root = new FrameLayout(this);
        LinearLayout main = new LinearLayout(this);
        main.setOrientation(LinearLayout.VERTICAL);
        main.setPadding(dp(24), dp(16), dp(24), dp(16));

        LinearLayout top = new LinearLayout(this);
        top.setOrientation(LinearLayout.HORIZONTAL);
        top.setGravity(Gravity.CENTER_VERTICAL);
        LinearLayout clockCol = new LinearLayout(this);
        clockCol.setOrientation(LinearLayout.VERTICAL);
        TextClock time = new TextClock(this);
        time.setFormat24Hour("HH:mm"); time.setFormat12Hour("h:mm");
        time.setTextColor(INK); time.setTextSize(TypedValue.COMPLEX_UNIT_SP, 56); time.setTypeface(Typeface.DEFAULT_BOLD);
        TextClock date = new TextClock(this);
        date.setFormat24Hour("EEEE, d MMMM"); date.setFormat12Hour("EEEE, d MMMM");
        date.setTextColor(MUTED); date.setTextSize(TypedValue.COMPLEX_UNIT_SP, 18);
        clockCol.addView(time); clockCol.addView(date);
        top.addView(clockCol, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1));
        TextView gear = new TextView(this);
        gear.setText("⚙"); gear.setTextColor(INK); gear.setTextSize(TypedValue.COMPLEX_UNIT_SP, 34);
        gear.setGravity(Gravity.CENTER); gear.setBackground(round(CARD, 16));
        gear.setContentDescription(t("Настройки рабочего стола", "Налаштування робочого столу", "Launcher settings"));
        gear.setOnClickListener(new View.OnClickListener() { public void onClick(View v) { showSettings(); } });
        top.addView(gear, new LinearLayout.LayoutParams(dp(72), dp(72)));
        main.addView(top);

        tilesRow = new LinearLayout(this);
        tilesRow.setOrientation(LinearLayout.HORIZONTAL);
        LinearLayout.LayoutParams tl = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0, 1);
        tl.topMargin = dp(16);
        main.addView(tilesRow, tl);

        favRow = new LinearLayout(this);
        favRow.setOrientation(LinearLayout.HORIZONTAL);
        LinearLayout.LayoutParams fl = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(104));
        fl.topMargin = dp(12);
        main.addView(favRow, fl);
        root.addView(main);

        // Все приложения — поверх главного экрана
        drawer = new FrameLayout(this);
        drawer.setBackgroundColor(BG);
        drawer.setVisibility(View.GONE);
        LinearLayout dcol = new LinearLayout(this);
        dcol.setOrientation(LinearLayout.VERTICAL);
        dcol.setPadding(dp(16), dp(12), dp(16), dp(12));
        LinearLayout dtop = new LinearLayout(this);
        dtop.setGravity(Gravity.CENTER_VERTICAL);
        TextView dtitle = new TextView(this);
        dtitle.setText(t("Все приложения", "Усі застосунки", "All apps"));
        dtitle.setTextColor(INK); dtitle.setTextSize(TypedValue.COMPLEX_UNIT_SP, 24); dtitle.setTypeface(Typeface.DEFAULT_BOLD);
        dtop.addView(dtitle, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1));
        TextView close = new TextView(this);
        close.setText("✕"); close.setTextColor(INK); close.setTextSize(TypedValue.COMPLEX_UNIT_SP, 28); close.setGravity(Gravity.CENTER);
        close.setBackground(round(CARD, 14));
        close.setOnClickListener(new View.OnClickListener() { public void onClick(View v) { hideDrawer(); } });
        dtop.addView(close, new LinearLayout.LayoutParams(dp(64), dp(64)));
        dcol.addView(dtop);
        grid = new GridView(this);
        grid.setNumColumns(GridView.AUTO_FIT);
        grid.setColumnWidth(dp(112));
        grid.setVerticalSpacing(dp(10)); grid.setHorizontalSpacing(dp(10));
        grid.setStretchMode(GridView.STRETCH_COLUMN_WIDTH);
        grid.setSelector(new GradientDrawable());
        gridAdapter = new BaseAdapter() {
            public int getCount() { return apps.size(); }
            public Object getItem(int p) { return apps.get(p); }
            public long getItemId(int p) { return p; }
            public View getView(int p, View v, ViewGroup parent) {
                App a = apps.get(p);
                LinearLayout cell = (v instanceof LinearLayout) ? (LinearLayout) v : appCell(false);
                bindCell(cell, a, a.label);
                return cell;
            }
        };
        grid.setAdapter(gridAdapter);
        grid.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            public void onItemClick(AdapterView<?> parent, View view, int p, long id) { launch(apps.get(p).cn, true); }
        });
        grid.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener() {
            public boolean onItemLongClick(AdapterView<?> parent, View view, int p, long id) { appInfo(apps.get(p).cn); return true; }
        });
        LinearLayout.LayoutParams gl = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0, 1);
        gl.topMargin = dp(12);
        dcol.addView(grid, gl);
        drawer.addView(dcol);
        root.addView(drawer);
        return root;
    }

    LinearLayout appCell(boolean big) {
        LinearLayout cell = new LinearLayout(this);
        cell.setOrientation(LinearLayout.VERTICAL);
        cell.setGravity(Gravity.CENTER);
        cell.setPadding(dp(8), dp(10), dp(8), dp(10));
        cell.setBackground(round(CARD, big ? 22 : 16));
        ImageView iv = new ImageView(this);
        iv.setScaleType(ImageView.ScaleType.FIT_CENTER);
        int s = dp(big ? 72 : 48);
        cell.addView(iv, new LinearLayout.LayoutParams(s, s));
        TextView tv = new TextView(this);
        tv.setTextColor(INK); tv.setGravity(Gravity.CENTER); tv.setMaxLines(big ? 1 : 2);
        tv.setTextSize(TypedValue.COMPLEX_UNIT_SP, big ? 20 : 13);
        if (big) tv.setTypeface(Typeface.DEFAULT_BOLD);
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        lp.topMargin = dp(6);
        cell.addView(tv, lp);
        if (big) {
            TextView sub = new TextView(this);
            sub.setTextColor(MUTED); sub.setGravity(Gravity.CENTER); sub.setMaxLines(1);
            sub.setTextSize(TypedValue.COMPLEX_UNIT_SP, 13);
            cell.addView(sub);
        }
        return cell;
    }

    void bindCell(LinearLayout cell, App a, String title) {
        final ImageView iv = (ImageView) cell.getChildAt(0);
        ((TextView) cell.getChildAt(1)).setText(title);
        if (cell.getChildCount() > 2) ((TextView) cell.getChildAt(2)).setText(a == null ? t("нажмите, чтобы выбрать", "натисніть, щоб вибрати", "tap to choose") : a.label);
        if (a == null) { iv.setImageDrawable(null); return; }
        final String key = a.cn.flattenToShortString();
        iv.setTag(key);
        Drawable d = icons.get(key);
        if (d != null) { iv.setImageDrawable(d); return; }
        iv.setImageDrawable(null);
        final ComponentName cn = a.cn;
        bg.execute(new Runnable() {
            public void run() {
                Drawable ic;
                try { ic = getPackageManager().getActivityIcon(cn); } catch (Exception e) { ic = null; }
                if (ic == null) return;
                icons.put(key, ic);
                final Drawable f = ic;
                ui.post(new Runnable() { public void run() { if (key.equals(iv.getTag())) iv.setImageDrawable(f); } });
            }
        });
    }

    void renderTiles() {
        tilesRow.removeAllViews();
        for (int i = 0; i < SLOTS.length; i++) {
            final int idx = i;
            LinearLayout cell = appCell(true);
            bindCell(cell, findApp(slotApp(i)), slotName(i));
            cell.setOnClickListener(new View.OnClickListener() { public void onClick(View v) {
                ComponentName cn = slotApp(idx);
                if (cn == null) pickApp(slotName(idx), "slot_" + SLOTS[idx]); else launch(cn, true);
            } });
            cell.setOnLongClickListener(new View.OnLongClickListener() { public boolean onLongClick(View v) { pickApp(slotName(idx), "slot_" + SLOTS[idx]); return true; } });
            addWeighted(tilesRow, cell, i > 0);
        }
        LinearLayout all = appCell(true);
        ((ImageView) all.getChildAt(0)).setImageDrawable(dots());
        ((TextView) all.getChildAt(1)).setText(t("Все", "Усі", "All apps"));
        ((TextView) all.getChildAt(2)).setText(apps.size() + "");
        all.setOnClickListener(new View.OnClickListener() { public void onClick(View v) { showDrawer(); } });
        addWeighted(tilesRow, all, true);

        favRow.removeAllViews();
        for (int i = 0; i < 6; i++) {
            final String key = "fav_" + i;
            final String title = t("Избранное", "Обране", "Favorite") + " " + (i + 1);
            App a = findApp(ComponentName.unflattenFromString(prefs.getString(key, "")));
            LinearLayout cell = appCell(false);
            if (a == null) { ((TextView) cell.getChildAt(1)).setText("+"); ((TextView) cell.getChildAt(1)).setTextSize(TypedValue.COMPLEX_UNIT_SP, 26); ((TextView) cell.getChildAt(1)).setTextColor(MUTED); }
            else bindCell(cell, a, a.label);
            final App fa = a;
            cell.setOnClickListener(new View.OnClickListener() { public void onClick(View v) { if (fa == null) pickApp(title, key); else launch(fa.cn, true); } });
            cell.setOnLongClickListener(new View.OnLongClickListener() { public boolean onLongClick(View v) { pickApp(title, key); return true; } });
            addWeighted(favRow, cell, i > 0);
        }
    }

    void addWeighted(LinearLayout row, View v, boolean gap) {
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.MATCH_PARENT, 1);
        if (gap) lp.leftMargin = dp(12);
        row.addView(v, lp);
    }

    Drawable dots() {
        GradientDrawable g = new GradientDrawable();
        g.setShape(GradientDrawable.OVAL); g.setColor(ACCENT); g.setSize(dp(56), dp(56));
        return g;
    }

    void showDrawer() { gridAdapter.notifyDataSetChanged(); drawer.setVisibility(View.VISIBLE); grid.setSelection(0); }
    void hideDrawer() { if (drawer != null) drawer.setVisibility(View.GONE); }

    // ------------------------------------------------------------------ приложения
    void reloadApps() {
        bg.execute(new Runnable() {
            public void run() {
                PackageManager pm = getPackageManager();
                Intent i = new Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER);
                List<ResolveInfo> ris = pm.queryIntentActivities(i, 0);
                final List<App> list = new ArrayList<>();
                for (ResolveInfo ri : ris) {
                    if (ri.activityInfo == null || getPackageName().equals(ri.activityInfo.packageName)) continue;
                    CharSequence l = ri.loadLabel(pm);
                    list.add(new App(l == null ? ri.activityInfo.packageName : l.toString(), new ComponentName(ri.activityInfo.packageName, ri.activityInfo.name)));
                }
                final Collator col = Collator.getInstance();
                Collections.sort(list, new Comparator<App>() { public int compare(App a, App b) { return col.compare(a.label, b.label); } });
                ui.post(new Runnable() {
                    public void run() {
                        apps.clear(); apps.addAll(list);
                        fillDefaults();
                        renderTiles();
                        gridAdapter.notifyDataSetChanged();
                    }
                });
            }
        });
    }

    App findApp(ComponentName cn) {
        if (cn == null) return null;
        for (App a : apps) if (a.cn.equals(cn)) return a;
        for (App a : apps) if (a.cn.getPackageName().equals(cn.getPackageName())) return a;   // активность переименовали при обновлении
        return null;
    }

    ComponentName slotApp(int i) {
        App a = findApp(ComponentName.unflattenFromString(prefs.getString("slot_" + SLOTS[i], "")));
        return a == null ? null : a.cn;
    }

    // Пустые плитки заполняем сами: известные пакеты, потом догадка по имени
    void fillDefaults() {
        SharedPreferences.Editor e = prefs.edit();
        boolean ch = false;
        for (int s = 0; s < SLOTS.length; s++) {
            if (prefs.getString("slot_" + SLOTS[s], "").length() > 0 && (slotApp(s) != null || "-".equals(prefs.getString("slot_" + SLOTS[s], "")))) continue;   // выбрано или нарочно очищено
            App pick = null;
            for (String pkg : KNOWN[s]) { for (App a : apps) if (a.cn.getPackageName().equals(pkg)) { pick = a; break; } if (pick != null) break; }
            if (pick == null) for (App a : apps) if (GUESS[s].matcher(a.cn.getPackageName() + " " + a.label).find()) { pick = a; break; }
            if (pick != null) { e.putString("slot_" + SLOTS[s], pick.cn.flattenToString()); ch = true; }
        }
        if (ch) e.apply();
    }

    void launch(ComponentName cn, boolean userAction) {
        if (cn == null) return;
        try {
            Intent i = new Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER).setComponent(cn)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_RESET_TASK_IF_NEEDED);
            startActivity(i);
            hideDrawer();
        } catch (Exception ex) {
            if (userAction) Toast.makeText(this, t("Не удалось открыть", "Не вдалося відкрити", "Couldn't open") + ": " + cn.getPackageName(), Toast.LENGTH_SHORT).show();
        }
    }

    void appInfo(ComponentName cn) {
        try { startActivity(new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:" + cn.getPackageName())).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)); }
        catch (Exception ignored) { }
    }

    // Выбор приложения для плитки / избранного / автозапуска
    void pickApp(String title, final String key) {
        final List<App> list = new ArrayList<>(apps);
        BaseAdapter ad = new BaseAdapter() {
            public int getCount() { return list.size() + 1; }
            public Object getItem(int p) { return p; }
            public long getItemId(int p) { return p; }
            public View getView(int p, View v, ViewGroup parent) {
                LinearLayout row = (v instanceof LinearLayout) ? (LinearLayout) v : listRow();
                if (p == 0) { ((ImageView) row.getChildAt(0)).setImageDrawable(null); ((TextView) row.getChildAt(1)).setText(t("— пусто —", "— порожньо —", "— empty —")); }
                else { App a = list.get(p - 1); ((TextView) row.getChildAt(1)).setText(a.label); bindIcon((ImageView) row.getChildAt(0), a); }
                return row;
            }
        };
        new AlertDialog.Builder(this).setTitle(title).setAdapter(ad, new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface d, int which) {
                prefs.edit().putString(key, which == 0 ? "-" : list.get(which - 1).cn.flattenToString()).apply();
                if (which == 0 && key.startsWith("auto")) prefs.edit().putString(key, "").apply();
                renderTiles();
            }
        }).show();
    }

    LinearLayout listRow() {
        LinearLayout row = new LinearLayout(this);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.setPadding(dp(16), dp(10), dp(16), dp(10));
        ImageView iv = new ImageView(this);
        row.addView(iv, new LinearLayout.LayoutParams(dp(40), dp(40)));
        TextView tv = new TextView(this);
        tv.setTextSize(TypedValue.COMPLEX_UNIT_SP, 18);
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        lp.leftMargin = dp(14);
        row.addView(tv, lp);
        return row;
    }

    void bindIcon(final ImageView iv, App a) {
        final String key = a.cn.flattenToShortString();
        iv.setTag(key);
        Drawable d = icons.get(key);
        if (d != null) { iv.setImageDrawable(d); return; }
        iv.setImageDrawable(null);
        final ComponentName cn = a.cn;
        bg.execute(new Runnable() {
            public void run() {
                Drawable ic;
                try { ic = getPackageManager().getActivityIcon(cn); } catch (Exception e) { return; }
                icons.put(key, ic);
                final Drawable f = ic;
                ui.post(new Runnable() { public void run() { if (key.equals(iv.getTag())) iv.setImageDrawable(f); } });
            }
        });
    }

    // ------------------------------------------------------------------ настройки
    void showSettings() {
        final String auto = prefs.getString("auto_boot", "");
        String autoName = t("ничего", "нічого", "nothing");
        if (auto.startsWith("slot:")) autoName = slotName(Integer.parseInt(auto.substring(5)));
        else if (auto.length() > 0) { App a = findApp(ComponentName.unflattenFromString(auto)); if (a != null) autoName = a.label; }
        final boolean wake = prefs.getBoolean("auto_wake", false);
        String[] items = {
            t("При включении открывать: ", "Після ввімкнення відкривати: ", "Open on power-on: ") + autoName,
            (wake ? "☑ " : "☐ ") + t("…и после сна (включился экран)", "…і після сну (увімкнувся екран)", "…and after sleep (screen on)"),
            t("Плитки и избранное: долгое нажатие — выбрать приложение", "Плитки й обране: довге натискання — вибрати застосунок", "Tiles and favorites: long press to choose an app"),
            t("Настройки Android", "Налаштування Android", "Android settings"),
            "car-launcher " + VERSION + " · car-kit · GPL-3.0"
        };
        new AlertDialog.Builder(this).setTitle(t("Рабочий стол", "Робочий стіл", "Launcher")).setItems(items, new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface d, int which) {
                if (which == 0) chooseAuto();
                else if (which == 1) prefs.edit().putBoolean("auto_wake", !wake).apply();
                else if (which == 3) { try { startActivity(new Intent(Settings.ACTION_SETTINGS).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)); } catch (Exception ignored) { } }
            }
        }).show();
    }

    void chooseAuto() {
        String[] items = { t("Ничего", "Нічого", "Nothing"), slotName(0), slotName(1), t("Другое приложение…", "Інший застосунок…", "Another app…") };
        new AlertDialog.Builder(this).setTitle(t("При включении открывать", "Після ввімкнення відкривати", "Open on power-on")).setItems(items, new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface d, int which) {
                if (which == 0) prefs.edit().putString("auto_boot", "").apply();
                else if (which == 1) prefs.edit().putString("auto_boot", "slot:0").apply();
                else if (which == 2) prefs.edit().putString("auto_boot", "slot:1").apply();
                else pickApp(t("При включении открывать", "Після ввімкнення відкривати", "Open on power-on"), "auto_boot");
            }
        }).show();
    }
}

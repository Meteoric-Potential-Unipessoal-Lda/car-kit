package net.zherdyev.carkit;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.text.InputType;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.ScrollView;
import android.widget.Spinner;
import android.widget.TextView;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.ConnectException;
import java.net.SocketTimeoutException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;

/** car-kit Mobile: телефон вместо ноутбука мастера. Экраны: подключение -> диагностика -> план -> применение -> откат. */
public class MainActivity extends Activity {
  static final int BG = 0xFF0F1418, CARD = 0xFF1A2229, TXT = 0xFFE8EEF2, MUTED = 0xFF98A6B3, ACC = 0xFF3DDC84, WARN = 0xFFFFB74D, BAD = 0xFFEF5350, OKC = 0xFF81C784;

  final Handler ui = new Handler(Looper.getMainLooper());
  SharedPreferences prefs;
  Lang L;
  Data data;
  AdbKey key;
  AdbConn conn;
  Engine eng;
  Engine.Journal journal;
  String lastAddr = "";
  volatile boolean busy;

  LinearLayout page;
  ScrollView scroll;
  LinearLayout logBox;
  ProgressBar bar;

  // ---------------------------------------------------------------- старт

  @Override
  protected void onCreate(Bundle b) {
    super.onCreate(b);
    prefs = getSharedPreferences("carkit", MODE_PRIVATE);
    getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
    if (Build.VERSION.SDK_INT >= 21) getWindow().setStatusBarColor(BG);
    scroll = new ScrollView(this);
    scroll.setBackgroundColor(BG);
    scroll.setFillViewport(true);
    page = new LinearLayout(this);
    page.setOrientation(LinearLayout.VERTICAL);
    int p = dp(16);
    page.setPadding(p, p, p, p);
    scroll.addView(page);
    setContentView(scroll);
    loadLang(prefs.getString("lang", Lang.pick(Locale.getDefault().getLanguage())));
    lastAddr = prefs.getString("addr", "");
    String auto = getIntent().getStringExtra("autotest");
    if (auto != null && isEmulator()) { autotest(auto); return; }
    showHome(null);
    new Thread(new Runnable() { public void run() { ensureKey(); } }).start();
  }

  Lang.Source assets() {
    return new Lang.Source() { public InputStream open(String name) throws IOException { return getAssets().open(name); } };
  }

  void loadLang(String code) {
    try {
      L = new Lang(code, assets());
      data = new Data(assets(), code);
    } catch (IOException e) { throw new RuntimeException(e); }
    prefs.edit().putString("lang", code).apply();
  }

  synchronized AdbKey ensureKey() {
    if (key == null) {
      try { key = AdbKey.loadOrCreate(new File(getFilesDir(), "adbkey")); }
      catch (Exception e) { postMsg(L.t("a015", e.toString()), BAD); }
    }
    return key;
  }

  File journalFile(String unit) {
    File d = new File(getFilesDir(), "journals");
    d.mkdirs();
    return new File(d, unit.replaceAll("[^A-Za-z0-9_.-]", "_") + ".tsv");
  }

  @Override
  public void onBackPressed() {
    if (busy) return;
    if (conn != null && eng != null) { showSummary(); return; }
    super.onBackPressed();
  }

  @Override
  protected void onDestroy() {
    if (conn != null) conn.close();
    super.onDestroy();
  }

  // ---------------------------------------------------------------- главный экран

  void showHome(final String msg) {
    clear();
    title(L.t("a000"));
    text(L.t("a001"), MUTED, 15);
    if (msg != null) text(msg, WARN, 15);
    final LinearLayout found = new LinearLayout(this);
    found.setOrientation(LinearLayout.VERTICAL);
    final TextView status = text("", MUTED, 14);
    button(L.t("a002"), true, new View.OnClickListener() { public void onClick(View v) { scan(found, status); } });
    page.addView(found);
    final EditText ip = new EditText(this);
    ip.setHint(L.t("a003"));
    ip.setText(lastAddr);
    ip.setTextColor(TXT);
    ip.setHintTextColor(MUTED);
    ip.setSingleLine(true);
    ip.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_URI);
    page.addView(ip, lp(-1, -2, 12));
    button(L.t("a004"), false, new View.OnClickListener() { public void onClick(View v) { connect(ip.getText().toString()); } });
    button(L.t("a005"), false, new View.OnClickListener() { public void onClick(View v) { showHelp(); } });
    space(12);
    langPicker();
    AdbKey k = key;
    if (k != null) text(L.t("a007", k.fingerprint()), MUTED, 12);
    text("car-kit Mobile " + Engine.VERSION + " · GPL-3.0 · github.com/Meteoric-Potential-Unipessoal-Lda/car-kit", MUTED, 11);
  }

  void langPicker() {
    LinearLayout row = new LinearLayout(this);
    row.setGravity(Gravity.CENTER_VERTICAL);
    TextView t = new TextView(this);
    t.setText(L.t("a006") + ": ");
    t.setTextColor(MUTED);
    row.addView(t);
    final Spinner sp = new Spinner(this);
    ArrayAdapter<String> ad = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, Lang.NAMES) {
      @Override public View getView(int pos, View cv, ViewGroup parent) { TextView v = (TextView) super.getView(pos, cv, parent); v.setTextColor(TXT); return v; }
    };
    ad.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
    sp.setAdapter(ad);
    int cur = 0;
    for (int i = 0; i < Lang.CODES.length; i++) if (Lang.CODES[i].equals(L.code)) cur = i;
    sp.setSelection(cur, false);
    sp.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
      public void onItemSelected(AdapterView<?> a, View v, int pos, long id) {
        if (!Lang.CODES[pos].equals(L.code)) { loadLang(Lang.CODES[pos]); showHome(null); }
      }
      public void onNothingSelected(AdapterView<?> a) {}
    });
    row.addView(sp);
    page.addView(row, lp(-1, -2, 4));
  }

  void scan(final LinearLayout found, final TextView status) {
    if (busy) return;
    busy = true;
    found.removeAllViews();
    new Thread(new Runnable() {
      public void run() {
        List<Scan.Net> nets = Scan.nets();
        final List<String> all = new ArrayList<String>();
        if (nets.isEmpty()) { setText(status, L.t("a063"), WARN); busy = false; return; }
        for (Scan.Net n : nets) {
          setText(status, L.t("a060", n.prefix + "0/24"), MUTED);
          all.addAll(Scan.find(n, 5555));
          if (!all.isEmpty()) break;
        }
        busy = false;
        ui.post(new Runnable() {
          public void run() {
            if (all.isEmpty()) { status.setText(L.t("a062")); status.setTextColor(WARN); return; }
            status.setText(L.t("a061", all.size()));
            status.setTextColor(OKC);
            for (final String ip : all) {
              Button bt = mkButton(ip + ":5555", true);
              bt.setOnClickListener(new View.OnClickListener() { public void onClick(View v) { connect(ip); } });
              found.addView(bt, lp(-1, -2, 6));
            }
            if (all.size() == 1) connect(all.get(0));
          }
        });
      }
    }).start();
  }

  void showHelp() {
    clear();
    title(L.t("a050"));
    for (String k : new String[] { "a051", "a052", "a053", "a054" }) text(L.t(k), TXT, 15);
    space(8);
    for (String k : new String[] { "k016", "k017", "k018", "k019" }) text(L.t(k).trim(), MUTED, 14);
    space(8);
    for (String k : new String[] { "a055", "a056", "k022", "k023", "k024" }) text(L.t(k).trim(), MUTED, 14);
    button(L.t("a071"), true, new View.OnClickListener() { public void onClick(View v) { showHome(null); } });
  }

  // ---------------------------------------------------------------- подключение и диагностика

  void connect(String addr) {
    if (busy) return;
    final String[] hp = Scan.parseAddr(addr);
    if (hp == null) { showHome(L.t("a015", addr)); return; }
    lastAddr = hp[0] + (hp[1].equals("5555") ? "" : ":" + hp[1]);
    prefs.edit().putString("addr", lastAddr).apply();
    busy = true;
    clear();
    title(L.t("a000"));
    startLog();
    postMsg(L.t("a010", hp[0] + ":" + hp[1]), MUTED);
    new Thread(new Runnable() {
      public void run() {
        try {
          if (conn != null) conn.close();
          conn = null;
          AdbKey k = ensureKey();
          if (k == null) { busy = false; return; }
          conn = AdbConn.connect(hp[0], Integer.parseInt(hp[1]), k, 60, new AdbConn.AuthListener() {
            public void onAllowNeeded() { postMsg(L.t("a011"), WARN); }
          });
          postMsg(L.t("a171", conn.addr), OKC);
          diagnose();
        } catch (AdbConn.TlsRequired e) { fail(L.t("a013"));
        } catch (AdbConn.NotAllowed e) { fail(L.t("a014"));
        } catch (ConnectException e) { fail(L.t("a012"));
        } catch (SocketTimeoutException e) { fail(L.t("a016", hp[0]));
        } catch (IOException e) { fail(L.t("a015", e.getMessage()));
        } catch (RuntimeException e) { fail(L.t("a015", e.toString())); }
      }
    }).start();
  }

  void fail(final String msg) {
    busy = false;
    if (conn != null) conn.close();
    conn = null;
    eng = null;
    ui.post(new Runnable() { public void run() { showHome(msg); } });
  }

  Engine.Log engineLog() {
    return new Engine.Log() {
      public void line(String t, int kind) { postMsg(t, kind == Engine.OK ? OKC : kind == Engine.WARN ? WARN : kind == Engine.BAD ? BAD : MUTED); }
      public void progress(final int done, final int total) { ui.post(new Runnable() { public void run() { if (bar != null) { bar.setMax(total); bar.setProgress(done); } } }); }
    };
  }

  /** В фоновом потоке. */
  void diagnose() throws IOException {
    postMsg(L.t("a024"), TXT);
    eng = new Engine(conn, data, L, engineLog());
    eng.diagnose();
    File jf = journalFile(eng.unitId);
    journal = jf.isFile() ? Engine.Journal.load(jf) : new Engine.Journal(jf);
    busy = false;
    ui.post(new Runnable() { public void run() { showSummary(); } });
  }

  void showSummary() {
    clear();
    final Engine e = eng;
    title(L.t("a026", (e.platName.length() > 0 ? e.platName + " · " : "") + e.model));
    text(e.chip + " · " + conn.addr, MUTED, 14);
    text(L.t("a027", e.P("ro.build.version.release"), e.sdk, e.before.memAvailMb, memTotalMb(), e.before.dataFreeMb), TXT, 14);
    LinearLayout c = card();
    if (e.obs.isEmpty()) cardText(c, L.t("a025"), OKC);
    for (String o : e.obs) cardText(c, "• " + o, TXT);
    for (String n : e.notes) cardText(c, "• " + n, MUTED);
    if (!e.diagOnly) button(L.t("a020"), true, new View.OnClickListener() { public void onClick(View v) { showPlan(); } });
    if (journal != null && !journal.entries.isEmpty())
      button(L.t("a022") + " — " + L.t("a160", journal.created, journal.entries.size()), false, new View.OnClickListener() { public void onClick(View v) { showRollback(); } });
    button(L.t("a021"), false, new View.OnClickListener() { public void onClick(View v) { share(); } });
    button(L.t("a023"), false, new View.OnClickListener() {
      public void onClick(View v) { if (conn != null) conn.close(); conn = null; eng = null; showHome(L.t("a161")); }
    });
  }

  long memTotalMb() { return eng.memTotalMb; }

  // ---------------------------------------------------------------- план

  void showPlan() {
    clear();
    final Engine e = eng;
    title(L.t("a020"));
    if (e.platId.equals("unknown")) text(L.t("a035"), WARN, 14);
    if (e.items.isEmpty()) { text(L.t("a036"), OKC, 15); button(L.t("a071"), true, back()); return; }
    final Button apply = mkButton("", true);
    final Runnable upd = new Runnable() { public void run() { apply.setText(L.t("a030", count(e.items))); } };
    String g = "";
    final List<CheckBox> boxes = new ArrayList<CheckBox>();
    for (final Engine.Item it : e.items) {
      if (!it.group.equals(g)) { g = it.group; TextView h = text(g, ACC, 15); h.setTypeface(Typeface.DEFAULT_BOLD); h.setPadding(0, dp(12), 0, dp(4)); }
      CheckBox cb = new CheckBox(this);
      cb.setText(it.text);
      cb.setTextColor(TXT);
      cb.setTextSize(14);
      cb.setChecked(it.on);
      if (Build.VERSION.SDK_INT >= 21) cb.setButtonTintList(android.content.res.ColorStateList.valueOf(ACC));
      cb.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
        public void onCheckedChanged(CompoundButton b, boolean on) { it.on = on; upd.run(); }
      });
      boxes.add(cb);
      page.addView(cb, lp(-1, -2, 2));
    }
    space(12);
    upd.run();
    apply.setOnClickListener(new View.OnClickListener() {
      public void onClick(View v) {
        final List<Engine.Item> sel = new ArrayList<Engine.Item>();
        for (Engine.Item it : e.items) if (it.on) sel.add(it);
        if (sel.isEmpty()) { toastMsg(L.t("a038")); return; }
        new AlertDialog.Builder(MainActivity.this).setMessage(L.t("a032", sel.size()))
          .setPositiveButton(L.t("a033"), new DialogInterface.OnClickListener() { public void onClick(DialogInterface d, int w) { runApply(sel); } })
          .setNegativeButton(L.t("a034"), null).show();
      }
    });
    page.addView(apply, lp(-1, -2, 8));
    button(L.t("a031"), false, new View.OnClickListener() { public void onClick(View v) { for (CheckBox cb : boxes) cb.setChecked(false); } });
    button(L.t("a071"), false, back());
  }

  static int count(List<Engine.Item> l) { int n = 0; for (Engine.Item it : l) if (it.on) n++; return n; }

  View.OnClickListener back() { return new View.OnClickListener() { public void onClick(View v) { showSummary(); } }; }

  void runApply(final List<Engine.Item> sel) {
    busy = true;
    clear();
    title(L.t("a020"));
    text(L.t("a040"), WARN, 14);
    bar = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
    page.addView(bar, lp(-1, -2, 8));
    startLog();
    new Thread(new Runnable() {
      public void run() {
        try {
          journal = eng.apply(sel, journal);
          busy = false;
          ui.post(new Runnable() { public void run() { showResult(false); } });
        } catch (IOException e) { lost(e); }
      }
    }).start();
  }

  void lost(IOException e) {
    busy = false;
    final String m = L.t("a080", e.getMessage());
    if (conn != null) conn.close();
    conn = null;
    eng = null;
    ui.post(new Runnable() { public void run() { showHome(m); } });
  }

  void showResult(boolean rolledBack) {
    final Engine e = eng;
    space(8);
    LinearLayout c = card();
    if (e.before != null && e.after != null) cardText(c, L.t("a153", e.before.memAvailMb, e.after.memAvailMb, e.before.procs, e.after.procs, e.before.disabled, e.after.disabled), TXT);
    cardText(c, rolledBack ? L.t("a045") : L.t("a041"), rolledBack ? OKC : WARN);
    if (!rolledBack) cardText(c, L.t("a170"), MUTED);
    if (!rolledBack && journal != null && !journal.entries.isEmpty())
      button(L.t("a042"), false, new View.OnClickListener() { public void onClick(View v) { confirmRollback(null); } });
    button(L.t("a021"), false, new View.OnClickListener() { public void onClick(View v) { share(); } });
    button(L.t("a043"), true, back());
    scrollDown();
  }

  // ---------------------------------------------------------------- откат

  void showRollback() {
    clear();
    title(L.t("a022"));
    final Engine.Journal j = journal;
    if (j == null || j.entries.isEmpty()) { text(L.t("a047"), MUTED, 15); button(L.t("a071"), true, back()); return; }
    text(L.t("a160", j.created, j.entries.size()), MUTED, 14);
    if (j.fingerprint.length() > 0 && !j.fingerprint.equals(eng.fingerprint)) text(L.t("a048", j.fingerprint), WARN, 13);
    final Set<Integer> pick = new HashSet<Integer>();
    final Button go = mkButton("", true);
    final Runnable upd = new Runnable() { public void run() { go.setText(L.t("a044", pick.size())); } };
    for (int i = 0; i < j.entries.size(); i++) {
      final int idx = i;
      pick.add(i);
      CheckBox cb = new CheckBox(this);
      cb.setText((i + 1) + ". " + eng.describe(j.entries.get(i)));
      cb.setTextColor(TXT);
      cb.setChecked(true);
      if (Build.VERSION.SDK_INT >= 21) cb.setButtonTintList(android.content.res.ColorStateList.valueOf(ACC));
      cb.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
        public void onCheckedChanged(CompoundButton b, boolean on) { if (on) pick.add(idx); else pick.remove(idx); upd.run(); }
      });
      page.addView(cb, lp(-1, -2, 2));
    }
    upd.run();
    go.setOnClickListener(new View.OnClickListener() {
      public void onClick(View v) {
        if (pick.isEmpty()) { toastMsg(L.t("a038")); return; }
        confirmRollback(pick.size() == j.entries.size() ? null : new HashSet<Integer>(pick));
      }
    });
    page.addView(go, lp(-1, -2, 12));
    button(L.t("a071"), false, back());
  }

  void confirmRollback(final Set<Integer> only) {
    int n = only == null ? journal.entries.size() : only.size();
    new AlertDialog.Builder(this).setMessage(L.t("a046", n))
      .setPositiveButton(L.t("a042"), new DialogInterface.OnClickListener() {
        public void onClick(DialogInterface d, int w) { runRollback(only); }
      })
      .setNegativeButton(L.t("a034"), null).show();
  }

  void runRollback(final Set<Integer> only) {
    busy = true;
    clear();
    title(L.t("a022"));
    startLog();
    new Thread(new Runnable() {
      public void run() {
        try {
          eng.rollback(journal, only);
          busy = false;
          ui.post(new Runnable() { public void run() { showResult(true); } });
        } catch (IOException e) { lost(e); }
      }
    }).start();
  }

  // ---------------------------------------------------------------- отчёт

  void share() {
    Intent i = new Intent(Intent.ACTION_SEND);
    i.setType("text/plain");
    i.putExtra(Intent.EXTRA_SUBJECT, L.t("a150", Engine.VERSION) + " — " + eng.model);
    i.putExtra(Intent.EXTRA_TEXT, eng.reportText(journal));
    try { startActivity(Intent.createChooser(i, L.t("a021"))); } catch (Exception ignored) {}
  }

  // ---------------------------------------------------------------- проверка в CI на эмуляторе (только эмулятор)

  static boolean isEmulator() {
    String fp = Build.FINGERPRINT == null ? "" : Build.FINGERPRINT;
    String hw = Build.HARDWARE == null ? "" : Build.HARDWARE;
    return fp.startsWith("generic") || fp.contains("emulator") || fp.contains("sdk_gphone") || hw.contains("ranchu") || hw.contains("goldfish");
  }

  void autotest(final String what) {
    clear();
    title("autotest");
    startLog();
    final String kinds = getIntent().getStringExtra("kinds") == null ? "anim,disable" : getIntent().getStringExtra("kinds");
    final int delay = getIntent().getIntExtra("delay", 0);
    new Thread(new Runnable() {
      public void run() {
        try {
          AdbKey k = ensureKey();
          if (what.equals("key")) {
            File d = getExternalFilesDir(null);
            FileOutputStream o = new FileOutputStream(new File(d, "adbkey.pub"));
            o.write((k.adbPublicKey("car-kit@phone") + "\n").getBytes("UTF-8"));
            o.close();
            alog("AUTOTEST KEY " + k.fingerprint());
            return;
          }
          if (delay > 0) Thread.sleep(delay * 1000L);
          String[] hp = Scan.parseAddr(what);
          conn = AdbConn.connect(hp[0], Integer.parseInt(hp[1]), k, 20, null);
          alog("AUTOTEST CONNECTED " + conn.banner);
          eng = new Engine(conn, data, L, new Engine.Log() {
            public void line(String t, int kind) { alog("  " + t); }
            public void progress(int done, int total) {}
          });
          eng.dnsWaitSec = 3;
          eng.settleMs = 1000;
          eng.diagnose();
          alog("AUTOTEST DIAG platform=" + eng.platId + " model=" + eng.model + " sdk=" + eng.sdk + " items=" + eng.items.size());
          List<Engine.Item> sel = new ArrayList<Engine.Item>();
          for (Engine.Item it : eng.items) if (("," + kinds + ",").contains("," + it.kind + ",") && it.on) sel.add(it);
          Engine.Journal j = eng.apply(sel, new Engine.Journal(journalFile(eng.unitId)));
          alog("AUTOTEST APPLIED " + j.entries.size());
          int n = j.entries.size();
          eng.rollback(Engine.Journal.load(j.file), null);
          alog("AUTOTEST ROLLBACK " + Engine.Journal.load(j.file).entries.size());
          alog(n >= 0 ? "AUTOTEST OK" : "AUTOTEST FAIL");
        } catch (Throwable e) {
          alog("AUTOTEST FAIL " + e);
        } finally {
          if (conn != null) conn.close();
        }
      }
    }).start();
  }

  void alog(String s) { android.util.Log.i("CARKIT", s); postMsg(s, MUTED); }

  // ---------------------------------------------------------------- вид

  void clear() { page.removeAllViews(); logBox = null; bar = null; scroll.scrollTo(0, 0); }

  int dp(int v) { return (int) (v * getResources().getDisplayMetrics().density + 0.5f); }

  LinearLayout.LayoutParams lp(int w, int h, int top) {
    LinearLayout.LayoutParams l = new LinearLayout.LayoutParams(w, h);
    l.topMargin = dp(top);
    return l;
  }

  void title(String s) {
    TextView t = text(s, TXT, 22);
    t.setTypeface(Typeface.DEFAULT_BOLD);
    t.setPadding(0, 0, 0, dp(6));
  }

  TextView text(String s, int color, int sp) {
    TextView t = new TextView(this);
    t.setText(s);
    t.setTextColor(color);
    t.setTextSize(sp);
    t.setLineSpacing(0, 1.15f);
    page.addView(t, lp(-1, -2, 6));
    return t;
  }

  void space(int h) { View v = new View(this); page.addView(v, lp(-1, dp(h), 0)); }

  Button mkButton(String s, boolean primary) {
    Button b = new Button(this);
    b.setText(s);
    b.setAllCaps(false);
    b.setTextSize(16);
    b.setTextColor(primary ? 0xFF0B1A10 : TXT);
    GradientDrawable g = new GradientDrawable();
    g.setCornerRadius(dp(10));
    g.setColor(primary ? ACC : CARD);
    if (!primary) g.setStroke(dp(1), 0xFF2E3A44);
    b.setBackground(g);
    b.setMinHeight(dp(52));
    b.setPadding(dp(14), dp(8), dp(14), dp(8));
    return b;
  }

  Button button(String s, boolean primary, View.OnClickListener l) {
    Button b = mkButton(s, primary);
    b.setOnClickListener(l);
    page.addView(b, lp(-1, -2, 10));
    return b;
  }

  LinearLayout card() {
    LinearLayout c = new LinearLayout(this);
    c.setOrientation(LinearLayout.VERTICAL);
    GradientDrawable g = new GradientDrawable();
    g.setCornerRadius(dp(12));
    g.setColor(CARD);
    c.setBackground(g);
    c.setPadding(dp(14), dp(10), dp(14), dp(12));
    page.addView(c, lp(-1, -2, 12));
    return c;
  }

  void cardText(LinearLayout c, String s, int color) {
    TextView t = new TextView(this);
    t.setText(s);
    t.setTextColor(color);
    t.setTextSize(14);
    t.setLineSpacing(0, 1.15f);
    t.setPadding(0, dp(4), 0, 0);
    c.addView(t);
  }

  void startLog() {
    logBox = new LinearLayout(this);
    logBox.setOrientation(LinearLayout.VERTICAL);
    page.addView(logBox, lp(-1, -2, 8));
  }

  void postMsg(final String s, final int color) {
    ui.post(new Runnable() {
      public void run() {
        if (logBox == null) return;
        TextView t = new TextView(MainActivity.this);
        t.setText(s);
        t.setTextColor(color);
        t.setTextSize(13);
        logBox.addView(t);
        if (logBox.getChildCount() > 400) logBox.removeViewAt(0);
        scrollDown();
      }
    });
  }

  void setText(final TextView t, final String s, final int color) {
    ui.post(new Runnable() { public void run() { t.setText(s); t.setTextColor(color); } });
  }

  void scrollDown() { scroll.post(new Runnable() { public void run() { scroll.fullScroll(View.FOCUS_DOWN); } }); }

  void toastMsg(String s) { android.widget.Toast.makeText(this, s, android.widget.Toast.LENGTH_SHORT).show(); }
}

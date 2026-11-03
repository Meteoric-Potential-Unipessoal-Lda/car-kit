package net.zherdyev.carkit;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Логика car-kit (carkit.ps1) для телефона: диагностика магнитолы, план с галочками, применение партиями
 * с проверкой служб магнитолы и откат по журналу. Без android.* — тестируется на обычной Java (tests/mobile).
 */
public final class Engine {
  public static final String VERSION = "0.4";
  public static final int INFO = 0, OK = 1, WARN = 2, BAD = 3;

  public interface Log {
    void line(String text, int kind);
    void progress(int done, int total);
  }

  public static final class Item {
    public String kind, pkg = "", text, group, tier = "";
    public boolean on;
    Item(String kind, String pkg, String text, boolean on, String group, String tier) {
      this.kind = kind; this.pkg = pkg == null ? "" : pkg; this.text = text; this.on = on; this.group = group; this.tier = tier == null ? "" : tier;
    }
  }

  /** Запись журнала: что изменено и как вернуть (те же типы, что у набора: disable, uninstall, setting, appops, idle). */
  public static final class Entry {
    public String t = "", pkg = "", key = "", old = "", nw = "";
    String tsv() { return t + "\t" + pkg + "\t" + key + "\t" + old + "\t" + nw; }
    static Entry of(String line) {
      String[] f = line.split("\t", -1);
      Entry e = new Entry();
      e.t = f[0]; if (f.length > 1) e.pkg = f[1]; if (f.length > 2) e.key = f[2]; if (f.length > 3) e.old = f[3]; if (f.length > 4) e.nw = f[4];
      return e;
    }
  }

  /** Журнал изменений одной магнитолы — файл в папке приложения; по нему делается откат даже через месяц. */
  public static final class Journal {
    public final File file;
    public String unit = "", model = "", fingerprint = "", created = "", kit = "";
    public final List<Entry> entries = new ArrayList<Entry>();
    public Journal(File f) { file = f; }
    public void save() throws IOException {
      StringBuilder sb = new StringBuilder();
      sb.append("#kit\t").append(kit).append('\n').append("#unit\t").append(unit).append('\n').append("#model\t").append(model).append('\n')
        .append("#fingerprint\t").append(fingerprint).append('\n').append("#created\t").append(created).append('\n');
      for (Entry e : entries) sb.append(e.tsv()).append('\n');
      File tmp = new File(file.getPath() + ".tmp");
      FileOutputStream o = new FileOutputStream(tmp);
      try { o.write(sb.toString().getBytes("UTF-8")); o.getFD().sync(); } finally { o.close(); }
      if (!tmp.renameTo(file)) throw new IOException("cannot save " + file);
    }
    public static Journal load(File f) throws IOException {
      Journal j = new Journal(f);
      String t = new String(AdbKey.readAll(new java.io.FileInputStream(f)), "UTF-8");
      for (String l : t.split("\n")) {
        if (l.length() == 0) continue;
        if (l.startsWith("#")) {
          String[] kv = l.substring(1).split("\t", 2);
          String v = kv.length > 1 ? kv[1] : "";
          if (kv[0].equals("kit")) j.kit = v; else if (kv[0].equals("unit")) j.unit = v; else if (kv[0].equals("model")) j.model = v;
          else if (kv[0].equals("fingerprint")) j.fingerprint = v; else if (kv[0].equals("created")) j.created = v;
          continue;
        }
        j.entries.add(Entry.of(l));
      }
      return j;
    }
  }

  public static final class Snap { public long memAvailMb, dataFreeMb; public int procs, disabled; }

  final Sh sh;
  final Data d;
  final Lang L;
  final Log log;

  public Engine(Sh sh, Data d, Lang L, Log log) { this.sh = sh; this.d = d; this.L = L; this.log = log; }

  // ---------------------------------------------------------------- команды

  public final List<String> notes = new ArrayList<String>();
  public final List<String> changes = new ArrayList<String>();

  static boolean readOnly(String cmd) {
    if (Pat.WRITE_META.matcher(cmd).find()) return false;
    for (Pattern p : Pat.READ) if (p.matcher(cmd).find()) return true;
    return false;
  }

  static boolean writeAllowed(String cmd) {
    if (Pat.WRITE_META.matcher(cmd).find()) return false;
    for (Pattern p : Pat.WRITE) if (p.matcher(cmd).find()) return true;
    return false;
  }

  String S(String cmd) throws IOException { return S(cmd, 40); }

  String S(String cmd, int timeout) throws IOException {
    if (!readOnly(cmd)) throw new IOException(L.t("m002", cmd));
    String o = sh.sh(cmd, timeout);
    if (o.endsWith("\nTIMEOUT")) { notes.add(L.t("m003", timeout, cmd)); return ""; }
    return o;
  }

  String W(String cmd) throws IOException { return W(cmd, 120); }

  String W(String cmd, int timeout) throws IOException {
    if (!writeAllowed(cmd)) throw new IOException(L.t("m117", cmd));
    String o = sh.sh(cmd, timeout).trim();
    if (o.endsWith("\nTIMEOUT") || o.equals("TIMEOUT")) o = "TIMEOUT " + o.replace("\nTIMEOUT", "");
    changes.add(new SimpleDateFormat("HH:mm:ss", Locale.US).format(new Date()) + " > " + cmd + "\n           " + o);
    return o;
  }

  void say(String t, int kind) { if (log != null) log.line(t, kind); opt.add(t); }

  public final List<String> opt = new ArrayList<String>();

  // ---------------------------------------------------------------- разбор

  static Map<String, String> parseProps(String t) {
    Map<String, String> r = new HashMap<String, String>();
    Matcher m = Pattern.compile("(?m)^\\[([^\\]]+)\\]: \\[(.*)\\]\\s*$").matcher(t);
    while (m.find()) r.put(m.group(1), m.group(2));
    return r;
  }

  static Set<String> pkgList(String t) {
    Set<String> s = new HashSet<String>();
    Matcher m = Pattern.compile("(?m)^package:([A-Za-z0-9_.]+)(\\s|$)").matcher(t);
    while (m.find()) s.add(m.group(1));
    return s;
  }

  static Map<String, Long> meminfo(String t) {
    Map<String, Long> h = new HashMap<String, Long>();
    Matcher m = Pattern.compile("(?m)^(\\w+):\\s+(\\d+) kB").matcher(t);
    while (m.find()) h.put(m.group(1), Long.parseLong(m.group(2)));
    return h;
  }

  static long mb(long kb) { return Math.round(kb / 1024.0); }

  static final class Proc { long kb; String name; Proc(long k, String n) { kb = k; name = n; } }

  static List<Proc> parsePs(String t) {
    List<Proc> r = new ArrayList<Proc>();
    Pattern a = Pattern.compile("^\\s*(\\d+)\\s+(\\S+)\\s*$"), b = Pattern.compile("^\\S+\\s+\\d+\\s+\\d+\\s+\\d+\\s+(\\d+)\\s+\\S+\\s+\\S+\\s+\\S+\\s+(\\S+)\\s*$");
    for (String l : t.split("\n")) {
      Matcher m = a.matcher(l);
      if (m.find()) { r.add(new Proc(Long.parseLong(m.group(1)), m.group(2))); continue; }
      m = b.matcher(l);
      if (m.find()) r.add(new Proc(Long.parseLong(m.group(1)), m.group(2)));
    }
    return r;
  }

  static long parseDuration(String s) {
    s = s.trim();
    Matcher m = Pattern.compile("^\\+?(?:(\\d+)d)?(?:(\\d+)h)?(?:(\\d+)m)?(?:(\\d+)s)?(?:\\d+ms)?$").matcher(s);
    if (s.matches(".*[dhms].*") && m.find()) return n(m.group(1)) * 86400 + n(m.group(2)) * 3600 + n(m.group(3)) * 60 + n(m.group(4));
    long days = 0;
    m = Pattern.compile("^(\\d+)d\\s*(.*)$").matcher(s);
    if (m.find()) { days = Long.parseLong(m.group(1)); s = m.group(2); }
    s = s.replaceAll("\\.\\d+$", "");
    long sec = 0;
    for (String x : s.split(":")) if (x.matches("^\\d+$")) sec = sec * 60 + Long.parseLong(x);
    return days * 86400 + sec;
  }

  private static long n(String s) { return s == null || s.length() == 0 ? 0 : Long.parseLong(s); }

  static final class Usage { String pkg; long sec; long last; }

  static Map<String, Usage> parseUsage(String t) {
    Map<String, Usage> h = new HashMap<String, Usage>();
    Pattern p = Pattern.compile("package=([A-Za-z0-9_.]+)\\s+totalTime(?:Used)?=\"([^\"]+)\""), q = Pattern.compile("lastTime(?:Used)?=\"(\\d{4}-\\d\\d-\\d\\d \\d\\d:\\d\\d:\\d\\d)\"");
    SimpleDateFormat f = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.US);
    for (String l : t.split("\n")) {
      Matcher m = p.matcher(l);
      if (!m.find()) continue;
      String pkg = m.group(1);
      long sec = parseDuration(m.group(2)), last = 0;
      Matcher m2 = q.matcher(l);
      if (m2.find()) { try { last = f.parse(m2.group(1)).getTime(); } catch (Exception ignored) {} }
      Usage u = h.get(pkg);
      if (u == null) { u = new Usage(); u.pkg = pkg; u.sec = sec; u.last = last; h.put(pkg, u); }
      else { if (u.sec < sec) u.sec = sec; if (u.last < last) u.last = last; }
    }
    return h;
  }

  static Map<String, List<String>> parseRoles(String t) {
    Map<String, List<String>> h = new HashMap<String, List<String>>();
    String name = "", user = "0";
    Pattern pu = Pattern.compile("user_id=(\\d+)"), pn = Pattern.compile("name=(android\\.app\\.role\\.[A-Z_]+)"), ph = Pattern.compile("holders=\\[?([A-Za-z0-9_.,\\s]*)\\]?");
    for (String l : t.split("\n")) {
      Matcher m = pu.matcher(l);
      if (m.find()) { user = m.group(1); continue; }
      if (!user.equals("0")) continue;
      m = pn.matcher(l);
      if (m.find()) { name = m.group(1); continue; }
      m = ph.matcher(l);
      if (name.length() > 0 && m.find()) {
        List<String> hs = new ArrayList<String>();
        for (String x : m.group(1).split("[,\\s]+")) if (x.matches("^[A-Za-z0-9_.]+$")) hs.add(x);
        if (!hs.isEmpty()) h.put(name, hs);
        name = "";
      }
    }
    return h;
  }

  static List<String> pkgsFromComponents(String s) {
    List<String> r = new ArrayList<String>();
    for (String x : s.split(":")) { Matcher m = Pattern.compile("^([A-Za-z0-9_.]+)/").matcher(x); if (m.find()) r.add(m.group(1)); }
    return r;
  }

  // ---------------------------------------------------------------- платформа (Get-CarPlatform)

  public Map<String, String> props = new HashMap<String, String>();
  String P(String k) { String v = props.get(k); return v == null ? "" : v.trim(); }

  public String platId = "unknown", platName = "", chip = "", model = "", unitId = "", homeComp = "";
  public int sdk = 0;
  public List<String> core = new ArrayList<String>();

  static String chipName(String bp, String hw) {
    Map<String, String> m = new HashMap<String, String>();
    String[] kv = { "ums512", "Unisoc UIS7862", "sp9863a", "Unisoc UIS8581", "ums9620", "Unisoc UIS7870", "sp9853i", "Intel/Spreadtrum SC9853i",
      "rk3368", "Rockchip PX5 (RK3368)", "rk3399", "Rockchip PX6 (RK3399)", "px30", "Rockchip PX30", "rk3326", "Rockchip PX30 (RK3326)", "rk3188", "Rockchip PX3 (RK3188)", "px3", "Rockchip PX3",
      "rk3566", "Rockchip RK3566", "rk3568", "Rockchip RK3568", "msm8953", "Qualcomm SDM625/450", "qcm6125", "Qualcomm QCM6125", "sm6125", "Qualcomm SM6125", "sdm660", "Qualcomm SDM660" };
    for (int i = 0; i < kv.length; i += 2) m.put(kv[i], kv[i + 1]);
    String k = bp.toLowerCase(Locale.US);
    if (m.containsKey(k)) return m.get(k);
    String h = hw.toLowerCase(Locale.US);
    if (k.matches("^(mt\\d+|ac\\d+).*") || h.matches("^mt\\d+.*")) return "MediaTek " + (bp.length() > 0 ? bp.toUpperCase(Locale.US) : hw.toUpperCase(Locale.US));
    if (k.matches("^sun\\d.*") || h.matches("^sun\\d.*")) return "Allwinner " + (bp.length() > 0 ? bp : hw);
    if (k.matches("^(ums|sp|sc)\\d.*")) return "Unisoc " + bp;
    if (k.matches("^rk.*")) return "Rockchip " + bp.toUpperCase(Locale.US);
    return bp;
  }

  void detectPlatform(Set<String> all, String apkPaths, String featTxt) {
    String bp = P("ro.board.platform"), hw = P("ro.hardware");
    String man = (P("ro.product.manufacturer") + " " + P("ro.product.brand")).toLowerCase(Locale.US);
    String id = "unknown", family = "";
    String fytMan = P("ro.build.fytmanufacturer");
    boolean mtc = Pattern.compile("MTCManager|HCTManagerService", Pattern.CASE_INSENSITIVE).matcher(apkPaths).find();
    if (!mtc) for (String p : all) if (p.matches("^(android|com)\\.microntek\\..*")) { mtc = true; break; }
    if (featTxt.contains("android.hardware.type.automotive")) id = "aaos";
    else if (P("ro.fyt.platform").length() > 0 || fytMan.length() > 0 || P("ro.fyt.uiid").length() > 0 || P("sys.fyt.platform").length() > 0 || all.contains("com.syu.ms")) {
      id = "fyt";
      if (fytMan.equals("95") || man.contains("teyes")) id = "teyes";
      else if (man.contains("atoto")) { id = "atoto"; family = "FYT"; }
    }
    else if (all.contains("com.qf.framework") || P("persist.sys.qf.launcher").length() > 0 || P("ro.qf.platform").length() > 0 || P("sys.qf.is.acc.on").length() > 0) id = "qf";
    else if (all.contains("com.tw.car") || all.contains("com.tw.carchoose") || all.contains("com.tv.carinfoservice") || P("ro.build.display.id").matches("(?i)^TS\\d.*")) id = "ts";
    else if (mtc) id = "mtc";
    else if (all.contains("com.reglink.services") || all.contains("com.reglink.launcher4")) id = "reglink";
    else if (all.contains("com.hcn.autocan") || all.contains("com.hcn.bluetoothservice") || all.contains("com.hcn.autoradio") || P("persist.sys.hcnport").length() > 0) { id = "hcn"; if (man.contains("atoto")) family = "ATOTO"; }
    else if (P("persist.nwd.launcher.default").length() > 0 || P("ro.nwd.start.launcher.by.fw").length() > 0) id = "nwd";
    else if (bp.matches("(?i)^sun\\d.*") || hw.matches("(?i)^sun\\d.*") || P("ro.product.board").toLowerCase(Locale.US).contains("allwinner")) id = "allwinner";
    else if (man.contains("atoto")) id = "atoto";
    Map<String, String[]> cores = new HashMap<String, String[]>();
    String[] syu = { "com.syu.ms", "com.syu.canbus", "com.syu.bt" };
    cores.put("fyt", syu); cores.put("teyes", syu);
    cores.put("atoto", new String[] { "com.syu.ms", "com.syu.canbus", "com.syu.bt", "com.atoto.keepaliveservice", "com.hcn.bluetoothservice" });
    cores.put("qf", new String[] { "com.qf.framework", "com.qf.vehicle", "com.qf.bluetooth" });
    cores.put("ts", new String[] { "com.tw.car", "com.tv.carinfoservice" });
    cores.put("mtc", new String[] { "android.microntek.service", "android.microntek.mtcser", "com.microntek.controlsettings" });
    cores.put("reglink", new String[] { "com.reglink.services" });
    cores.put("hcn", new String[] { "com.hcn.bluetoothservice", "com.hcn.autocan" });
    Map<String, String> names = new HashMap<String, String>();
    String[] nv = { "fyt", "FYT (SYU)", "teyes", "Teyes (FYT)", "atoto", "ATOTO", "qf", "QF / Qianfeng", "ts", "Topway TS", "mtc", "Microntek MTCD/MTCE (HCT)",
      "reglink", "Reglink (MTK)", "hcn", "HCN", "nwd", "NWD (Nowadays)", "allwinner", "Allwinner", "aaos", "Android Automotive OS", "unknown", "" };
    for (int i = 0; i < nv.length; i += 2) names.put(nv[i], nv[i + 1]);
    platId = id;
    platName = names.get(id) + (family.length() > 0 ? " (" + family + ")" : "");
    chip = chipName(bp, hw);
    core = new ArrayList<String>();
    String[] c = cores.get(id);
    if (c != null) for (String x : c) if (all.contains(x)) core.add(x);
  }

  // ---------------------------------------------------------------- защита (Test-Protected)

  boolean isProtected(String pkg) {
    String cl = d.carLevel.get(pkg), rl = d.ruLevel.get(pkg);
    if ("protect".equals(cl)) return true;
    if ("ok".equals(cl) || "ask".equals(cl)) return false;
    if ("ok".equals(rl)) return false;
    for (Pattern p : Pat.PROTECTED) if (p.matcher(pkg).find()) return true;
    return "protect".equals(rl);
  }

  // ---------------------------------------------------------------- диагностика

  public final List<String> obs = new ArrayList<String>();
  public final List<Item> items = new ArrayList<Item>();
  public final List<String> report = new ArrayList<String>();
  public Snap before, after;
  public boolean diagOnly = false;
  public long memTotalMb = 0;
  public String fingerprint = "";

  Set<String> all = new HashSet<String>(), third = new HashSet<String>(), disabled = new HashSet<String>(), usedPkgs = new HashSet<String>();
  Set<String> keepSet = new HashSet<String>(), roleSet = new HashSet<String>();
  List<Proc> procs = new ArrayList<Proc>();
  String psCmd = "ps -A";
  Map<String, String> set = new LinkedHashMap<String, String>();
  List<String> preUninst = new ArrayList<String>();

  long rssMb(String pkg) {
    long kb = 0;
    for (Proc p : procs) if (p.name.equals(pkg) || p.name.startsWith(pkg + ":")) kb += p.kb;
    return mb(kb);
  }

  boolean running(String pkg) {
    for (Proc p : procs) if (p.name.equals(pkg) || p.name.startsWith(pkg + ":")) return true;
    return false;
  }

  String G(String ns, String k) throws IOException { return S("settings get " + ns + " " + k).trim(); }

  long dataFree() throws IOException {
    Matcher m = Pattern.compile("(?m)^\\S+\\s+\\d+\\s+\\d+\\s+(\\d+)\\s+\\d+%").matcher(S("df -k /data"));
    return m.find() ? Long.parseLong(m.group(1)) : 0;
  }

  public Snap snap() {
    Snap s = new Snap();
    try {
      Long a = meminfo(S("cat /proc/meminfo")).get("MemAvailable");
      if (a != null) s.memAvailMb = mb(a);
      s.procs = parsePs(S(psCmd)).size();
      s.dataFreeMb = mb(dataFree());
      s.disabled = pkgList(S("pm list packages -d")).size();
    } catch (IOException ignored) {}
    return s;
  }

  public static String unitId(Sh sh) throws IOException {
    String sn = sh.sh("getprop ro.serialno", 10).trim();
    if (sn.length() > 0 && !sn.matches("^(0123456789ABCDEF|unknown|0+)$") && !sn.contains("TIMEOUT")) return sn;
    return "aid:" + sh.sh("settings get secure android_id", 10).trim();
  }

  private int step = 0;
  void step(String t) { step++; if (log != null) log.line("[" + step + "] " + t, INFO); }

  /** Полная диагностика (только чтение) + план. */
  public void diagnose() throws IOException {
    step(L.t("a101"));
    String propsTxt = S("getprop");
    props = parseProps(propsTxt);
    model = P("ro.product.model");
    fingerprint = P("ro.build.fingerprint");
    try { sdk = Integer.parseInt(P("ro.build.version.sdk")); } catch (NumberFormatException e) { sdk = 0; }
    unitId = unitId(sh);
    Set<String> all0 = pkgList(S("pm list packages"));
    String apkTxt = S("pm list packages -f");
    String featTxt = S("pm list features");
    detectPlatform(all0, apkTxt, featTxt);
    String adbPersist = P("persist.adb.tcp.port");
    boolean rootAdb = S("id").trim().startsWith("uid=0(");
    if (platId.equals("aaos")) { say(L.t("k062"), WARN); say(L.t("k063"), WARN); diagOnly = true; }
    else if (platId.equals("unknown")) say(L.t("k061", chip), WARN);
    else say(L.t("k060", platName, chip), OK);

    step(L.t("m257"));
    Map<String, Long> mem = meminfo(S("cat /proc/meminfo"));
    long uptimeSec = 0;
    Matcher um = Pattern.compile("^(\\d+)").matcher(S("cat /proc/uptime").trim());
    if (um.find()) uptimeSec = Long.parseLong(um.group(1));
    for (String pc : new String[] { "ps -A -o RSS,NAME", "ps -A", "ps" }) {
      procs = parsePs(S(pc));
      if (procs.size() >= 3) { psCmd = pc; break; }
    }

    step(L.t("m268"));
    long dataTotal = 0, dataUsed = 0, dataFree = 0;
    Matcher dm = Pattern.compile("(?m)^\\S+\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+\\d+%").matcher(S("df -k /data"));
    if (dm.find()) { dataTotal = Long.parseLong(dm.group(1)); dataUsed = Long.parseLong(dm.group(2)); dataFree = Long.parseLong(dm.group(3)); }
    long dataPct = dataTotal > 0 ? Math.round(100.0 * dataUsed / dataTotal) : 0;
    String dsTxt = S("dumpsys diskstats", 60);
    long cacheMb = 0;
    // как у набора: размеры кэша считаем, только если их столько же, сколько имён пакетов
    List<String> dsNames = jsonArr(dsTxt, "App Package Names"), dsCache = jsonArr(dsTxt, "Cache Sizes");
    if (!dsNames.isEmpty() && dsCache.size() == dsNames.size()) {
      long sum = 0;
      for (String x : dsCache) { try { sum += Long.parseLong(x); } catch (NumberFormatException ignored) {} }
      cacheMb = Math.round(sum / 1048576.0);
    }

    step(L.t("m269"));
    all = pkgList(S("pm list packages"));
    Set<String> allU = pkgList(S("pm list packages -u"));
    Set<String> sys = pkgList(S("pm list packages -s"));
    third = pkgList(S("pm list packages -3"));
    disabled = pkgList(S("pm list packages -d"));
    preUninst = new ArrayList<String>();
    for (String p : allU) if (!all.contains(p)) preUninst.add(p);
    Map<String, String> installer = new HashMap<String, String>();
    Matcher im = Pattern.compile("(?m)^package:([A-Za-z0-9_.]+)\\s+installer=(\\S+)").matcher(S("pm list packages -i -3"));
    while (im.find()) installer.put(im.group(1), im.group(2));
    Set<String> launchable = new HashSet<String>();
    Matcher lm = Pattern.compile("(?m)^\\s*([A-Za-z0-9_.]+)/").matcher(S("cmd package query-activities --brief -a android.intent.action.MAIN -c android.intent.category.LAUNCHER"));
    while (lm.find()) launchable.add(lm.group(1));

    step(L.t("m270"));
    homeComp = homeComp();
    String homePkg = homeComp.split("/")[0];
    Map<String, List<String>> roles = new HashMap<String, List<String>>();
    if (sdk >= 29) roles = parseRoles(S("dumpsys role"));
    String ime = G("secure", "default_input_method");
    String imePkg = ime.split("/")[0];

    step(L.t("m271"));
    Map<String, Usage> usage = parseUsage(S("dumpsys usagestats", 120));
    boolean usageOk = usage.size() >= 5;
    usedPkgs = new HashSet<String>();
    long monthAgo = System.currentTimeMillis() - 30L * 86400000L;
    for (Usage u : usage.values()) if (u.sec >= 60 || u.last > monthAgo) usedPkgs.add(u.pkg);
    if (!usageOk) notes.add(L.t("m272"));

    step(L.t("m273"));
    List<String> a11yPkgs = pkgsFromComponents(G("secure", "enabled_accessibility_services"));
    List<String> nlsPkgs = pkgsFromComponents(G("secure", "enabled_notification_listeners"));
    String dpTxt = S("dumpsys device_policy");
    List<String> adminPkgs = new ArrayList<String>();
    Matcher am = Pattern.compile("ComponentInfo\\{([A-Za-z0-9_.]+)/").matcher(dpTxt);
    while (am.find()) if (!adminPkgs.contains(am.group(1))) adminPkgs.add(am.group(1));
    List<String> overlayPkgs = new ArrayList<String>(), installPkgs = new ArrayList<String>();
    if (sdk >= 29) { overlayPkgs = queryOp("SYSTEM_ALERT_WINDOW"); installPkgs = queryOp("REQUEST_INSTALL_PACKAGES"); }

    step(L.t("m276"));
    String connTxt = S("dumpsys connectivity");
    boolean dnsBroken = connTxt.contains("PRIVATE_DNS_BROKEN");
    set.put("anim_w", G("global", "window_animation_scale"));
    set.put("anim_t", G("global", "transition_animation_scale"));
    set.put("anim_d", G("global", "animator_duration_scale"));
    set.put("low_power", G("global", "low_power"));
    set.put("dns_mode", G("global", "private_dns_mode"));
    set.put("dns_spec", G("global", "private_dns_specifier"));
    set.put("finish_act", G("global", "always_finish_activities"));
    set.put("bg_limit", G("global", "background_process_limit"));
    set.put("verifier", G("global", "package_verifier_enable"));

    step(L.t("m291"));
    String crashTxt = S("logcat -d -b crash -t 400");
    Map<String, Integer> crashes = new HashMap<String, Integer>();
    Matcher crm = Pattern.compile("Process: ([A-Za-z0-9_.:]+)").matcher(crashTxt);
    while (crm.find()) { Integer c = crashes.get(crm.group(1)); crashes.put(crm.group(1), c == null ? 1 : c + 1); }

    long unitTime = 0;
    try { unitTime = Long.parseLong(S("date +%s").trim()); } catch (NumberFormatException ignored) {}
    long timeDiffMin = unitTime > 0 ? Math.round((System.currentTimeMillis() / 1000.0 - unitTime) / 60.0) : 0;
    String autoTime = G("global", "auto_time"), locMode = G("secure", "location_mode");
    int rssi = 0;
    Matcher wm = Pattern.compile("mWifiInfo[^\\n]*?RSSI: (-\\d+)").matcher(S("dumpsys wifi", 60));
    if (wm.find()) rssi = Integer.parseInt(wm.group(1));

    // ---------------- анализ
    step(L.t("m292"));
    roleSet = new HashSet<String>();
    for (List<String> hs : roles.values()) roleSet.addAll(hs);
    for (String x : new String[] { homePkg, imePkg }) if (x.length() > 0 && !x.equals("null")) roleSet.add(x);
    keepSet = new HashSet<String>(roleSet);
    keepSet.addAll(a11yPkgs); keepSet.addAll(nlsPkgs); keepSet.addAll(adminPkgs);
    boolean kids = all.contains("com.google.android.apps.kids.familylinkhelper") || roles.containsKey("android.app.role.SYSTEM_SUPERVISION")
      || Pattern.compile("(?i)supervision|kids").matcher(dpTxt).find() || all.contains("com.sec.android.app.kidshome");
    boolean launchOk = launchable.size() >= 5;

    // --- кандидаты: включённые системные пакеты из базы
    final class Cand { String pkg, removal, note, ask, tier, skip; long mbv; }
    List<Cand> cands = new ArrayList<Cand>();
    for (String pkg : new TreeSet<String>(sys)) {
      if (disabled.contains(pkg)) continue;
      Data.Uad u = d.uad.get(pkg);
      String rl = d.carLevel.containsKey(pkg) ? d.carLevel.get(pkg) : d.ruLevel.get(pkg);
      boolean rlKnown = "ok".equals(rl) || "ask".equals(rl) || "protect".equals(rl);
      if (u == null && !rlKnown) continue;
      String removal = u != null ? u.removal : "ok".equals(rl) ? "Recommended" : "Advanced";
      if ((removal.equals("Expert") || removal.equals("Unsafe")) && !("ok".equals(rl) || "ask".equals(rl))) continue;
      List<String> why = new ArrayList<String>();
      if (isProtected(pkg)) why.add(L.t("m298"));
      if (pkg.startsWith("com.android.") && !pkg.equals("com.android.chrome") && !removal.equals("Recommended")) why.add(L.t("m299"));
      if (keepSet.contains(pkg)) why.add(L.t("m300"));
      if (usedPkgs.contains(pkg)) why.add(L.t("m301"));
      if (u != null && u.neededby != null && u.neededby.length() > 0) {
        List<String> nb = new ArrayList<String>();
        for (String x : u.neededby.split(",")) if (x.length() > 0 && all.contains(x) && !disabled.contains(x)) nb.add(x);
        if (!nb.isEmpty()) why.add(L.t("m302") + join(nb, ", "));
      }
      String uname = u != null ? u.name : "";
      String ask = "";
      if (!usageOk) ask = L.t("m303");
      else if (launchOk && launchable.contains(pkg)) ask = L.t("m304");
      else if (!launchOk) ask = L.t("m305");
      else if ("ask".equals(rl)) ask = L.t("m306");
      else if (!"ok".equals(rl) && removal.equals("Advanced")) ask = L.t("m307");
      else if (!"ok".equals(rl) && Pat.AskPattern.matcher(pkg + " " + uname).find()) ask = L.t("m308");
      else if (kids && !"ok".equals(rl)) ask = L.t("m309");
      String tier = "ask";
      if (ask.length() == 0) tier = ("ok".equals(rl) || Pat.AutoPattern.matcher(pkg + " " + uname).find()) ? "auto" : "base";
      Cand c = new Cand();
      c.pkg = pkg; c.removal = removal; c.ask = ask; c.tier = tier; c.skip = join(why, "; "); c.mbv = rssMb(pkg);
      c.note = d.note.get(pkg); if (c.note == null || c.note.length() == 0) c.note = uname;
      cands.add(c);
    }
    final Map<String, Integer> tierOrder = new HashMap<String, Integer>();
    tierOrder.put("auto", 0); tierOrder.put("base", 1); tierOrder.put("ask", 2);
    List<Cand> candOk = new ArrayList<Cand>();
    for (Cand c : cands) if (c.skip.length() == 0) candOk.add(c);
    Collections.sort(candOk, new Comparator<Cand>() {
      public int compare(Cand a, Cand b) {
        int x = tierOrder.get(a.tier) - tierOrder.get(b.tier); if (x != 0) return x;
        x = (a.removal.equals("Recommended") ? 0 : 1) - (b.removal.equals("Recommended") ? 0 : 1); if (x != 0) return x;
        x = Long.compare(b.mbv, a.mbv); if (x != 0) return x;
        return a.pkg.compareTo(b.pkg);
      }
    });
    // Магнитолы: пакет от имени системы (sharedUserId android.uid.system) — часть прошивки -> не трогаем
    step(L.t("k066"));
    for (Cand c : candOk) {
      if ("ok".equals(d.carLevel.get(c.pkg)) || "ask".equals(d.carLevel.get(c.pkg)) || "ok".equals(d.ruLevel.get(c.pkg))) continue;
      String dp = S("dumpsys package " + c.pkg, 20);
      if (Pattern.compile("sharedUser=SharedUserSetting\\{[^}]*android\\.uid\\.system").matcher(dp).find() || Pattern.compile("(?m)^\\s*userId=1000\\b").matcher(dp).find()) c.skip = L.t("k049");
    }
    if (platId.equals("teyes") || chip.contains("UIS7870")) {
      for (Cand c : candOk) if (c.tier.equals("auto") && !"ok".equals(d.carLevel.get(c.pkg)) && !"ok".equals(d.ruLevel.get(c.pkg))) c.tier = "base";
      notes.add(L.t("k067"));
    }
    List<Cand> ok2 = new ArrayList<Cand>();
    for (Cand c : candOk) if (c.skip.length() == 0) ok2.add(c);
    candOk = ok2;

    // --- безопасность: сторонние приложения
    final class Susp { String pkg, level, why; }
    List<Susp> susp = new ArrayList<Susp>();
    for (String pkg : new TreeSet<String>(third)) {
      if (disabled.contains(pkg)) continue;
      List<String> strong = new ArrayList<String>(), weak = new ArrayList<String>();
      boolean side = false;
      String inst = installer.containsKey(pkg) ? installer.get(pkg) : "";
      boolean noInst = inst.length() == 0 || inst.equals("null");
      boolean preinst = inst.equals("android") || (noInst && d.uad.containsKey(pkg));
      if (a11yPkgs.contains(pkg)) strong.add(L.t("m310"));
      if (adminPkgs.contains(pkg)) strong.add(L.t("m311"));
      boolean webapk = pkg.startsWith("org.chromium.webapk.");
      boolean store = Pat.StoreInstallers.matcher(inst).find();
      if (!webapk) {
        if (inst.equals("com.android.shell")) { strong.add(L.t("m312")); side = true; }
        else if (!noInst && !store && !preinst) { strong.add(L.t("m313", inst)); side = true; }
        else if (noInst && !preinst) weak.add(L.t("m314"));
        if (launchOk && !launchable.contains(pkg) && !roleSet.contains(pkg) && !store && !preinst) strong.add(L.t("m315"));
      }
      if (nlsPkgs.contains(pkg)) weak.add(L.t("m316"));
      if (overlayPkgs.contains(pkg)) weak.add(L.t("m317"));
      if (installPkgs.contains(pkg)) weak.add(L.t("m318"));
      boolean cleaner = Pat.CleanerPattern.matcher(pkg).find();
      if (cleaner) strong.add(L.t("m319"));
      String lvl = "";
      if (strong.size() >= 2 || (side && weak.size() >= 1) || cleaner) lvl = "warn";
      else if (strong.size() >= 1 || (weak.size() >= 2 && !store)) lvl = "check";
      if (webapk) { lvl = "check"; weak.add(L.t("m320")); }
      if (lvl.length() > 0) {
        Susp s = new Susp(); s.pkg = pkg; s.level = lvl;
        List<String> w = new ArrayList<String>(strong); w.addAll(weak); s.why = join(w, "; ");
        susp.add(s);
      }
    }
    List<Susp> suspOk = new ArrayList<Susp>();
    for (Susp s : susp) if (s.level.equals("warn") && !roleSet.contains(s.pkg)) suspOk.add(s);
    Set<String> suspSet = new HashSet<String>();
    for (Susp s : suspOk) suspSet.add(s.pkg);

    // --- фон: сторонние, которые больше месяца не открывали, но сейчас работают
    List<String> bgCands = new ArrayList<String>();
    if (usageOk) {
      for (String pkg : new TreeSet<String>(third)) {
        if (keepSet.contains(pkg) || usedPkgs.contains(pkg) || disabled.contains(pkg) || Pat.KeepBgPattern.matcher(pkg).find() || suspSet.contains(pkg)) continue;
        if (!running(pkg)) continue;
        bgCands.add(pkg);
      }
      Collections.sort(bgCands, new Comparator<String>() { public int compare(String a, String b) { return Long.compare(rssMb(b), rssMb(a)); } });
      if (bgCands.size() > 15) bgCands = new ArrayList<String>(bgCands.subList(0, 15));
    }

    // --- «не усыплять» навигацию, музыку, CarPlay/Android Auto
    List<String[]> idleCands = new ArrayList<String[]>();
    if (sdk >= 23) {
      Set<String> idleSet = idleSet();
      for (String pkg : new TreeSet<String>(all)) {
        if (disabled.contains(pkg) || idleSet.contains(pkg) || !Pat.NavPattern.matcher(pkg).find()) continue;
        if (!(usedPkgs.contains(pkg) || (third.contains(pkg) && launchable.contains(pkg)))) continue;
        idleCands.add(new String[] { pkg, usedPkgs.contains(pkg) ? L.t("k057") : L.t("k058") });
        if (idleCands.size() >= 12) break;
      }
    }

    // ---------------- наблюдения
    Long memTotal = mem.get("MemTotal"), memAvail = mem.get("MemAvailable");
    if (memTotal != null) memTotalMb = mb(memTotal);
    if (memTotal != null && memAvail != null && memTotal > 0) {
      long pct = Math.round(100.0 * memAvail / memTotal);
      if (memAvail < 400 * 1024 || pct < 10) obs.add(L.t("m321", mb(memAvail), mb(memTotal), pct));
    }
    if (uptimeSec > 14 * 86400) obs.add(L.t("m323", uptimeSec / 86400));
    if (uptimeSec > 0 && uptimeSec < 600) obs.add(L.t("m324"));
    if (dataPct >= 85) obs.add(L.t("m325", dataPct, mb(dataFree)));
    if ("1".equals(set.get("low_power"))) obs.add(L.t("m326"));
    int relMajor = 0;
    try { relMajor = Integer.parseInt(P("ro.build.version.release").split("\\.")[0]); } catch (NumberFormatException ignored) {}
    int[][] sdkRel = { { 23, 6 }, { 24, 7 }, { 25, 7 }, { 26, 8 }, { 27, 8 }, { 28, 9 }, { 29, 10 }, { 30, 11 }, { 31, 12 }, { 32, 12 }, { 33, 13 }, { 34, 14 }, { 35, 15 }, { 36, 16 } };
    for (int[] sr : sdkRel) if (sr[0] == sdk && relMajor > sr[1]) obs.add(L.t("k070", P("ro.build.version.release"), sr[1], sdk));
    if ("1".equals(G("global", "setting.duraspeed.enabled")) || "1".equals(G("system", "setting.duraspeed.enabled"))) obs.add(L.t("k071"));
    if (adbPersist.length() > 0) obs.add(L.t("k073", adbPersist));
    long gms = rssMb("com.google.android.gms");
    if (memTotal != null && memTotal < 2600 * 1024 && gms >= 250) obs.add(L.t("k074", gms));
    Map<String, String> tips = new HashMap<String, String>();
    for (String x : new String[] { "fyt", "teyes", "atoto" }) tips.put(x, "k081");
    tips.put("qf", "k082"); tips.put("reglink", "k083"); tips.put("mtc", "k084");
    for (String x : new String[] { "ts", "hcn", "nwd", "allwinner", "unknown" }) tips.put(x, "k085");
    if (tips.containsKey(platId)) obs.add(L.t("k080") + " " + L.t(tips.get(platId)));
    if (rootAdb) obs.add(L.t("k072"));
    if (Math.abs(timeDiffMin) >= 5) obs.add(L.t("k111", Math.abs(timeDiffMin), "1".equals(autoTime) ? L.t("k112") : L.t("k113")));
    else if ("0".equals(autoTime)) obs.add(L.t("k114"));
    if ("0".equals(locMode)) obs.add(L.t("k115"));
    if (rssi < 0 && rssi <= -78) obs.add(L.t("k116", rssi));
    if ("1".equals(set.get("finish_act"))) obs.add(L.t("m331"));
    String bl = set.get("bg_limit");
    if (bl.length() > 0 && !bl.equals("null") && !bl.equals("-1")) obs.add(L.t("m332", bl));
    if ("0".equals(set.get("verifier"))) obs.add(L.t("m333"));
    for (Map.Entry<String, Integer> e : crashes.entrySet()) if (e.getValue() >= 2) obs.add(L.t("m337", e.getKey(), e.getValue()));
    if (dnsBroken) obs.add(L.t("m339"));
    List<String> warnPk = new ArrayList<String>();
    for (Susp s : susp) if (s.level.equals("warn")) warnPk.add(s.pkg);
    if (!warnPk.isEmpty()) obs.add(L.t("a140", join(warnPk, ", ")));
    if (kids) obs.add(L.t("m342"));
    String aw = set.get("anim_w");
    if (aw.length() == 0 || aw.equals("null") || aw.equals("1") || aw.equals("1.0")) obs.add(L.t("m345"));

    // ---------------- план
    if (!diagOnly) {
      if (!(aw.equals("0.5") || aw.equals("0.5f") || aw.equals("0") || aw.equals("0.0")))
        add("anim", "", L.t("m174", aw.length() > 0 && !aw.equals("null") ? aw : "1x"), true, L.t("m175"), "");
      if (!"hostname".equals(set.get("dns_mode"))) {
        if (kids) { add("dns", "family.adguard-dns.com", L.t("m176"), false, L.t("m175"), ""); add("dns", "dns.adguard-dns.com", L.t("m177"), false, L.t("m175"), ""); }
        else { add("dns", "dns.adguard-dns.com", L.t("m177"), false, L.t("m175"), ""); add("dns", "family.adguard-dns.com", L.t("m176"), false, L.t("m175"), ""); }
      }
      String ct = L.t("m178") + (cacheMb > 0 ? L.t("m179", cacheMb) : "") + L.t("m180");
      add("cache", "", ct, dataPct >= 85, L.t("m175"), "");
      for (Susp s : suspOk) add("third", s.pkg, L.t("m181", s.pkg, s.why), false, L.t("m182"), "");
      Map<String, String> grp = new HashMap<String, String>();
      grp.put("auto", L.t("m186")); grp.put("base", L.t("m187")); grp.put("ask", L.t("m188"));
      for (Cand c : candOk) {
        String txt = L.t("m183", c.pkg);
        if (c.note != null && c.note.length() > 0) txt += " — " + c.note;
        if (c.mbv > 0) txt += L.t("m184", c.mbv);
        if (c.ask.length() > 0) txt += "  (" + c.ask + ")";
        if (c.tier.equals("base")) txt += L.t("a141");
        add("disable", c.pkg, txt, c.tier.equals("auto"), grp.get(c.tier), c.tier);
      }
      for (String b : bgCands) { long m = rssMb(b); add("bg", b, L.t("m190", b, m > 0 ? L.t("m189", m) : ""), true, L.t("m191"), ""); }
      for (String[] x : idleCands) add("idle", x[0], L.t("k047", x[0], x[1]), true, L.t("k048"), "");
    }

    // ---------------- отчёт
    report.add(L.t("a150", VERSION));
    report.add(new SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.US).format(new Date()));
    report.add(L.t("m353", P("ro.product.brand"), model, P("ro.product.device"), P("ro.product.manufacturer")));
    report.add(L.t("m355", P("ro.build.version.release"), sdk, P("ro.build.version.security_patch")));
    report.add(L.t("m358", P("ro.build.display.id")));
    report.add(L.t("m361", P("ro.hardware"), P("ro.board.platform"), P("ro.product.cpu.abilist")));
    report.add(L.t("k090", platName.length() > 0 ? platName : L.t("k091"), chip).trim());
    for (String k : new String[] { "ro.fyt.platform", "ro.build.fytmanufacturer", "ro.fyt.uiid", "ro.fota.platform", "ro.fyt.mcu_type", "ro.qf.platform", "persist.sys.qf.launcher", "persist.sys.hcnport" })
      if (P(k).length() > 0) report.add("    " + k + " = " + P(k));
    if (!core.isEmpty()) report.add(L.t("k092", join(core, ", ")).trim());
    if (memTotal != null) report.add(L.t("m377", mb(memTotal), mb(memAvail == null ? 0 : memAvail)).trim());
    report.add(L.t("m380", mb(dataTotal), mb(dataUsed), dataPct, mb(dataFree), cacheMb).trim());
    report.add(L.t("m388", all.size(), sys.size(), third.size(), disabled.size(), preUninst.size()).trim().replaceAll("^\\d+\\.\\s*", ""));
    if (!disabled.isEmpty()) report.add(L.t("m390") + join(new ArrayList<String>(new TreeSet<String>(disabled)), ", "));
    before = snap();
  }

  private void add(String kind, String pkg, String text, boolean on, String group, String tier) { items.add(new Item(kind, pkg, text, on, group, tier)); }

  static List<String> jsonArr(String t, String name) {
    List<String> r = new ArrayList<String>();
    Matcher m = Pattern.compile("(?m)^" + Pattern.quote(name) + ": \\[(.*)\\]").matcher(t);
    if (m.find()) for (String x : m.group(1).split(",")) r.add(x.trim().replaceAll("^\"|\"$", ""));
    return r;
  }

  List<String> queryOp(String op) throws IOException {
    List<String> r = new ArrayList<String>();
    for (String l : S("cmd appops query-op --user 0 " + op + " allow").split("\n")) { String x = l.trim(); if (x.matches("^[A-Za-z0-9_.]+$") && x.contains(".")) r.add(x); }
    return r;
  }

  String homeComp() throws IOException {
    String c = "";
    Matcher m = Pattern.compile("(?m)^\\s*([A-Za-z0-9_.]+/[A-Za-z0-9_.$]+)\\s*$").matcher(S("cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.HOME"));
    while (m.find()) c = m.group(1);
    return c;
  }

  static boolean homeBad(String c) { return c.length() == 0 || c.startsWith("android/") || c.contains("FallbackHome") || c.contains("ResolverActivity"); }

  Set<String> idleSet() throws IOException {
    Set<String> s = new HashSet<String>();
    Matcher m = Pattern.compile("(?m)^\\s*(user|system|system-excidle),([A-Za-z0-9_.]+),").matcher(S("dumpsys deviceidle whitelist"));
    while (m.find()) s.add(m.group(2));
    return s;
  }

  static String join(List<String> l, String sep) {
    StringBuilder sb = new StringBuilder();
    for (String x : l) { if (sb.length() > 0) sb.append(sep); sb.append(x); }
    return sb.toString();
  }

  // ---------------------------------------------------------------- здоровье магнитолы (Get-Health / Compare-Health)

  static final class Health { String model = "", home = ""; boolean homeBad, settings, ime, sysUi; List<String> core = new ArrayList<String>(); }

  Health health() throws IOException {
    Health h = new Health();
    h.model = S("getprop ro.product.model").trim();
    h.home = homeComp();
    h.homeBad = homeBad(h.home);
    h.settings = Pattern.compile("[A-Za-z0-9_.]+/[A-Za-z0-9_.$]+").matcher(S("cmd package resolve-activity --brief -a android.settings.SETTINGS -c android.intent.category.DEFAULT")).find();
    String imePkg = G("secure", "default_input_method").split("/")[0];
    Set<String> dis = pkgList(S("pm list packages -d"));
    h.ime = imePkg.length() == 0 || imePkg.equals("null") || !dis.contains(imePkg);
    h.sysUi = S("pidof com.android.systemui").trim().length() > 0;
    for (String c : core) if (S("pidof " + c).trim().length() > 0) h.core.add(c);
    return h;
  }

  List<String> compare(Health base, Health now) {
    List<String> p = new ArrayList<String>();
    if (now.model.length() == 0) p.add(L.t("m118"));
    if (now.homeBad && !base.homeBad) p.add(L.t("m119", now.home));
    if (base.settings && !now.settings) p.add(L.t("m120"));
    if (base.ime && !now.ime) p.add(L.t("m121"));
    if (base.sysUi && !now.sysUi) p.add(L.t("m122"));
    for (String c : base.core) if (!now.core.contains(c)) p.add(L.t("k040", c));
    return p;
  }

  // ---------------------------------------------------------------- изменения

  Journal j;

  void journal(Entry e) throws IOException { j.entries.add(e); j.save(); }

  static Entry e(String t, String pkg) { Entry x = new Entry(); x.t = t; x.pkg = pkg; return x; }

  boolean disablePkg(String pkg, boolean thirdParty) throws IOException {
    if (keepSet.contains(pkg) && !thirdParty) { say(L.t("m123", pkg), WARN); return false; }
    if (thirdParty && roleSet.contains(pkg)) { say(L.t("m123", pkg), WARN); return false; }
    if (!thirdParty) {
      if (isProtected(pkg)) { say(L.t("m124", pkg), WARN); return false; }
      if (third.contains(pkg)) { say(L.t("m125", pkg), WARN); return false; }
      if (usedPkgs.contains(pkg)) { say(L.t("m126", pkg), WARN); return false; }
    }
    String out = W("pm disable-user --user 0 " + pkg);
    boolean listed = pkgList(S("pm list packages -d")).contains(pkg);
    boolean said = out.contains("new state: disabled");
    if (listed || said) journal(e("disable", pkg));
    if (listed) { say(L.t("m127", pkg), OK); return true; }
    if (said) { say(L.t("m128", pkg), WARN); return true; }
    if (thirdParty) { say(L.t("m129", pkg, out), WARN); return false; }
    String out2 = W("pm uninstall -k --user 0 " + pkg);
    boolean gone = !pkgList(S("pm list packages")).contains(pkg);
    if (out2.contains("Success") || gone) {
      journal(e("uninstall", pkg));
      if (gone) { say(L.t("m130", pkg), OK); return true; }
      say(L.t("m131", pkg), WARN); return true;
    }
    say(L.t("m132", pkg, out, out2), WARN);
    return false;
  }

  void setGlobal(String key, String val) throws IOException {
    String old = G("global", key);
    if (old.equals(val)) return;
    W("settings put global " + key + " " + val);
    Entry x = e("setting", ""); x.key = key; x.old = old; x.nw = val;
    journal(x);
  }

  boolean setDns(String host, int waitSec) throws IOException {
    int start = j.entries.size();
    setGlobal("private_dns_specifier", host);
    setGlobal("private_dns_mode", "hostname");
    say(L.t("m138").trim(), INFO);
    sleep(waitSec * 1000L);
    if (S("dumpsys connectivity").contains("PRIVATE_DNS_BROKEN")) { say(L.t("m139", host), BAD); undo(start, null); return false; }
    say(L.t("m140", host), OK);
    return true;
  }

  String bgMode(String pkg) throws IOException {
    Matcher m = Pattern.compile("RUN_ANY_IN_BACKGROUND: (\\w+)").matcher(S("cmd appops get " + pkg + " RUN_ANY_IN_BACKGROUND"));
    return m.find() ? m.group(1) : "default";
  }

  boolean restrictBg(String pkg) throws IOException {
    if (keepSet.contains(pkg)) { say(L.t("m141", pkg), WARN); return false; }
    String old = bgMode(pkg);
    if (old.equals("ignore")) { say(L.t("m142", pkg), OK); return false; }
    W("cmd appops set " + pkg + " RUN_ANY_IN_BACKGROUND ignore");
    if (bgMode(pkg).equals("ignore")) { Entry x = e("appops", pkg); x.old = old; journal(x); say(L.t("m143", pkg), OK); return true; }
    say(L.t("m144", pkg), WARN);
    return false;
  }

  boolean addIdle(String pkg) throws IOException {
    if (idleSet().contains(pkg)) { say(L.t("k042", pkg), OK); return false; }
    W("dumpsys deviceidle whitelist +" + pkg);
    if (idleSet().contains(pkg)) { journal(e("idle", pkg)); say(L.t("k041", pkg), OK); return true; }
    say(L.t("k043", pkg), WARN);
    return false;
  }

  void clearCaches() throws IOException {
    long f1 = dataFree();
    W("pm trim-caches 999G", 300);
    sleep(3000);
    long f2 = dataFree();
    say(L.t("m145", Math.max(0, mb(f2 - f1)), mb(f2)), OK);
  }

  public long dnsWaitSec = 15;
  public long settleMs = 10000;

  static void sleep(long ms) { try { Thread.sleep(ms); } catch (InterruptedException e) { Thread.currentThread().interrupt(); } }

  /** Применить отмеченные пункты. Журнал пишется до первого изменения; после каждой партии из 5 пакетов — проверка магнитолы. */
  public Journal apply(List<Item> sel, Journal existing) throws IOException {
    // прошлые изменения этой магнитолы остаются в журнале: откат вернёт всё
    j = existing;
    j.kit = "car-kit mobile " + VERSION; j.unit = unitId; j.model = model; j.fingerprint = fingerprint;
    if (j.created.length() == 0 || j.entries.isEmpty()) j.created = new SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.US).format(new Date());
    j.save();
    Health base = health();
    if (base.homeBad) say(L.t("m209", base.home), WARN);
    boolean stopped = false;
    for (Item it : sel) if (it.kind.equals("anim")) { for (String k : new String[] { "window_animation_scale", "transition_animation_scale", "animator_duration_scale" }) setGlobal(k, "0.5"); say(L.t("m137", "0.5"), OK); break; }
    Item dns = null;
    for (Item it : sel) if (it.kind.equals("dns") && (dns == null || it.pkg.startsWith("family"))) dns = it;
    if (dns != null) setDns(dns.pkg, (int) dnsWaitSec);
    for (Item it : sel) if (it.kind.equals("cache")) { clearCaches(); break; }
    List<Item> pk = new ArrayList<Item>();
    for (Item it : sel) if (it.kind.equals("disable") || it.kind.equals("third")) pk.add(it);
    for (int i = 0; i < pk.size(); i += 5) {
      int start = j.entries.size();
      for (int k = i; k < Math.min(i + 5, pk.size()); k++) disablePkg(pk.get(k).pkg, pk.get(k).kind.equals("third"));
      if (log != null) log.progress(Math.min(i + 5, pk.size()), pk.size());
      List<String> prob = compare(base, health());
      if (!prob.isEmpty()) {
        say(L.t("m211") + join(prob, "; ") + L.t("m212"), BAD);
        undo(start, null);
        stopped = true;
        break;
      }
      say(L.t("m213", i / 5 + 1), OK);
    }
    if (!stopped) {
      for (Item it : sel) if (it.kind.equals("bg")) restrictBg(it.pkg);
      for (Item it : sel) if (it.kind.equals("idle")) addIdle(it.pkg);
    }
    if (j.entries.isEmpty()) say(L.t("m214"), WARN);
    sleep(settleMs);
    after = snap();
    return j;
  }

  // ---------------------------------------------------------------- откат

  public String describe(Entry x) {
    String t;
    if (x.t.equals("disable")) t = L.t("m232", x.pkg);
    else if (x.t.equals("uninstall")) t = L.t("m233", x.pkg);
    else if (x.t.equals("setting")) t = L.t("m234", x.key, x.old.length() > 0 && !x.old.equals("null") ? x.old : L.t("m146"));
    else if (x.t.equals("appops")) t = L.t("m235", x.pkg);
    else if (x.t.equals("idle")) t = L.t("k045", x.pkg);
    else t = x.t + " " + x.pkg;
    return t.trim().replaceAll("^-\\s*", "");
  }

  void undoEntry(Entry x) throws IOException {
    if (x.t.equals("disable")) {
      String out = W("pm enable --user 0 " + x.pkg);
      if (!pkgList(S("pm list packages -d")).contains(x.pkg)) say(L.t("m133", x.pkg), OK); else say(L.t("m134", x.pkg, out), BAD);
    } else if (x.t.equals("uninstall")) {
      String out = W("cmd package install-existing --user 0 " + x.pkg);
      if (!pkgList(S("pm list packages")).contains(x.pkg)) out += " / " + W("pm install-existing --user 0 " + x.pkg);
      if (pkgList(S("pm list packages")).contains(x.pkg)) say(L.t("m135", x.pkg), OK); else say(L.t("m136", x.pkg, out), BAD);
    } else if (x.t.equals("setting")) {
      if (x.old.length() == 0 || x.old.equals("null")) W("settings delete global " + x.key); else W("settings put global " + x.key + " " + x.old);
      say(L.t("m147", x.key, x.old.length() > 0 && !x.old.equals("null") ? x.old : L.t("m146")), OK);
    } else if (x.t.equals("idle")) {
      W("dumpsys deviceidle whitelist -" + x.pkg);
      say(L.t("k044", x.pkg), OK);
    } else if (x.t.equals("appops")) {
      String old = Arrays.asList("allow", "ignore", "default").contains(x.old) ? x.old : "default";
      W("cmd appops set " + x.pkg + " RUN_ANY_IN_BACKGROUND " + old);
      say(L.t("m148", x.pkg), OK);
    }
  }

  /** Откатить записи журнала с номера from (с конца); only — только эти номера (выборочный откат). */
  void undo(int from, Set<Integer> only) throws IOException {
    for (int i = j.entries.size() - 1; i >= from; i--) {
      if (only != null && !only.contains(i)) continue;
      undoEntry(j.entries.get(i));
      j.entries.remove(i);
      j.save();
    }
  }

  public void rollback(Journal jr, Set<Integer> only) throws IOException {
    j = jr;
    undo(0, only);
    after = snap();
    say(L.t("m219") + homeComp(), OK);
  }

  /** Текст отчёта для отправки (WhatsApp / Telegram / почта). */
  public String reportText(Journal jr) {
    StringBuilder sb = new StringBuilder();
    for (String l : report) sb.append(l).append('\n');
    if (!obs.isEmpty()) { sb.append('\n').append(L.t("a151")).append('\n'); for (String o : obs) sb.append("- ").append(o).append('\n'); }
    if (!notes.isEmpty()) { sb.append('\n'); for (String n : notes) sb.append("* ").append(n).append('\n'); }
    if (!opt.isEmpty()) { sb.append('\n').append(L.t("a152")).append('\n'); for (String o : opt) sb.append("  ").append(o).append('\n'); }
    if (before != null && after != null) sb.append('\n').append(L.t("a153", before.memAvailMb, after.memAvailMb, before.procs, after.procs, before.disabled, after.disabled)).append('\n');
    if (jr != null && !jr.entries.isEmpty()) { sb.append('\n').append(L.t("a154", jr.entries.size())).append('\n'); for (Entry x : jr.entries) sb.append("  ").append(describe(x)).append('\n'); }
    return sb.toString();
  }
}

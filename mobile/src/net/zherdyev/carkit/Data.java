package net.zherdyev.carkit;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/** База пакетов набора: data/uad.tsv (UAD-ng), data/ru.tsv, data/car.tsv, data/notes/<язык>.tsv. */
public final class Data {
  public static final class Uad { public String list, removal, name, neededby; }

  public final Map<String, Uad> uad = new HashMap<String, Uad>();
  public final Map<String, String> carLevel = new HashMap<String, String>();
  public final Map<String, String> ruLevel = new HashMap<String, String>();
  /** Пояснение к пакету на языке мастера (как $ruNote в наборе). */
  public final Map<String, String> note = new HashMap<String, String>();

  public Data(Lang.Source src, String lang) throws IOException {
    for (String[] f : rows(src, "uad.tsv")) {
      if (f.length < 3) continue;
      Uad u = new Uad();
      u.list = f[1]; u.removal = f[2]; u.name = f.length > 3 ? f[3] : ""; u.neededby = f.length > 4 ? f[4] : "";
      uad.put(f[0], u);
    }
    for (String[] f : rows(src, "ru.tsv")) {
      if (f.length < 2) continue;
      ruLevel.put(f[0], f[1]);
      if (f.length > 2 && f[2].length() > 0) note.put(f[0], f[2]);
    }
    if (!lang.equals("ru")) {
      String[][] n = null;
      try { n = rows(src, "notes/" + lang + ".tsv"); } catch (IOException e) { try { n = rows(src, "notes/en.tsv"); } catch (IOException e2) { n = new String[0][]; } }
      for (String[] f : n) if (f.length > 1 && f[1].length() > 0) note.put(f[0], f[1]);
    }
    String[][] car = rows(src, "car.tsv", true);
    String[] head = car[0];
    int col = -1, en = -1, ru = -1;
    for (int i = 0; i < head.length; i++) { if (head[i].equals(lang)) col = i; if (head[i].equals("en")) en = i; if (head[i].equals("ru")) ru = i; }
    for (int r = 1; r < car.length; r++) {
      String[] f = car[r];
      if (f.length < 2) continue;
      carLevel.put(f[0], f[1]);
      String t = cell(f, col);
      if (t.length() == 0) t = cell(f, en);
      if (t.length() == 0) t = cell(f, ru);
      if (t.length() > 0) note.put(f[0], t);
    }
  }

  private static String cell(String[] f, int i) { return i >= 0 && i < f.length ? f[i] : ""; }

  private static String[][] rows(Lang.Source src, String name) throws IOException { String[][] r = rows(src, name, false); return r; }

  private static String[][] rows(Lang.Source src, String name, boolean keepHead) throws IOException {
    String t = new String(AdbKey.readAll(src.open(name)), "UTF-8");
    if (t.startsWith("﻿")) t = t.substring(1);
    String[] lines = t.replace("\r", "").split("\n");
    java.util.ArrayList<String[]> r = new java.util.ArrayList<String[]>();
    for (int i = keepHead ? 0 : 1; i < lines.length; i++) {
      if (lines[i].length() == 0) continue;
      r.add(unq(lines[i].split("\t", -1)));
    }
    return r.toArray(new String[0][]);
  }

  // Import-Csv снимает кавычки вокруг поля — делаем так же
  private static String[] unq(String[] f) {
    for (int i = 0; i < f.length; i++) {
      String s = f[i];
      if (s.length() >= 2 && s.startsWith("\"") && s.endsWith("\"")) f[i] = s.substring(1, s.length() - 1).replace("\"\"", "\"");
    }
    return f;
  }

  /** Подпись пакета: наше пояснение -> имя из UAD -> сам пакет. */
  public String label(String pkg) {
    String n = note.get(pkg);
    if (n == null && uad.get(pkg) != null) n = uad.get(pkg).name;
    return n == null || n.length() == 0 ? pkg : pkg + " (" + n + ")";
  }
}

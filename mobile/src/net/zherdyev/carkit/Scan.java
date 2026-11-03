package net.zherdyev.carkit;

import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.InterfaceAddress;
import java.net.NetworkInterface;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Enumeration;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

/** Поиск магнитол: открытый порт ADB 5555 в локальных сетях телефона (точка доступа, Wi-Fi). */
public final class Scan {
  private Scan() {}

  public static final class Net { public String iface, own, prefix; public boolean hotspot; }

  /** Сети /24 телефона: сначала точка доступа (ap*, swlan*, softap*, wlan1...), сотовые и VPN пропускаем. */
  public static List<Net> nets() {
    List<Net> r = new ArrayList<Net>();
    try {
      Enumeration<NetworkInterface> e = NetworkInterface.getNetworkInterfaces();
      if (e == null) return r;
      for (NetworkInterface ni : Collections.list(e)) {
        String name = ni.getName() == null ? "" : ni.getName().toLowerCase(java.util.Locale.US);
        if (!ni.isUp() || ni.isLoopback()) continue;
        if (name.matches("^(rmnet|ccmni|pdp|clat|v4-|tun|ppp|dummy|ip6|sit|p2p-dev|ifb|lo|bond|seth|r_rmnet|wwan|usb_rmnet).*")) continue;
        for (InterfaceAddress ia : ni.getInterfaceAddresses()) {
          InetAddress a = ia.getAddress();
          if (!(a instanceof Inet4Address) || a.isLoopbackAddress() || a.isLinkLocalAddress()) continue;
          if (!a.isSiteLocalAddress()) continue;
          byte[] b = a.getAddress();
          Net n = new Net();
          n.iface = name;
          n.own = a.getHostAddress();
          n.prefix = (b[0] & 0xff) + "." + (b[1] & 0xff) + "." + (b[2] & 0xff) + ".";
          n.hotspot = name.matches("^(ap|swlan|softap|wlan1|wlan2|wifi_ap|rndis|eth|bt-pan).*");
          boolean dup = false;
          for (Net x : r) if (x.prefix.equals(n.prefix)) dup = true;
          if (!dup) { if (n.hotspot) r.add(0, n); else r.add(n); }
        }
      }
    } catch (Exception ignored) {}
    return r;
  }

  /** Перебор .1–.254 сети на порт 5555 (64 потока, ~5 с на /24). */
  public static List<String> find(Net n, final int port) {
    final List<String> found = Collections.synchronizedList(new ArrayList<String>());
    ExecutorService ex = Executors.newFixedThreadPool(64);
    for (int i = 1; i < 255; i++) {
      final String ip = n.prefix + i;
      if (ip.equals(n.own)) continue;
      ex.execute(new Runnable() {
        public void run() {
          Socket s = new Socket();
          try { s.connect(new InetSocketAddress(ip, port), 700); found.add(ip); }
          catch (Exception ignored) {}
          finally { try { s.close(); } catch (Exception ignored) {} }
        }
      });
    }
    ex.shutdown();
    try { ex.awaitTermination(30, TimeUnit.SECONDS); } catch (InterruptedException ignored) {}
    List<String> r = new ArrayList<String>(found);
    Collections.sort(r, new java.util.Comparator<String>() {
      public int compare(String a, String b) { return Integer.parseInt(a.substring(a.lastIndexOf('.') + 1)) - Integer.parseInt(b.substring(b.lastIndexOf('.') + 1)); }
    });
    return r;
  }

  /** «192.168.43.120», «192.168.43.120:5555» -> {host, port}; null если это не адрес. */
  public static String[] parseAddr(String s) {
    s = s.trim();
    String host = s; int port = 5555;
    int c = s.lastIndexOf(':');
    if (c > 0) { host = s.substring(0, c); try { port = Integer.parseInt(s.substring(c + 1)); } catch (NumberFormatException e) { return null; } }
    if (!host.matches("^\\d{1,3}(\\.\\d{1,3}){3}$") && !host.matches("^[A-Za-z0-9.-]+$")) return null;
    if (host.matches("^\\d{1,3}(\\.\\d{1,3}){3}$")) for (String p : host.split("\\.")) if (Integer.parseInt(p) > 255) return null;
    if (port < 1 || port > 65535) return null;
    return new String[] { host, String.valueOf(port) };
  }
}

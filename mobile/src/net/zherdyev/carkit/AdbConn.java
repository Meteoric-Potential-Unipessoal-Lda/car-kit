package net.zherdyev.carkit;

import java.io.ByteArrayOutputStream;
import java.io.Closeable;
import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketTimeoutException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

/**
 * Клиент протокола ADB по TCP (как «adb connect IP:5555»): CNXN, AUTH (ключ RSA телефона), OPEN shell:.
 * Беспроводная отладка Android 11+ (TLS после сопряжения) не поддерживается — нужен обычный порт 5555.
 */
public final class AdbConn implements Sh, Closeable {
  static final int CNXN = 0x4e584e43, AUTH = 0x48545541, OPEN = 0x4e45504f, OKAY = 0x59414b4f, CLSE = 0x45534c43, WRTE = 0x45545257, STLS = 0x534c5453;
  static final int VERSION = 0x01000000; // старая версия + контрольная сумма: понимают и Android 4, и новые
  static final int MAXDATA = 256 * 1024;

  public interface AuthListener { void onAllowNeeded(); }

  /** Магнитола требует TLS (это порт беспроводной отладки, а не 5555). */
  public static final class TlsRequired extends IOException { TlsRequired() { super("TLS"); } }
  /** Ключ не приняли: на экране магнитолы не нажали «Разрешить». */
  public static final class NotAllowed extends IOException { NotAllowed() { super("not allowed"); } }

  private final Socket sock;
  private final DataInputStream in;
  private final OutputStream out;
  private int maxData = 4096;
  private int nextId = 1;
  public String banner = "";
  public final String addr;

  private AdbConn(Socket s, String addr) throws IOException {
    sock = s;
    this.addr = addr;
    in = new DataInputStream(new java.io.BufferedInputStream(s.getInputStream(), 65536));
    out = s.getOutputStream();
  }

  public static AdbConn connect(String host, int port, AdbKey key, int allowWaitSec, AuthListener l) throws IOException {
    Socket s = new Socket();
    s.setTcpNoDelay(true);
    s.connect(new InetSocketAddress(host, port), 5000);
    AdbConn c = new AdbConn(s, host + ":" + port);
    try {
      c.handshake(key, allowWaitSec, l);
      return c;
    } catch (IOException e) { c.close(); throw e; }
  }

  private void handshake(AdbKey key, int allowWaitSec, AuthListener l) throws IOException {
    sock.setSoTimeout(10000);
    send(CNXN, VERSION, MAXDATA, "host::car-kit\0".getBytes("UTF-8"));
    boolean sentSig = false, sentPub = false;
    while (true) {
      Msg m;
      try { m = read(); }
      catch (SocketTimeoutException e) { if (sentPub) throw new NotAllowed(); throw e; }
      if (m.cmd == STLS) throw new TlsRequired();
      if (m.cmd == CNXN) {
        maxData = Math.max(1024, Math.min(m.arg1, MAXDATA));
        banner = new String(m.data, "UTF-8").replace("\0", "");
        sock.setSoTimeout(0);
        return;
      }
      if (m.cmd == AUTH && m.arg0 == 1) {
        if (!sentSig) {
          try { send(AUTH, 2, 0, key.sign(m.data)); } catch (java.security.GeneralSecurityException e) { throw new IOException(e.toString()); }
          sentSig = true;
        } else if (!sentPub) {
          send(AUTH, 3, 0, (key.adbPublicKey("car-kit@phone") + "\0").getBytes("UTF-8"));
          sentPub = true;
          if (l != null) l.onAllowNeeded();
          sock.setSoTimeout(Math.max(5, allowWaitSec) * 1000);
        } else throw new NotAllowed();
      }
    }
  }

  /** Команда в shell магнитолы; вывод (stdout+stderr, без \r). По таймауту в конце — "TIMEOUT". */
  @Override
  public synchronized String sh(String cmd, int timeoutSec) throws IOException {
    int id = nextId++;
    send(OPEN, id, 0, ("shell:" + cmd + "\0").getBytes("UTF-8"));
    ByteArrayOutputStream buf = new ByteArrayOutputStream();
    int remote = 0;
    long deadline = System.currentTimeMillis() + Math.max(1, timeoutSec) * 1000L;
    while (true) {
      long left = deadline - System.currentTimeMillis();
      if (left <= 0) return timeout(id, remote, buf);
      sock.setSoTimeout((int) Math.max(200, left));
      Msg m;
      try { m = read(); } catch (SocketTimeoutException e) { return timeout(id, remote, buf); }
      if (m.arg1 != id) {
        // хвосты прошлых команд (после таймаута): подтверждаем и закрываем
        if (m.cmd == WRTE) { send(OKAY, m.arg1, m.arg0, null); send(CLSE, m.arg1, m.arg0, null); }
        continue;
      }
      if (m.cmd == OKAY) { remote = m.arg0; continue; }
      if (m.cmd == WRTE) { buf.write(m.data); remote = m.arg0; send(OKAY, id, m.arg0, null); continue; }
      if (m.cmd == CLSE) { if (remote != 0) send(CLSE, id, remote, null); break; }
    }
    return new String(buf.toByteArray(), "UTF-8").replace("\r", "");
  }

  private String timeout(int id, int remote, ByteArrayOutputStream buf) throws IOException {
    if (remote != 0) send(CLSE, id, remote, null);
    return new String(buf.toByteArray(), "UTF-8").replace("\r", "") + "\nTIMEOUT";
  }

  private static final class Msg { int cmd, arg0, arg1; byte[] data; }

  private Msg read() throws IOException {
    byte[] h = new byte[24];
    in.readFully(h);
    ByteBuffer b = ByteBuffer.wrap(h).order(ByteOrder.LITTLE_ENDIAN);
    Msg m = new Msg();
    m.cmd = b.getInt(); m.arg0 = b.getInt(); m.arg1 = b.getInt();
    int len = b.getInt();
    b.getInt(); // контрольная сумма
    int magic = b.getInt();
    if (magic != (m.cmd ^ 0xffffffff)) throw new IOException("bad ADB packet");
    if (len < 0 || len > 16 * 1024 * 1024) throw new IOException("bad ADB length " + len);
    m.data = new byte[len];
    in.readFully(m.data);
    return m;
  }

  private void send(int cmd, int a0, int a1, byte[] data) throws IOException {
    if (data == null) data = new byte[0];
    int off = 0;
    // WRTE больше maxData не бывает: мы шлём только короткие OPEN/AUTH/CNXN
    ByteBuffer b = ByteBuffer.allocate(24 + data.length).order(ByteOrder.LITTLE_ENDIAN);
    int sum = 0;
    for (byte x : data) sum += x & 0xff;
    b.putInt(cmd).putInt(a0).putInt(a1).putInt(data.length).putInt(sum).putInt(cmd ^ 0xffffffff);
    b.put(data, off, data.length);
    out.write(b.array());
    out.flush();
  }

  public int maxData() { return maxData; }

  @Override
  public void close() { try { sock.close(); } catch (IOException ignored) {} }

  static String readStream(InputStream in) throws IOException { return new String(AdbKey.readAll(in), "UTF-8"); }
}

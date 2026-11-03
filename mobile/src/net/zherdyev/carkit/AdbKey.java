package net.zherdyev.carkit;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.math.BigInteger;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.security.GeneralSecurityException;
import java.security.KeyFactory;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;
import java.security.interfaces.RSAPrivateCrtKey;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.RSAPublicKeySpec;
import java.security.interfaces.RSAPublicKey;

/** Ключ ADB телефона: RSA-2048, хранится в папке приложения; публичная часть — в формате adb (adbkey.pub). */
public final class AdbKey {
  final RSAPrivateCrtKey priv;
  final RSAPublicKey pub;

  private AdbKey(RSAPrivateCrtKey priv) throws GeneralSecurityException {
    this.priv = priv;
    this.pub = (RSAPublicKey) KeyFactory.getInstance("RSA").generatePublic(new RSAPublicKeySpec(priv.getModulus(), priv.getPublicExponent()));
  }

  /** Ключ из файла adbkey (PKCS#8: PEM «BEGIN PRIVATE KEY» или DER); нет файла — создаёт новый. */
  public static AdbKey loadOrCreate(File f) throws IOException, GeneralSecurityException {
    if (f.isFile() && f.length() > 0) return load(f);
    KeyPairGenerator g = KeyPairGenerator.getInstance("RSA");
    g.initialize(2048);
    KeyPair kp = g.generateKeyPair();
    byte[] der = kp.getPrivate().getEncoded();
    File tmp = new File(f.getPath() + ".tmp");
    FileOutputStream o = new FileOutputStream(tmp);
    try { o.write(pem(der).getBytes("US-ASCII")); } finally { o.close(); }
    if (!tmp.renameTo(f)) throw new IOException("cannot save " + f);
    return new AdbKey((RSAPrivateCrtKey) kp.getPrivate());
  }

  public static AdbKey load(File f) throws IOException, GeneralSecurityException {
    byte[] raw = readAll(new FileInputStream(f));
    String s = new String(raw, "US-ASCII");
    byte[] der = raw;
    if (s.contains("BEGIN")) {
      if (s.contains("BEGIN RSA PRIVATE KEY")) throw new GeneralSecurityException("PKCS#1 key is not supported, use PKCS#8");
      der = B64.decode(s.replaceAll("-----[^-]+-----", "").replaceAll("\\s", ""));
    }
    return new AdbKey((RSAPrivateCrtKey) KeyFactory.getInstance("RSA").generatePrivate(new PKCS8EncodedKeySpec(der)));
  }

  static String pem(byte[] der) {
    String b = B64.encode(der);
    StringBuilder sb = new StringBuilder("-----BEGIN PRIVATE KEY-----\n");
    for (int i = 0; i < b.length(); i += 64) sb.append(b, i, Math.min(b.length(), i + 64)).append('\n');
    return sb.append("-----END PRIVATE KEY-----\n").toString();
  }

  // adbd подписывает 20-байтовый токен как готовый SHA-1: RSA_sign(NID_sha1, token)
  private static final byte[] SHA1_PREFIX = { 0x30, 0x21, 0x30, 0x09, 0x06, 0x05, 0x2b, 0x0e, 0x03, 0x02, 0x1a, 0x05, 0x00, 0x04, 0x14 };

  public byte[] sign(byte[] token) throws GeneralSecurityException {
    byte[] m = new byte[SHA1_PREFIX.length + token.length];
    System.arraycopy(SHA1_PREFIX, 0, m, 0, SHA1_PREFIX.length);
    System.arraycopy(token, 0, m, SHA1_PREFIX.length, token.length);
    try {
      Signature s = Signature.getInstance("NONEwithRSA");
      s.initSign(priv);
      s.update(m);
      return s.sign();
    } catch (GeneralSecurityException e) {
      // запасной путь (старые Android): PKCS#1 v1.5 тип 1 вручную
      BigInteger n = priv.getModulus();
      int k = (n.bitLength() + 7) / 8;
      byte[] em = new byte[k];
      em[0] = 0; em[1] = 1;
      for (int i = 2; i < k - m.length - 1; i++) em[i] = (byte) 0xff;
      em[k - m.length - 1] = 0;
      System.arraycopy(m, 0, em, k - m.length, m.length);
      byte[] r = new BigInteger(1, em).modPow(priv.getPrivateExponent(), n).toByteArray();
      byte[] out = new byte[k];
      int off = r.length > k ? r.length - k : 0;
      System.arraycopy(r, off, out, k - (r.length - off), r.length - off);
      return out;
    }
  }

  /** Публичный ключ в формате adb: base64(RSAPublicKey из libcrypto_utils) + " имя". */
  public String adbPublicKey(String name) {
    BigInteger n = pub.getModulus();
    int words = 2048 / 32;
    ByteBuffer b = ByteBuffer.allocate(4 + 4 + words * 4 + words * 4 + 4).order(ByteOrder.LITTLE_ENDIAN);
    BigInteger r32 = BigInteger.ONE.shiftLeft(32);
    BigInteger n0inv = r32.subtract(n.mod(r32).modInverse(r32)).mod(r32);
    b.putInt(words);
    b.putInt(n0inv.intValue());
    putWords(b, n, words);
    putWords(b, BigInteger.ONE.shiftLeft(2048).pow(2).mod(n), words);
    b.putInt(pub.getPublicExponent().intValue());
    return B64.encode(b.array()) + " " + name;
  }

  private static void putWords(ByteBuffer b, BigInteger v, int words) {
    BigInteger mask = BigInteger.ONE.shiftLeft(32).subtract(BigInteger.ONE);
    for (int i = 0; i < words; i++) { b.putInt(v.and(mask).intValue()); v = v.shiftRight(32); }
  }

  /** Короткий отпечаток для экрана (как у adb: MD5 публичного ключа не показываем — хватит 8 знаков SHA-256). */
  public String fingerprint() {
    try {
      byte[] d = java.security.MessageDigest.getInstance("SHA-256").digest(pub.getEncoded());
      StringBuilder sb = new StringBuilder();
      for (int i = 0; i < 4; i++) sb.append(String.format("%02X", d[i] & 0xff));
      return sb.toString();
    } catch (GeneralSecurityException e) { return "?"; }
  }

  static byte[] readAll(InputStream in) throws IOException {
    try {
      ByteArrayOutputStream o = new ByteArrayOutputStream();
      byte[] buf = new byte[8192];
      int n;
      while ((n = in.read(buf)) > 0) o.write(buf, 0, n);
      return o.toByteArray();
    } finally { in.close(); }
  }
}

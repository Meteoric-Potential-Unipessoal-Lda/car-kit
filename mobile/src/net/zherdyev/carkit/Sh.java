package net.zherdyev.carkit;

import java.io.IOException;

/** Shell магнитолы: по сети через AdbConn, в тестах — через подставной adb. */
public interface Sh {
  String sh(String cmd, int timeoutSec) throws IOException;
}

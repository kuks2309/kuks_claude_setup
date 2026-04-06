#!/usr/bin/env python3
"""RoboteQ serial communication unit test (pyserial, 115200-8-N-1, \\r terminator)."""

import time
import unittest
import serial


class RoboteQSerialTest(unittest.TestCase):
    PORT = "/dev/ttyUSB0"
    BAUD = 115200
    TIMEOUT = 0.5
    DELAY = 0.02

    # -- helpers ----------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        cls.ser = serial.Serial(cls.PORT, cls.BAUD, timeout=cls.TIMEOUT)
        cls.results = []
        time.sleep(0.1)
        cls.ser.reset_input_buffer()

    @classmethod
    def tearDownClass(cls):
        cls.ser.close()
        print("\n" + "=" * 60)
        print(f"  RESULTS: {sum(r[1] for r in cls.results)}/{len(cls.results)} passed")
        print("=" * 60)
        for name, ok, detail in cls.results:
            mark = "PASS" if ok else "FAIL"
            print(f"  [{mark}] {name}: {detail}")
        print("=" * 60)

    def _send(self, cmd: str) -> str:
        self.ser.reset_input_buffer()
        self.ser.write(f"{cmd}\r".encode())
        time.sleep(self.DELAY)
        resp = b""
        while True:
            chunk = self.ser.read(256)
            if not chunk:
                break
            resp += chunk
        return resp.decode(errors="replace").strip()

    def _query(self, cmd: str) -> str:
        return self._send(cmd)

    def _assert_ack(self, cmd: str, tag: str):
        resp = self._send(cmd)
        ok = "+" in resp
        self.results.append((tag, ok, f"cmd={cmd!r} resp={resp!r}"))
        self.assertTrue(ok, f"{tag}: expected ACK(+), got {resp!r}")

    def _assert_value(self, cmd: str, tag: str, key: str = None):
        resp = self._query(cmd)
        if key:
            ok = resp.startswith(f"{key}=")
        else:
            ok = "=" in resp
        self.results.append((tag, ok, f"cmd={cmd!r} resp={resp!r}"))
        self.assertTrue(ok, f"{tag}: expected '=' response, got {resp!r}")
        return resp.split("=", 1)[-1] if ok else None

    # -- 1. connection / model ID ----------------------------------------
    def test_01_connection(self):
        self._assert_value("?TRN", "Connection(?TRN)", "TRN")

    # -- 2. voltage -------------------------------------------------------
    def test_02_voltage_battery(self):
        self._assert_value("?V 2", "Battery voltage(?V 2)", "V")

    def test_03_voltage_internal(self):
        self._assert_value("?V 1", "Internal voltage(?V 1)", "V")

    def test_04_voltage_5v(self):
        self._assert_value("?V 3", "5V output(?V 3)", "V")

    # -- 3. temperature ---------------------------------------------------
    def test_05_temp_mcu(self):
        self._assert_value("?T 1", "MCU temp(?T 1)", "T")

    def test_06_temp_heatsink(self):
        self._assert_value("?T 2", "Heatsink temp(?T 2)", "T")

    # -- 4. current -------------------------------------------------------
    def test_07_motor_current(self):
        self._assert_value("?A 1", "Motor1 current(?A 1)", "A")

    # -- 5. faults --------------------------------------------------------
    def test_08_fault_flags(self):
        self._assert_value("?FF", "Fault flags(?FF)", "FF")

    def test_09_fault_motor(self):
        self._assert_value("?FM 1", "Motor fault(?FM 1)", "FM")

    def test_10_fault_status(self):
        self._assert_value("?FS", "Status flags(?FS)", "FS")

    # -- 6. encoder -------------------------------------------------------
    def test_11_encoder_read(self):
        self._assert_value("?C 1", "Encoder read(?C 1)", "C")

    def test_12_encoder_reset(self):
        self._assert_ack("!C 1 0", "Encoder reset(!C 1 0)")

    # -- 7. VAR communication --------------------------------------------
    def test_13_var_write_read(self):
        self._assert_ack("!VAR 1 12345", "VAR write(!VAR 1 12345)")
        val = self._assert_value("?VAR 1", "VAR read(?VAR 1)", "VAR")
        if val is not None:
            ok = val.strip() == "12345"
            self.results.append(("VAR verify", ok, f"expected=12345 got={val!r}"))
            self.assertEqual(val.strip(), "12345", f"VAR mismatch: {val!r}")

    # -- 8. config (MXRPM) -----------------------------------------------
    def test_14_config_read_write(self):
        orig = self._assert_value("~MXRPM 1", "Config read(~MXRPM 1)", "MXRPM")
        if orig is None:
            self.skipTest("Cannot read MXRPM")
        orig = orig.strip()
        test_val = str(int(orig) + 1) if orig.isdigit() else "3000"
        self._assert_ack(f"^MXRPM 1 {test_val}", f"Config write(^MXRPM 1 {test_val})")
        readback = self._assert_value("~MXRPM 1", "Config readback(~MXRPM 1)", "MXRPM")
        if readback is not None:
            ok = readback.strip() == test_val
            self.results.append(("Config verify", ok, f"exp={test_val} got={readback!r}"))
        # restore
        self._assert_ack(f"^MXRPM 1 {orig}", f"Config restore(^MXRPM 1 {orig})")

    # -- 9. motor commands -----------------------------------------------
    def test_15_motor_stop(self):
        self._assert_ack("!MS 1", "Motor stop(!MS 1)")

    def test_16_emergency_stop(self):
        self._assert_ack("!EX", "Emergency stop(!EX)")

    def test_17_emergency_release(self):
        self._assert_ack("!MG", "E-stop release(!MG)")

    # -- 10. digital I/O --------------------------------------------------
    def test_18_digital_input(self):
        self._assert_value("?DI 1", "Digital input(?DI 1)", "DI")


if __name__ == "__main__":
    unittest.main(verbosity=2)

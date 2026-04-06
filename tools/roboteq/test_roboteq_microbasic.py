#!/usr/bin/env python3
"""
RoboteQ MicroBasic script verification tests.

VAR mapping:  VAR1:cmd-home  VAR2:cmd-target  VAR3:cmd-stop  VAR4:cmd-maxSpeed
  VAR5:fb-homing_done  VAR6:fb-homing_active  VAR10:fb-switchCase
  VAR11:cmd-mode(0=auto,1=manual)  VAR12:cmd-relPos
  VAR15:fb-status(1:moving 2:ok 3:fail 4:lowLim 5:upLim 7:homeFirst 8:fault)
  VAR16:fb-mode_status

State machine(VAR10): 0:idle 10:STOP 20-24:homing 30-32:pos_move 100-101:manual

Execution order:
  roundtrip -> homing -> position_move -> stop -> manual -> fault -> limit

Usage:  python3 test_roboteq_microbasic.py
        PORT=/dev/ttyACM0 python3 test_roboteq_microbasic.py
"""
import os, time, unittest
from typing import Optional, Set
import serial


class Conn:
    """Serial VAR read/write helper."""
    def __init__(self, port: str, baud: int = 115200):
        self.ser = serial.Serial(port, baud, timeout=0.5)
        time.sleep(0.1); self.ser.reset_input_buffer()

    def close(self):
        self.ser.close()

    def _send(self, cmd: str) -> str:
        self.ser.reset_input_buffer()
        self.ser.write(f"{cmd}\r".encode()); time.sleep(0.02)
        buf = b""
        while True:
            c = self.ser.read(256)
            if not c: break
            buf += c
        return buf.decode(errors="replace").strip()

    def vw(self, idx: int, val: int) -> bool:
        return "+" in self._send(f"!VAR {idx} {val}")

    def vr(self, idx: int) -> Optional[int]:
        r = self._send(f"?VAR {idx}")
        if "=" not in r: return None
        try: return int(r.split("=",1)[1].strip())
        except ValueError: return None

    def query(self, cmd: str) -> str:
        return self._send(cmd)

    def poll(self, idx: int, expect: int, timeout: float = 10.0) -> bool:
        dl = time.monotonic() + timeout
        while time.monotonic() < dl:
            if self.vr(idx) == expect: return True
            time.sleep(0.3)
        return False

    def poll_in(self, idx: int, vals: Set[int], timeout: float = 10.0) -> Optional[int]:
        dl = time.monotonic() + timeout
        while time.monotonic() < dl:
            v = self.vr(idx)
            if v in vals: return v
            time.sleep(0.3)
        return None

    def _parse(self, resp: str) -> Optional[int]:
        if "=" not in resp: return None
        try: return int(resp.split("=",1)[1].strip())
        except ValueError: return None


class TestMicroBasic(unittest.TestCase):
    """MicroBasic script state-machine verification (7 tests)."""
    PORT = os.environ.get("PORT", "/dev/ttyUSB0")

    @classmethod
    def setUpClass(cls):
        cls.c = Conn(cls.PORT)
        cls.log = []

    @classmethod
    def tearDownClass(cls):
        cls.c.vw(3, 1); time.sleep(2)
        cls.c.vw(3, 0); cls.c.vw(11, 0); cls.c.close()
        p = sum(r[1] for r in cls.log)
        print("\n" + "="*55)
        print(f"  MicroBasic: {p}/{len(cls.log)} passed")
        print("="*55)
        for n, ok, d in cls.log:
            print(f"  [{'PASS' if ok else 'FAIL'}] {n}: {d}")
        print("="*55)

    def _rec(self, n, ok, d):
        self.log.append((n, ok, d))

    # 1. VAR roundtrip
    def test_1_var_roundtrip(self):
        v = 2500
        ok_w = self.c.vw(4, v)
        self._rec("var_write", ok_w, f"VAR4={v}")
        self.assertTrue(ok_w, "VAR4 write failed")
        rb = self.c.vr(4)
        ok_r = rb == v
        self._rec("var_read", ok_r, f"exp={v} got={rb}")
        self.assertEqual(rb, v)
        self.c.vw(4, 0)

    # 2. Homing sequence (30s timeout)
    def test_2_homing_sequence(self):
        self.c.vw(11, 0); self.c.vw(3, 0); time.sleep(0.5)
        ok = self.c.vw(1, 1)
        self._rec("home_cmd", ok, "VAR1=1")
        self.assertTrue(ok)
        ok_a = self.c.poll(6, 1, timeout=5.0)
        self._rec("home_active", ok_a, f"VAR6={self.c.vr(6)}")
        ok_d = self.c.poll(5, 1, timeout=30.0)
        v5, v10 = self.c.vr(5), self.c.vr(10)
        self._rec("home_done", ok_d, f"VAR5={v5} sw={v10}")
        self.assertTrue(ok_d, f"Homing fail: VAR5={v5} sw={v10}")

    # 3. Position move
    def test_3_position_move(self):
        tgt = 50000
        if self.c.vr(5) != 1:
            self.skipTest("Homing not done")
        ok = self.c.vw(2, tgt)
        self._rec("pos_cmd", ok, f"VAR2={tgt}")
        self.assertTrue(ok)
        r = self.c.poll_in(15, {2, 3, 4, 5, 8}, timeout=20.0)
        v15 = self.c.vr(15)
        self._rec("pos_move", r == 2, f"VAR15={v15}")
        self.assertEqual(r, 2, f"Move fail: VAR15={v15}")

    # 4. Stop command
    def test_4_stop_command(self):
        ok = self.c.vw(3, 1)
        self._rec("stop_cmd", ok, "VAR3=1")
        self.assertTrue(ok)
        ok_s = self.c.poll(10, 0, timeout=5.0)
        v10 = self.c.vr(10)
        self._rec("stop_done", ok_s, f"VAR10={v10}")
        self.assertTrue(ok_s, f"Stop fail: sw={v10}")
        self.c.vw(3, 0)

    # 5. Manual mode
    def test_5_manual_mode(self):
        ok = self.c.vw(11, 1)
        self._rec("manual_cmd", ok, "VAR11=1")
        self.assertTrue(ok)
        ok_f = self.c.poll(16, 1, timeout=3.0)
        v16 = self.c.vr(16)
        self._rec("manual_fb", ok_f, f"VAR16={v16}")
        self.assertTrue(ok_f, f"Manual fail: VAR16={v16}")
        self.c.vw(11, 0); time.sleep(0.5)

    # 6. Fault detection
    def test_6_fault_detection(self):
        ff = self.c._parse(self.c.query("?FF 1"))
        if ff is None:
            self.skipTest("Cannot read FF")
        v15 = self.c.vr(15)
        if ff == 0:
            ok = v15 != 8
            self._rec("fault_none", ok, f"FF=0 VAR15={v15}")
            self.assertNotEqual(v15, 8)
        else:
            ok = v15 == 8
            self._rec("fault_det", ok, f"FF={ff} VAR15={v15}")
            self.assertEqual(v15, 8, f"Fault but VAR15={v15}")

    # 7. Limit switch
    def test_7_limit_switch(self):
        di1 = self.c._parse(self.c.query("?DI 1"))  # upper
        di2 = self.c._parse(self.c.query("?DI 2"))  # lower
        v15 = self.c.vr(15)
        if di1 is None or di2 is None:
            self.skipTest("Cannot read DI")
        d = f"DI1={di1} DI2={di2} VAR15={v15}"
        if di1 == 1:
            ok = v15 == 5
            self._rec("limit_up", ok, d)
            self.assertEqual(v15, 5, f"Upper limit but VAR15={v15}")
        elif di2 == 1:
            ok = v15 == 4
            self._rec("limit_low", ok, d)
            self.assertEqual(v15, 4, f"Lower limit but VAR15={v15}")
        else:
            self._rec("limit_none", True, d)


if __name__ == "__main__":
    unittest.main(verbosity=2)

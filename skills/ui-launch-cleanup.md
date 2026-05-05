---
name: ui-launch-cleanup
description: This skill should be used when implementing UI (PyQt5/PySide) that spawns and terminates ROS2 launch processes — covers Loc Stop / closeEvent / X 버튼 / Ctrl+C cleanup. Triggered by "ros2 launch UI 종료", "노드가 종료가 안됨", "child process orphan", "kill_all_node", or new GUI package adding `ros2 launch` entry.
user_invocable: true
trigger: ui-launch-cleanup
---

# UI Launch Cleanup 정공법 SSOT

> ROS2 GUI 패키지 (PyQt5/PySide) 에서 ros2 launch / run 자식 프로세스를 띄우고 정리하는 모든 작업의 표준 패턴.
>
> **배경**: 2026-05-05 acs_gui 세션에서 cleanup 회귀 7건 누적 (setsid → shutdown_all → kill_external → phase timeout → RuntimeError → kill_keywords → ros2 node list 정공법). 사용자 명시 7회 후 도달한 정공법을 영구 보존하여 모든 GUI 패키지에 재사용.

## 적용 대상

UI 에서 `ros2 launch` / `ros2 run` 자식 프로세스 띄우는 모든 패키지. 신규 GUI 패키지 추가 시 본 skill 따라 적용.

## 핵심 정공법 (사용자 명시 3단계)

```
1) ros2 node list 로 살아있는 노드 list 획득
2) yaml 의 expected_nodes 와 매칭 (gui 가 띄운 노드만)
3) pgrep -f __node:=<name> 으로 PID 검색 → kill -9 <pid>
```

원본 `~/T-Robot_nav_ros2_ws/kill_all_ros2.sh` 동등. 외부 ros2 작업 (다른 ws / 다른 터미널) 영향 없음.

## Instructions

신규 GUI 패키지에 cleanup 도입 또는 기존 패키지 cleanup 회귀 발생 시 다음 순서:

### Step 1: 원본 SSOT 라인별 read (CLAUDE.md "원본 전체 분석" 의무)

다음 3 파일 라인별 확인 후 작업 시작:

- 원본 closeEvent: `~/T-Robot_nav_ros2_ws/src/acs/acs/acs_gui_node.py:1688-1724` — signal disconnect + stop_process 패턴
- 원본 launch_manager: `~/T-Robot_nav_ros2_ws/src/Tools/tm_nav_tool/tm_nav_tool/launch_manager.py` — `launch_process` / `stop_process` / `kill_external_component`
- kill_all_node 정공법 source: `~/T-Robot_nav_ros2_ws/kill_all_ros2.sh` — ros2 node list → __node:= PID kill

### Step 2: yaml entry 의무 필드 추가

각 launch entry 마다:

```yaml
- name: <entry>
  cmd: ros2 launch <pkg> <file>.launch.py
  expected_nodes:        # 이 entry 가 띄우는 노드 모두 (ros2 node list 매칭용)
    - "/foo/icp_odometry"
    - "/foo/rtabmap"
    - "/map_server_loc"
  kill_keywords:         # 폴백 — expected_nodes 누락된 child 보강 (pkill -9 -f)
    - "rtabmap"
    - "map_server_loc"
```

### Step 3: process_manager 모듈 생성 (단일 책임)

`<pkg>/process_manager.py` 신규:

```python
from PyQt5.QtCore import QProcess
import subprocess
from typing import Callable, List, Optional

def launch(parent, cmd: List[str]) -> Optional[QProcess]:
    """단순 ros2 launch — setsid 불필요."""
    proc = QProcess(parent)
    proc.setProcessChannelMode(QProcess.MergedChannels)
    proc.start(cmd[0], cmd[1:])
    if not proc.waitForStarted(3000):
        return None
    return proc

def stop_by_node_list(expected_nodes: List[str],
                      log: Optional[Callable[[str], None]] = None) -> None:
    """3단계 정공법 — kill_all_ros2.sh 동등."""
    if not expected_nodes:
        return
    try:
        result = subprocess.run(['ros2', 'node', 'list'],
                                capture_output=True, text=True, timeout=5)
        active = [ln.strip() for ln in result.stdout.strip().splitlines() if ln.strip()]
    except Exception:
        return
    expected_set = set(expected_nodes)
    for node_full in active:
        if node_full not in expected_set:
            continue
        node_short = node_full.lstrip('/').split('/')[-1]
        try:
            pgrep = subprocess.run(['pgrep', '-f', f'__node:={node_short}'],
                                   capture_output=True, text=True, timeout=2)
            pids = [p for p in pgrep.stdout.split() if p.isdigit()]
        except Exception:
            pids = []
        for pid in pids:
            try:
                subprocess.run(['kill', '-9', pid], capture_output=True, timeout=2)
            except Exception:
                pass
            if log:
                log(f'[stop] kill -9 {pid} (node={node_full})')

def stop(kill_keywords: List[str],
         log: Optional[Callable[[str], None]] = None) -> None:
    """폴백 — expected_nodes 누락 child 정리."""
    if not kill_keywords:
        return
    for kw in kill_keywords:
        if not kw:
            continue
        try:
            subprocess.run(['pkill', '-9', '-f', kw], capture_output=True, timeout=2)
        except Exception:
            pass

def is_running(proc: Optional[QProcess]) -> bool:
    if proc is None:
        return False
    try:
        return proc.state() != QProcess.NotRunning
    except RuntimeError:
        return False
```

### Step 4: shutdown_all (closeEvent 진입점)

```python
def shutdown_all(self):
    """closeEvent / app quit / Ctrl+C 어떤 경로든 호출.

    1) signal disconnect — closeEvent 도중 callback RuntimeError 회피
    2) 정공법 — ros2 node list → expected_nodes 매칭 → __node:= PID kill -9
    3) 폴백 — kill_keywords pkill -9 -f
    """
    self._all_queue = []
    for e in self._entries.values():
        for proc_attr in ('proc', 'rviz_proc'):
            p = getattr(e, proc_attr, None)
            if p is None:
                continue
            for sig_name in ('readyReadStandardOutput', 'finished', 'errorOccurred'):
                sig = getattr(p, sig_name, None)
                if sig is not None:
                    try:
                        sig.disconnect()
                    except (RuntimeError, TypeError):
                        pass
    all_expected = []
    for e in self._entries.values():
        all_expected.extend(e.expected_nodes or [])
    if all_expected:
        pm.stop_by_node_list(all_expected)
    all_keywords = []
    for e in self._entries.values():
        all_keywords.extend(e.kill_keywords or [])
    if all_keywords:
        pm.stop(all_keywords)
```

### Step 5: main() finally — Ctrl+C / 예외 안전망

```python
def main():
    rclpy.init(...)
    win = MainWindow(...)
    try:
        rc = app.exec_()
    finally:
        try:
            win.launch_tab.shutdown_all()
        except Exception:
            pass
        # ... rclpy / executor shutdown
```

### Step 6: callback 안전망

widget 접근 callback 모두 RuntimeError 안전망:

```python
def _log(self, msg):
    try:
        self.txtLog.appendPlainText(msg)
    except RuntimeError:
        pass

def _reset_entry_ui(self, e):
    try:
        if e.lbl_status: e.lbl_status.setText(...)
        if e.btn_start: e.btn_start.setEnabled(...)
    except RuntimeError:
        pass
```

### Step 7: 검증 의무

#### Unit (pytest)

```python
def test_yaml_expected_nodes_loaded(tab):
    e = tab._entries['<entry>']
    assert '<expected node>' in e.expected_nodes

def test_pm_stop_by_node_list_calls_kill(monkeypatch):
    # ros2 node list / pgrep / kill 호출 인자 검증

def test_closeEvent_triggers_node_cleanup(qapp, monkeypatch):
    # AcsGuiWindow 인스턴스 + closeEvent 호출
    # → ros2 node list / kill -9 / pkill 호출 자동 검증
```

#### SmokeRun

`tools/verify/smoke_run/<pkg>_node.sh` — 격리 도메인 (`ROS_DOMAIN_ID=99`) + headless (`QT_QPA_PLATFORM=offscreen`).

#### Step A2 (Xvfb + xdotool e2e — 후속)

`tools/verify/smoke_run/<pkg>_e2e.sh` — Xvfb 가상 X 디스플레이 + xdotool button click + 단계별 ros2 node list 검증.

## 안티 패턴 (이번 세션 7건 회귀 — 절대 사용 금지)

| 안티 패턴 | 결과 | 정공법 |
|----------|------|-------|
| `setsid` + session kill (`pkill -s <pid>`) | 자기 launch 만, 외부 미적용 | `ros2 node list` 매칭 |
| 비동기 3-phase (`QTimer.singleShot(1500, ...)`) | timeout 짧으면 SIGTERM 강제 → exit=15 | 동기 `kill -9` 단순 |
| `signal.connect` 후 disconnect 안 함 | closeEvent → widget destroy → callback RuntimeError | shutdown_all 시작 시 모두 disconnect |
| pytest `subprocess.run` mock 만 검증 | 호출 인자만, 실제 cleanup 안 봄 | e2e (`test_closeEvent_triggers_node_cleanup`) |
| SmokeRun 이 시작만 검증 | 종료 / cleanup 부재 | Xvfb + xdotool e2e |
| 부분 패치 누적 (한 path 만 수정) | 다른 path 부정합 → 회귀 | process_manager 단일 책임 격리 |
| 원본 closeEvent 미참조 | 위반 #8 재발 (메타 패턴) | 원본 라인별 read |

## 새 GUI 패키지 추가 시 체크리스트

- [ ] 원본 SSOT 3 파일 라인별 read (Step 1)
- [ ] yaml entry 마다 `expected_nodes` 정의
- [ ] yaml entry 마다 `kill_keywords` 정의 (폴백)
- [ ] `process_manager.py` 모듈 추가 (Step 3 코드 그대로)
- [ ] `shutdown_all` 정공법 흐름 (Step 4)
- [ ] `main()` finally 에 `shutdown_all` 호출 (Step 5)
- [ ] `_log` / `_reset_entry_ui` callback 안전망 (Step 6)
- [ ] pytest e2e + SmokeRun (Step 7)
- [ ] `tools/verify/run_gates.sh L2 <pkg>` 통과
- [ ] 사용자 검증: 새 GUI 띄움 → entry Start → UI X → `ros2 node list` 빈 결과

## Reference 구현

`~/Project/kkw/TR_Nav_ros2_ws/src/ACS/acs_gui/` (2026-05-05 검증 완료):

- `config/launch_manager.yaml` — expected_nodes / kill_keywords 적용
- `acs_gui/process_manager.py` — Step 3 그대로
- `acs_gui/launch_tab.py:shutdown_all` — Step 4 그대로
- `acs_gui/acs_gui_node.py:main` — Step 5 그대로
- `test/test_launch_tab_regression.py` — Step 7 의 pytest e2e

## 관련 기록 (참조 SSOT)

- 본 프로젝트 도메인 가이드: `docs/abstraction/ui_launch_cleanup.md`
- 회귀 7건 누적 history: `docs/claude-mistake/2026-05-05.md` (위반 #1~#12)
- 검증 완료 이슈: `docs/issues_fixes/issues_and_fixes.md` ([2026-05-05 19:30])

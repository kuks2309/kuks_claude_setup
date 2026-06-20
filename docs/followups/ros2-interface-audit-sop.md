# Follow-ups: ROS2 인터페이스 감사 SOP

- **브랜치**: `docs/ros2-interface-audit-sop`
- **대상 파일**: `claude_guideline/coding/ros2.md`
- **사용자 verbatim 근거**: `docs/user_instructions/user_instructions.md` 의 2026-05-25 entry

§8 본문(8.1~8.8) 은 `06558c7` → `9d1f0f0` → `31e87e8` 으로 push 완료. 본 문서는 같은 세션(2026-05-25)에서 합의됐으나 본문에 반영되지 않은 후속 항목을 추적한다. 구현 완료 시 해당 항목을 본 문서에서 체크 표시 또는 제거하고 동일 브랜치에 commit.

다음 세션은 본 문서를 진입점으로 사용한다.

---

## [ ] 합의 1 — §3.9 설정 파일 / 패키지 경로 (재배포)

§3 추가 룰의 신규 절. 3 하위 항목.

### §3.9.1 설정 파일 src 원본 수정

- 모든 설정 파일(rviz·yaml·json·urdf·xacro) 은 `src/<pkg>/...` 원본 편집
- `install/share/<pkg>/...` 사본 직접 수정 시 `colcon build` 가 src→install 복사로 덮어써 변경 사항이 사라짐
- `--symlink-install` 옵션 디폴트 사용 — install/share 가 src 의 symlink 가 되어 install 경로 접근에도 실제 수정은 src 에 반영 (Linux/macOS)

### §3.9.2 rviz2 config 특화 (★ GUI 저장 함정)

- rviz2 메뉴 "Save Config" / `Ctrl+S` 는 **launch 시 가리킨 파일 경로에 그대로 덮어쓴다**
- 그 경로가 `install/share/.../X.rviz` 이고 `--symlink-install` 도 아니면 → 다음 `colcon build` 에서 작업이 모두 사라진다
- 그러므로 rviz2 config 는 항상 **src 에 보관**하고, 다음 둘 중 하나로 launch:
  1. `--symlink-install` 디폴트 + `get_package_share_directory()` (★ 권장 — 패키지 상대 경로 유지하면서 src 가 실질적 저장 대상)
  2. symlink 미지원 환경에선 launch 에서 src 절대 경로 직접 지정
- 일반 yaml 은 IDE 로 수정하므로 위 함정이 없지만, rviz2 는 GUI 가 저장 주체라 별도 명시

### §3.9.3 패키지 상대 경로 (재배포)

- 코드·launch·config 에서 절대 경로 하드코드 금지, 패키지 상대 경로 API 사용:
  - C++: `ament_index_cpp::get_package_share_directory("<pkg>")`
  - Python: `ament_index_python.packages.get_package_share_directory`
  - launch.py: `os.path.join(get_package_share_directory('<pkg>'), 'config', 'X.yaml')`
  - launch.xml: `$(find-pkg-share <pkg>)/config/X.yaml`
  - URDF/xacro: `$(find <pkg>)/...`
- 이유: 배포·다른 호스트 설치 시 절대 경로는 깨진다

### 연관 보완

- **§4 A 체크리스트** 3 항목 추가:
  - "설정 파일 install/share 직접 수정 없음 (§3.9.1)"
  - "rviz config src 보관 + launch 경로 정합 (§3.9.2)"
  - "절대 경로 → 패키지 상대 경로 치환 완료 (§3.9.3)"
- **§5 평가 태그** `[path]` 추가 — 절대 경로 / install/share 직접 참조 / rviz2 저장 경로
- **§7 자체 점검 grep** 추가:
  - 절대 경로 패턴 — `grep -nE '"/(home|opt|root|usr/local)/[^"]+"' src/**/*.{py,yaml,launch.py,rviz,xml}`
  - install/share 직접 참조 — `grep -nE 'install/share/[a-z_]+' src/**/*.{py,launch.py,xml}`

---

## [ ] 합의 2 — rqt_graph 산출물 추가

§8 감사 SOP 에 토픽 간 연결 시각화 산출물 추가. §8.6.1 토픽 연결 맵(표)의 **시각 동반**.

- **§8.3.2 P3 런타임 실측 명령** 에 추가:

  ```bash
  rqt_graph                     # GUI 에서 노드/토픽 그래프 → File > Save As PNG/SVG
  ```

- **§8.2 산출물 위치** 표에 한 줄 추가:

  | 토픽 그래프 시각화 | `docs/rqt_graph.png` (또는 `.svg`) | rqt_graph GUI 캡처 — §8.6.1 토픽 연결 맵 시각 보조 |

- **§8.8 B 체크리스트** 추가:
  - "rqt_graph 캡처 `docs/rqt_graph.png` 가 §8.6.1 토픽 연결 맵과 정합 (노드·토픽 수 일치)"

---

## [ ] 합의 3 — Timer / Thread 룰 보강

현재 `coding/ros2.md` 의 timer 규약은 §2.4 파라미터 예시의 `publish_rate_hz` 한 줄뿐이고, Thread/Executor 는 §3.3 에 있으나 timer 특화 룰 부재. 다음 보강:

### §2.x Timer 인벤토리 표 (신설)

`docs/<pkg>/interfaces.md` 의 Lifecycle 표 앞에 추가:

| # | 이름 | 주기 | callback | callback group | clock source | 기능 | 설명 | 위치 |
|---|---|---|---|---|---|---|---|---|
| 1 | `control_tick` | 20 Hz (50 ms) | `on_control_cb` | `ctrl_cb_group` (ReentrantCallbackGroup) | use_sim_time=True → `/clock` | 제어 루프 주기 | `/cmd_vel` 산출 — base_driver 가 구독 | `ctrl_node.cpp:120` |

- 주기 단위 접미사 의무 (`_hz`, `_ms`, `_us`) — 상위 README §4.2 정렬
- clock source: wall / steady / system / ROS clock (use_sim_time 활성 시) 명시
- callback group 미지정 = 디폴트 group — 명시 의무

### §3.3 (또는 §3.x) Timer 룰 보강

- Timer 도 callback 이므로 §3.3 callback group 배정 의무 동일 적용 — 미지정 시 long-running timer 가 다른 callback 을 직렬화 차단
- `use_sim_time` 활성 환경에서는 wall_timer 대신 ROS clock 기반 timer 사용 (`create_timer(node->get_clock(), ...)` rclcpp / `create_timer(...)` rclpy). wall_timer 는 sim time 무시 → 시뮬에서 실시간으로 발화
- 주기 budget: 콜백 실행 시간 < 주기 × 0.7 권장 (jitter 여유). 초과 시 별도 ReentrantCallbackGroup 또는 worker thread 분리 — §3.3 long-running 룰 연장
- Timer 정지 / 재시작 lifecycle 명시 — node 소멸 시 timer 누수 방지

### §3.x 외부 Thread / Publisher Thread-Safety (신설)

- rclcpp publisher/subscriber 메서드는 thread-safe 보장 — 그러나 사용자 콜백·shared state 는 보호 필요 ([coding/concurrency.md](concurrency.md) §3.1 정렬)
- 외부 `std::thread` 또는 worker pool 에서 publish 호출 허용. 다만 동일 publisher 를 다중 thread 가 호출할 때 **메시지 순서 무보장** — 큐잉 또는 단일 publisher thread 권장
- `spin_some` / `spin_once` 와 `executor.spin()` 혼용 금지 — 메인 루프 polling vs 전용 spin thread 중 하나만 선택

### 연관 보완

- **§4 A 체크리스트**:
  - "Timer 인벤토리 표 §2.x 갱신"
  - "Timer 주기 단위 접미사 (`_hz`, `_ms`) 명시"
  - "Timer callback 차단성 검토 (실행 시간 < 주기 × 0.7)"
  - "use_sim_time 환경에서 wall_timer 사용 없음"
- **§5 평가 태그**:
  - `[timing]` — concurrency.md 와 공유 (jitter, budget 초과)
  - `[clock]` — sim time / wall / ROS clock 불일치 (신설)
- **§7 자체 점검 grep**:
  - `grep -rEn 'create_wall_timer\|create_timer' src/` — 인벤토리 누락 검출
  - `grep -rEn 'wall_timer' src/` + use_sim_time 활성 여부 cross-check

---

## 다음 세션 진입 순서

1. `git -C kuks_claude_setup checkout docs/ros2-interface-audit-sop`
2. 본 문서 읽기 — 합의 사항 확인 (project memory `project_pending_ros2_audit_followups` 과 동일 내용)
3. `kuks_claude_setup_new/claude_guideline/coding/ros2.md` 편집:
   - §3.9 신설 (§3.8 micro-ROS 뒤에 추가) — 합의 1
   - §8.2 산출물 표·§8.3.2 P3 명령·§8.8 B 체크리스트 보강 — 합의 2 (rqt_graph)
   - §2.x Timer 인벤토리 표 신설 + §3.3 Timer 룰 보강 + §3.x 외부 thread 정책 — 합의 3
   - §4 A 체크리스트·§5 평가 태그·§7 grep 보강 — 합의 1·3 연관 보완 통합
4. repo 로 cp → `git add claude_guideline/coding/ros2.md` 단일 파일 → commit (`feat(claude_guideline):` prefix) → push
5. 본 문서의 해당 체크박스 표시 또는 제거 → `git add docs/followups/ros2-interface-audit-sop.md` → commit → push
6. 세 합의 모두 완료되면 본 문서 삭제 + 메모리 갱신

# coding/ros2 — ROS 2 도메인 룰

상위: [coding/README.md](README.md) §10 (도메인 확장 인터페이스)

본 파일은 ROS 2 (Humble 기준) 도메인 특화 룰. 상위 README §1~§9 와 충돌 없이 인벤토리·룰·체크리스트·평가 카테고리를 추가.

기준 배포: ROS 2 Humble Hawksbill (Ubuntu 22.04 LTS, 2027-05 EOL). 다른 배포는 프로젝트 결정 §8 에 명시.

---

## 1. 트리거 (자동 감지)

상위 [coding/README.md](README.md) §10.2 에 등록된 트리거 재명시:

- `package.xml` (build_type: `ament_cmake` / `ament_python`)
- `rclpy` / `rclcpp` import
- `.launch.py` / `.launch.xml` / `.launch.yaml`
- `rcl_interfaces` (msg / srv / action)
- `ros2 run` / `ros2 launch` / `colcon` 빌드 명령

1개 이상 충족 시 본 도메인 활성.

---

## 2. 추가 인벤토리

상위 §9 (문서 양식) 의 함수표·변수표에 추가하여 ROS 2 특화 표 작성. 위치: `docs/<pkg>/` 또는 모듈 `docs/`. 패키지별 분리 (상위 §0.1 ROS 2 워크스페이스 트리).

### 2.1 Subscriptions

| # | 토픽 | 메시지 타입 | QoS (depth · reliability · durability · history) | 콜백 함수 | 위치 |
|---|---|---|---|---|---|
| 1 | `/cam_front/image_raw` | `sensor_msgs/msg/Image` | 5 · BEST_EFFORT · VOLATILE · KEEP_LAST | `on_image_cb` | `cam_node.py:42` |

### 2.2 Publications

| # | 토픽 | 메시지 타입 | QoS | 발행 위치 (함수) | 위치 |
|---|---|---|---|---|---|
| 1 | `/cmd_vel` | `geometry_msgs/msg/Twist` | 10 · RELIABLE · VOLATILE · KEEP_LAST | `publish_cmd` | `ctrl_node.cpp:88` |

### 2.3 Services / Actions

| # | 이름 | 타입 | 클라이언트 / 서버 | 콜백 / 요청 위치 | 위치 |
|---|---|---|---|---|---|
| 1 | `/nav/set_goal` | `nav2_msgs/action/NavigateToPose` | client | `send_goal()` | `nav_client.py:24` |

### 2.4 Parameters (표 + YAML)

| # | 이름 | 타입 | default | declare 위치 | 사용 위치 |
|---|---|---|---|---|---|
| 1 | `front_sector_start` | double | -1.5708 | `node.cpp:30` | `process_scan()` |

YAML 예시 — **의미 그룹별 분리 + 단위·물리량 주석 의무**:

```yaml
node_name:
  ros__parameters:
    # 의미 그룹 1 — 섹터
    front_sector_start: -1.5708    # rad, -90°
    front_sector_end:    1.5708    # rad, +90°

    # 의미 그룹 2 — 거리
    base_stop_distance:    0.3      # m, d_base
    base_warning_distance: 0.8      # m

    # 의미 그룹 3 — 타이밍
    publish_rate_hz:  20.0          # Hz
```

### 2.5 TF Frames (TF 사용 시)

| # | frame | parent | 발행 노드 | 정적 / 동적 | 위치 |
|---|---|---|---|---|---|
| 1 | `base_link` | `odom` | `ekf_node` | 동적 | `ekf.py:60` |

### 2.6 Lifecycle / Composable nodes (사용 시)

| # | 노드 | 타입 | 컨테이너 (composable) | 진입점 |
|---|---|---|---|---|
| 1 | `motor_ctrl` | lifecycle | `ctrl_container` | `MotorCtrl::on_configure()` |

### 2.7 Launch 인자 / Include / Remap

| # | launch arg | default | 사용처 | 위치 |
|---|---|---|---|---|
| 1 | `use_sim_time` | false | 모든 노드 | `bringup.launch.py:18` |

---

## 3. 추가 룰

### 3.1 QoS

- pub / sub QoS **호환성** 검사 의무 (RELIABLE ↔ BEST_EFFORT 불일치 시 메시지 미수신)
- TRANSIENT_LOCAL latching 정합 (latched 토픽 구독 시 sub 도 TRANSIENT_LOCAL)
- 권장 프로파일:

| 데이터 종류 | QoS 권장 |
|---|---|
| 센서 (카메라 · LIDAR · IMU) | `sensor_data` (BEST_EFFORT, KEEP_LAST depth=5) |
| 명령 / 상태 | `default` (RELIABLE, KEEP_LAST depth=10) |
| 정적 정보 (map · TF static) | TRANSIENT_LOCAL + RELIABLE |
| 진단 / 로그 | `default` 또는 `system_default` |

### 3.2 네임스페이스 / 토픽 명명

- 토픽: `<context>/<sensor_or_action>` (예: `/cam_front/image_raw`)
- 가능한 한 **상대 토픽** 사용 (composable / multi-robot 대응)
- 글로벌 절대 토픽은 `/tf`, `/tf_static`, `/clock`, `/parameter_events`, `/rosout` 만 허용
- composable node 시 컨테이너 내 네임스페이스 충돌 검사

### 3.3 Executor / Callback Group

- **multi-threaded executor** 사용 시 callback group 명시 의무
- `MutuallyExclusiveCallbackGroup` (디폴트) — 그룹 내 콜백 순차 실행
- `ReentrantCallbackGroup` — 동시 실행 허용 (재진입 안전 필요)
- Long-running callback (>10ms) 은 별도 ReentrantCallbackGroup 또는 worker thread 분리
- callback 차단성 검토 — `[exec]` 평가 카테고리

### 3.4 Parameters

- `declare_parameter` **의무** (undeclared 파라미터 사용 금지 — `automatically_declare_parameters_from_overrides` 사용 시 명시)
- 단위·물리량 주석 의무 (상위 §1.1 명명 · §4.2 단위 접미사 정렬)
- 파라미터 범위 validator (`ParameterDescriptor.integer_range` / `floating_point_range`)
- 동적 재구성 지원 시 `on_set_parameters_callback` 등록

### 3.5 Launch / 빌드

- launch arg 는 `declare_launch_argument` + `default_value` + `description` 의무
- composable node 시 컨테이너 분리 명시 (single-process 효율 vs 격리 트레이드오프)
- `ament_python`: `setup.py` 의 `entry_points` 와 `package.xml` 의 `exec_depend` 일관
- `ament_cmake`: `install(TARGETS ... DESTINATION lib/${PROJECT_NAME})` 누락 점검
- launch description 은 `OpaqueFunction` 으로 동적 분기 시 명시

### 3.6 Lifecycle

- 노드 lifecycle 사용 시 transition 명시: `configure` → `activate` → `deactivate` → `cleanup` → `shutdown`
- `on_configure`: 리소스 할당 (publisher / subscription / param)
- `on_activate`: publisher `on_activate()` 호출 의무 (LifecyclePublisher)
- `on_deactivate`: publisher `on_deactivate()`
- `on_cleanup`: 리소스 해제
- 안전 분기 (motor / actuator) 는 lifecycle 권장

### 3.7 TF / 좌표계

- frame 명명: REP 105 (`map` ↔ `odom` ↔ `base_link` ↔ `<sensor>_link`)
- 정적 vs 동적 frame 명시 (`tf2_ros::StaticTransformBroadcaster` vs `TransformBroadcaster`)
- 좌표계 단위는 상위 §4.2 정렬 (m, rad)
- `use_sim_time` 활성 시 `/clock` 구독 + sim time 사용 일관성

### 3.8 micro-ROS / 임베디드 연계

`rclc` (micro-ROS) 사용 시 [embedded/README.md](embedded/README.md) 도메인 동시 활성. ISR · WCET · stack 룰은 embedded 따름.

---

## 4. 추가 종료 체크리스트

상위 §7 A/B/C/D 골격에 다음 항목 첨가.

### A. 기술 부채 방지 (ROS 2 특화)
- [ ] QoS 호환성 (pub / sub 정합) — `ros2 topic info -v` 확인
- [ ] `declare_parameter` 누락 없음
- [ ] composable node 컨테이너 명시
- [ ] launch arg 기본값 + 설명
- [ ] callback 차단성 검토 (>10ms 시 별도 group)

### B. 이해 부채 방지 (ROS 2 특화)
- [ ] Subscriptions / Publications 표 갱신 (§2.1, §2.2)
- [ ] Services / Actions 표 갱신 (§2.3)
- [ ] Parameters YAML 단위 주석 (§2.4, §3.4)
- [ ] TF frames 표 갱신 (§2.5)
- [ ] Lifecycle / Composable 표 갱신 (§2.6)
- [ ] Launch 인자 표 갱신 (§2.7)

### C. 의도 부채 방지 (ROS 2 특화)
- [ ] QoS 변경 → ADR (상위 §1.2 외부 인터페이스 트리거)
- [ ] 토픽 명명 / 네임스페이스 변경 → ADR
- [ ] Executor / Callback group 정책 ADR
- [ ] Lifecycle 도입 / 변경 ADR

### D. 위반 / 예외 / 인계 (ROS 2 특화)
- [ ] 글로벌 절대 토픽 사용 사유 (허용 5개 외)
- [ ] callback 차단성 위반 — tech_debt.md 등록

---

## 5. 평가 카테고리 (인라인 태그)

[code_review.md](../code_review.md) Add-on A 와 정합.

- `[QoS]` — pub / sub QoS 호환성, latching 정합, depth 부족
- `[ns]` — 네임스페이스 / 토픽 충돌, 글로벌 절대 토픽 남용
- `[exec]` — executor 선택 (single vs multi), callback group 적합성
- `[param]` — 파라미터 declare / 단위 / 범위
- `[runtime]` — 런타임 필수 노드 부재 시 동작 (상위 §1 의존성 tier 2 와 연계)
- `[lifecycle]` — lifecycle transition 누락 / 잘못된 호출
- `[tf]` — TF frame 명명 / 좌표계 / sim time
- `[launch]` — launch arg 누락 / composable 분리 / `install()` 누락

---

## 6. 다른 도메인과의 의존 / 충돌

- **concurrency**: multi-threaded executor + callback group 은 본질적으로 concurrency. lock 순서 / race / shared state 룰은 [coding/concurrency.md](concurrency.md) 따름. 본 파일은 executor · callback group 정책만.
- **embedded**: micro-ROS (rclc) 사용 시 [embedded/README.md](embedded/README.md) 동시 활성. ISR · WCET · stack · DMA 룰은 embedded 따름. 본 파일은 ROS 통신·메시지·QoS 만.
- 충돌 시 우선순위: 상위 [coding/README.md](README.md) > 도메인 파일. 도메인 간 충돌은 사용자 결정.

---

## 7. 자체 점검 grep

```bash
TARGET=docs/<pkg>/ros2_review.md  # 또는 docs/code_review/<주제>.md

# 1. Subscriptions 표
grep -E "토픽.*메시지 타입.*QoS.*콜백" $TARGET

# 2. Publications 표
grep -E "토픽.*메시지 타입.*QoS.*발행 위치" $TARGET

# 3. Parameters 표
grep -E "이름.*타입.*default.*declare 위치" $TARGET

# 4. YAML 단위 주석 (의미 그룹 또는 단위)
grep -E "^\s+#\s+(rad|m|Hz|deg|ms|s|kg|°)" $TARGET

# 5. 평가 태그
grep -oE "\[(QoS|ns|exec|param|runtime|lifecycle|tf|launch)\]" $TARGET | sort -u
```

---

## 룰 (요약)

1. **QoS 호환성** §3.1 — pub/sub 정합, 권장 프로파일
2. **상대 토픽 우선** §3.2 — 글로벌 절대 토픽은 5개만 허용
3. **multi-threaded executor 시 callback group 의무** §3.3
4. **declare_parameter 의무** §3.4 — undeclared 사용 금지
5. **YAML 파라미터 단위 주석 의무** §3.4
6. **launch arg declare + default + description** §3.5
7. **Lifecycle 사용 시 transition 명시** §3.6 — `on_activate` publisher activate 의무
8. **TF REP 105 + 정적/동적 명시** §3.7
9. **micro-ROS 시 embedded 동시 활성** §3.8
10. **concurrency / embedded 충돌 시 해당 도메인 우선** §6
11. **본 README 와 충돌 금지** — 상위 [coding/README.md](README.md) §1~§9 가 권위

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

## 8. 기존 워크스페이스 인터페이스 감사 SOP

§2 인벤토리 표는 **코드 작성 시** 양식이다. 본 절은 반대 방향 — **기존 워크스페이스에서 토픽 / 서비스 / 액션 / QoS 인터페이스를 역추출·정규화·검증**하는 절차다.

### 8.1 적용 시점

다음 1개 이상 충족 시 본 SOP 실행 의무:

- 기존 ROS 2 워크스페이스를 처음 분석·인수·코드 리뷰할 때
- 인터페이스 문서(`docs/<pkg>/interfaces.md`)가 없거나 코드와 어긋났다고 의심될 때
- 노드별 토픽 / 액션 리스트 또는 QoS 준수 여부를 보고해야 할 때

### 8.2 산출물 위치

| 산출물 | 위치 | 내용 |
|---|---|---|
| 패키지별 인터페이스 | `docs/<pkg>/interfaces.md` | §2.1~§2.7 표를 역추출 값으로 채움 |
| 워크스페이스 집계 | `docs/interfaces_index.md` | 노드↔토픽 매핑 + §8.5 QoS 매트릭스 + §8.6 불일치 보고 |

**메타 감사 모드** — 여러 워크스페이스를 한 외부 위치에 수집할 때는 `<수집경로>/<workspace_slug>/` 하위에 위 구조를 그대로 출력하고, 대상 워크스페이스 repo 는 read-only 로 둔다 (소스만 읽고 산출물은 외부에 기록). 수집경로·slug 규칙은 작업 지시 시 명시한다.

### 8.3 3단계 절차

| Phase | 입력 | 명령 / 패턴 | 출력 |
|---|---|---|---|
| **P1 문서 수집** | 워크스페이스 내 `docs/`, `README.md` | `find` + `grep -lEi 'topic|qos|publisher|subscriber'` 로 기존 인터페이스 서술 검색 | P1 인벤토리 (문서 기준) |
| **P2 코드 정적 분석** | 소스 트리 (`src/**`) | 아래 §8.3.1 패턴 grep / AST 검색 | P2 인벤토리 (코드 기준) |
| **P3 런타임 실측** | 빌드+노드 실행 가능한 환경 | 아래 §8.3.2 `ros2` CLI 명령 | P3 인벤토리 (런타임 ground truth) |

P3 가 불가능한 환경(실 로봇 부재 · 빌드 실패 · HIL 미구성)은 **"P3 skipped + 사유"** 를 §8.6 에 명시한다. P1+P2 만으로도 본 SOP 는 완수로 인정하되, QoS 매트릭스의 실측 열은 `(미실측)` 으로 표기한다.

#### 8.3.1 P2 코드 정적 분석 패턴

```bash
# Publisher / Subscriber
grep -rEn 'create_publisher|create_subscription|\.advertise|\.subscribe' src/
# Service / Client
grep -rEn 'create_service|create_client' src/
# Action
grep -rEn 'ActionServer|ActionClient|rclcpp_action::create_' src/
# Parameter
grep -rEn 'declare_parameter|declare_parameters' src/
# QoS 리터럴 / 프로파일
grep -rEn 'QoSProfile|qos_profile_sensor_data|rclcpp::QoS|ReliabilityPolicy|DurabilityPolicy|HistoryPolicy' src/
# TF broadcaster
grep -rEn 'TransformBroadcaster|StaticTransformBroadcaster' src/
```

토픽명이 런타임 remap / 네임스페이스로 결정되는 경우 코드 리터럴만으로 단정하지 말고 launch 파일의 `remappings` 와 노드 네임스페이스를 함께 확인한다.

#### 8.3.2 P3 런타임 실측 명령

```bash
# 빌드 + 소싱 (워크스페이스 루트, §coding/README 0.1)
colcon build --symlink-install && source install/setup.bash
# 노드 기동 후:
ros2 node list
ros2 node info <node>                 # 노드별 pub/sub/service/action 전체
ros2 topic list -t                    # 토픽 + 타입
ros2 topic info <topic> -v            # QoS profile 실값 (pub/sub 별)
ros2 service list -t
ros2 action list -t
ros2 param dump <node>                # 파라미터 실값
```

`ros2 node info` 와 `ros2 topic info -v` 의 출력이 노드별 토픽 리스트 + QoS 의 1차 권위 소스다.

### 8.4 정규화 규칙

3 소스(P1 문서 · P2 코드 · P3 런타임)가 충돌할 때 권위 순서:

```text
P3 런타임  ≻  P2 코드  ≻  P1 문서
```

근거: 런타임 = 실제 동작(ground truth), 코드 = 의도, 문서 = 설명. 정규화 표(`interfaces.md`)에는 권위 소스 값을 싣되, 다음을 지킨다:

- 각 항목에 **출처 열**(`P1 / P2 / P3` 또는 조합) 명시. `P2-only` = 코드에 있으나 런타임 미관측 → dead code 또는 비활성 노드 의심 → §8.6 기재.
- QoS 값은 P3 실측 우선, 미실측 시 P2 코드 리터럴, 둘 다 없으면 rmw 기본값을 `(추정)` 으로 표기 — [coding/README.md](README.md) §1.4 L3 추정 금지와 정렬, 추정 항목은 실측 격상 대상.
- 충돌(같은 토픽이 소스마다 타입·QoS 다름)은 정규화 표에서 권위 값 사용 + §8.6 불일치 보고에 전체 기재.

### 8.5 QoS 검증 매트릭스

`interfaces_index.md` 에 토픽별 1행으로 §2.1/§2.2 표를 집계한다.

| 토픽 | 메시지 타입 | Publishers (node · QoS) | Subscribers (node · QoS) | 호환성 | 권장(§3.1) 대비 |
|---|---|---|---|---|---|
| `/cmd_vel` | `geometry_msgs/msg/Twist` | ctrl_node · RELIABLE·VOLATILE·KEEP_LAST·10 | base_driver · RELIABLE·VOLATILE·KEEP_LAST·10 | ✅ | 명령 → `default` 부합 |
| `/scan` | `sensor_msgs/msg/LaserScan` | lidar_node · BEST_EFFORT·VOLATILE·KEEP_LAST·5 | nav_node · RELIABLE·VOLATILE·KEEP_LAST·10 | ❌ reliability | 센서 → `sensor_data` 권장, 양쪽 BEST_EFFORT 로 통일 |

**호환성 판정 (DDS request-offered 규칙)**:

| 정책 | 호환 (pub offered ⊇ sub requested) | 불일치 (sub 미수신) |
|---|---|---|
| Reliability | pub RELIABLE → sub RELIABLE/BEST_EFFORT, pub BEST_EFFORT → sub BEST_EFFORT | pub BEST_EFFORT → sub RELIABLE |
| Durability | pub TRANSIENT_LOCAL → sub TRANSIENT_LOCAL/VOLATILE, pub VOLATILE → sub VOLATILE | pub VOLATILE → sub TRANSIENT_LOCAL (late-join 미수신) |
| History / depth | 직접 불일치는 아니나 depth 부족은 드롭 유발 — 권장 프로파일 §3.1 대비로 점검 | — |

`❌` 1건 이상이면 §8.7 A 체크리스트 미통과 — 원인·조치를 §8.6 에 기재한다.

### 8.6 불일치 보고 양식

`interfaces_index.md` 말미에 작성. 무불일치 시 "불일치 없음" 한 줄.

| # | 항목 | P1 문서 | P2 코드 | P3 런타임 | 판정 | 조치 |
|---|---|---|---|---|---|---|
| 1 | `/scan` QoS | 미기재 | BEST_EFFORT | BEST_EFFORT | 문서 누락 | `interfaces.md` 갱신 |
| 2 | `/old_cmd` 토픽 | 기재됨 | grep 검출 | `node info` 미검출 | P2-only, dead code 의심 | 코드 확인 후 제거 또는 사유 ADR |
| 3 | P3 전체 | — | — | skipped | 실 로봇 부재 | 실측 가능 시 재감사 |

### 8.7 감사 종료 체크리스트

[coding/README.md](README.md) §7 A/B/C/D 골격에 본 SOP 특화 항목을 첨가한다.

#### A. 기술 부채 방지 (감사)
- [ ] P1·P2·P3 실행 (skip 시 §8.6 에 사유)
- [ ] 모든 노드 커버 — `ros2 node list` 전수 또는 `src/**` 진입점 전수
- [ ] QoS 매트릭스 §8.5 작성, `❌` 0건 (잔존 시 §8.6 조치 기재)

#### B. 이해 부채 방지 (감사)
- [ ] `docs/<pkg>/interfaces.md` §2 표 채움 (출처 열 포함)
- [ ] `docs/interfaces_index.md` 노드↔토픽 매핑 + QoS 매트릭스
- [ ] 각 항목 권위 소스(P1/P2/P3) 명시, `(추정)` 항목 표기

#### C. 의도 부채 방지 (감사)
- [ ] 권장 QoS(§3.1) 위반인데 의도적이면 사유 ADR
- [ ] 정규화 권위 순서(§8.4) 예외 적용 시 ADR

#### D. 위반 / 예외 / 인계 (감사)
- [ ] P3 skip 사유
- [ ] 코드↔문서 불일치 잔존 항목 (§8.6 미해결 행)

#### 자체 점검 grep (감사 산출물용 — §7 보완)

```bash
TARGET=docs/interfaces_index.md
grep -E "토픽.*메시지 타입.*Publishers.*Subscribers.*호환성" $TARGET   # QoS 매트릭스 헤더
grep -E "P1 문서.*P2 코드.*P3 런타임.*판정" $TARGET                      # 불일치 보고 헤더
grep -oE "P[123](-only)?" docs/*/interfaces.md | sort -u                # 출처 표기 존재
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
12. **기존 워크스페이스 인수 시 §8 감사 SOP** — 3단계(문서·코드·런타임) 역추출 + QoS 매트릭스 검증, 권위 순서 P3≻P2≻P1

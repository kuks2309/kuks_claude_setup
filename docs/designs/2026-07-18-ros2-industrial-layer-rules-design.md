# 설계: ROS2 산업용 응용 계층 코딩 룰 (자율주행 · 로봇 제어 · TF)

- 날짜: 2026-07-18 / 세션: 3de11025
- 상태: 사용자 스펙 검토 대기
- 반영 대상 SSOT(Single Source of Truth): `kuks_claude_setup_new/claude_guideline/coding/` (v2)
- 관련 기존 문서: `coding/ros2.md` (메커니즘 축, 451줄), `docs/followups/ros2-interface-audit-sop.md` (합의 1~4)

## 1. 배경과 목적

기존 `coding/ros2.md` 는 QoS(Quality of Service)·executor·파라미터·lifecycle 등 **ROS2 메커니즘 축**의 룰이다. 본 설계는 여기에 직교하는 **응용 기능 계층 축**을 추가하되, 표준 스택(Nav2·MoveIt) 사용 안내가 아니라 **산업 현장 요구 기준**으로 작성한다. 표준 스택의 디폴트 동작이 산업 요구를 위반하면(예: Nav2 상시 경로 재계획) **디폴트를 바꾸는 쪽이 룰**이다.

## 2. 결정 사항 (토론 로그 요약)

| # | 결정 | 근거 (사용자 지시) |
|---|---|---|
| 1 | 산출물 = **계층별 코딩 룰** (인벤토리 양식·아키텍처 룰 아님) | 2026-07-18 문답 |
| 2 | 로봇 제어는 **벤더 위임형 + 자체형 모두** 수용, 역할 계층으로 정의 | "표준 스택은 산업용으로 미흡, 토론 필요" |
| 3 | 구조 = **응용 도메인 파일 분리** (기존 ros2.md 비대화 방지, v3 이식 단위와 1:1) | 구조 3안 중 A 채택 |
| 4 | 문서 성격 = **산업용 기준 룰** — 표준 디폴트 위반 지점을 식별·강제 대체 | "Nav2 불필요한 상시 path 생성은 산업용에서 절대 회피" |
| 5 | **TF(Transform) 원칙 별도 파일** — 코더 오해 교정 중심 | "코더들이 잘 모르는 TF 원칙 별도 추가·강화" |
| 6 | 이동로봇 **의무 TF 체인** `map→odom→base_footprint→base_link→<sensor>_link` | "반드시 규칙을 지켜야 함" |
| 7 | **오도메트리 보강 룰** 신설 — 1순위: 엔코더 카운트 기반 위치 (속도 적분 금지) | "엔코더를 위치로 사용해야 하는데 속도를 적분해서 사용함" (최다 빈발 문제) |
| 8 | **합의 2 (rqt_graph 산출물)** 이번 세션 구현에 포함 | "합의 2 는 진행해야, 중요한데" |
| 9 | v3 이식은 이번 세션 **비범위** — followups 합의 4 에 등록만 | 기존 합의 4 규약 유지 |
| 10 | **dead reckoning 상대 변위 원칙** — 절대 위치 투영 금지 | "절대 위치를 쓰면 원점과 동떨어진 곳에서 odom 이 생성됨" |

## 3. 전체 구조

```text
kuks_claude_setup_new/claude_guideline/coding/
├─ ros2.md               기존 유지 + 경미 수정 (§7 참조)
├─ ros2_autonomous.md    신설 — 자율주행 인지/판단/제어 + 산업 4원칙 + 안티패턴 대조표
├─ ros2_manipulation.md  신설 — 로봇 제어 계층 + 벤더 위임/자체 변형 + 산업 4원칙
└─ ros2_tf.md            신설 — TF 원칙 (오해 교정 + 의무 체인, 두 응용 파일이 공통 참조)
```

- 우선순위: 상위 `coding/README.md` > `ros2.md`(메커니즘) > 응용 파일. 응용 파일은 메커니즘 룰(QoS 표·파라미터 규약 등)을 복제하지 않고 `ros2.md` 를 참조한다.
- 각 신설 파일은 기존 도메인 파일 관례를 따른다: 트리거 → 룰 본문 → 종료 체크리스트(A/B/C/D 골격) → 평가 태그 → 자체 점검 grep → 룰 요약.
- 약어는 각 파일 첫 등장 시 `약어(영어 단어)` 형식으로 병기한다.

## 4. 산업 4원칙 (두 응용 파일 서두 공통, 예시만 도메인별)

1. **결정론** — 같은 입력·같은 상태 → 같은 행동. 예측 불가능한 적응 행동 금지 (현장 안전 = 예측 가능성).
2. **이벤트 구동** — 지속 폴링·지속 재계획 금지. 열거된 트리거 이벤트에만 반응.
3. **정지 우선** — 불확실 상황의 기본 동작은 정지 후 대기. 회피·재시도는 명시 허용 + ADR(Architecture Decision Record) 시에만.
4. **자원 예산** — 상시 모니터링 루프의 CPU·대역폭 낭비 금지. 모든 주기 작업은 주기와 존재 사유 명시 의무.

## 5. ros2_autonomous.md 골격

- **§1 트리거**: `nav2_*`·`slam_toolbox`·`robot_localization` 의존, `/cmd_vel` 발행, `nav_msgs` 사용 등 1개 충족 시 활성.
- **§2 문서 성격 + 산업 4원칙** (§4 내용, 자율주행 예시).
- **§3 계층 정의 + 노드↔계층 매핑 표**: 인지(센서 드라이버·전처리·인식·위치추정) / 판단(경로계획·행동결정·작업관리) / 제어(경로추종·속도제어·모터 드라이버 IF(Interface)). "한 노드 = 한 계층" 원칙, 위반 시 ADR. 표 양식: `노드 | 계층 | 입력 토픽 | 출력 토픽 | 근거`.
- **§4 인지 룰**: 센서 입력 BEST_EFFORT(`ros2.md` §3.1 정렬), 출력 msg 에 `header.stamp`(센서 원본 시각 유지)·`frame_id` 의무, 처리 지연 예산 파라미터화, TF lookup timeout·extrapolation 정책 명시.
- **§4.x 오도메트리 룰 (인지 하위절, ★ 사용자 최다 빈발 문제 반영)**:
  1. **위치는 엔코더 누적 카운트 차분으로** — pose 증분 = Δticks × 거리/틱. 속도 샘플 `v·Δt` 적분으로 pose 산출 **금지** (지터·드롭·필터 지연이 위치에 영구 누적). **명령 속도 적분(open-loop)은 절대 금지**. twist 는 카운트 차분의 미분으로 채움. 카운터 오버플로/랩어라운드 처리 명시. 펌웨어→호스트 IF 는 **누적 카운트 보고 의무** (속도만 보고하는 설계 = 위반, 임베디드 도메인 연계).
  2. **상대 변위 누적 (dead reckoning 원점 원칙)** — 기동 시 엔코더 카운트 baseline 을 캡처하고 이후 Δ만 누적, odom pose 는 기동 시점 (0,0,0) 에서 시작. 드라이버의 수명 누적 카운트·절대 위치값을 pose 로 직접 투영 **금지** (odom 이 원점과 동떨어진 곳에서 생성되는 원인). 절대(전역) 위치 정렬은 `map→odom` 보정 소관 — GPS(Global Positioning System)·마커 등 절대 위치를 odom 에 직접 주입하는 것도 위반.
  3. **단독 휠 오도메트리 금지** — IMU(Inertial Measurement Unit) 융합(EKF(Extended Kalman Filter) 등) 의무, 스캔매칭 보정은 환경별 추가.
  4. **공분산 정직성** — covariance 실측 근거 설정, 디폴트 0·임의 상수 금지.
  5. **캘리브레이션 규정** — 휠 반경·휠 간격 파라미터화 + 절차·재수행 조건(마모·하중 변경) 명시.
  6. **슬립 검출 의무** — 명령 vs 측정 속도, IMU vs 휠 각속도 비교 → 판단 계층에 이상 보고.
  7. **드리프트 예산** — 주행거리 대비 허용 드리프트 수치화, localization 보정 커버 검증.
  8. **twist 프레임 규약** — odometry twist 는 child frame(`base_footprint`) 기준 (REP(ROS Enhancement Proposal) 105).
- **§5 판단 룰**: 상태기계/BT(Behavior Tree) 전이 문서화 의무, 모든 대기 상태 timeout+fallback(무한 대기 금지), 인지 입력 스테일 검출·안전 동작. **재계획 트리거 열거 의무** — `경로 봉쇄 확정 / 목표 변경 / 운영자 지시` 등 열거 이벤트에서만 재계획, 매 주기·타이머 상시 재계획 **금지**. Nav2 사용 시 BT XML 감사 의무(`RateController`+`ComputePathToPose` 상시 루프 = 위반). 고정 경로/노드-엣지 그래프 기본, 자유공간 계획은 ADR.
- **§6 제어 룰**: 고정 주기 timer 루프(콜백 즉발 제어 금지), 상위 명령 스테일 시 정지 발행(deadman/watchdog), 속도·가속 클램프 파라미터화+단위 주석, 종료·예외 시 0 명령 보장(fail-safe).
- **§7 안전·진단 (cross-cutting)**: E-stop 경로만 계층 우회 직결 허용, diagnostics 발행 의무 노드 규정, heartbeat 감시.
- **§8 표준 디폴트 vs 산업 룰 대조표**:

| # | 표준 스택 디폴트 | 산업 룰 |
|---|---|---|
| 1 | Nav2 상시 경로 재계획 (매 주기 path 재생성) | 이벤트 트리거 재계획만 허용 |
| 2 | 동적 장애물 회피 기동 | 정지 후 대기, 해소 시 재개 |
| 3 | costmap 전역 상시 갱신 | 주행 구간 한정 + 갱신 주기 명시 |
| 4 | 자유공간 어디로든 계획 | 고정 경로·허용 구역 제한 |
| 5 | 노드별 자율 재시도 (best-effort) | 실패 시 상위 보고·운영자 개입 경로 명시 |
| 6 | 속도 적분으로 위치 산출 / 휠 엔코더 무보강 신뢰 | 카운트 차분 위치 + 융합·슬립 검출·공분산 정직성 의무 |
| 7 | 누적 카운트·절대 위치를 그대로 odom pose 로 투영 | 기동 baseline 차분 누적, odom 은 (0,0,0) 시작, 절대 정렬은 `map→odom` 소관 |

- **§9 체크리스트(A/B/C/D) + 평가 태그** `[layer]` `[replan]` `[stale]` `[deadman]` `[estop]` `[odom]` **+ 자체 점검 grep** (예: `create_wall_timer` 인접 `compute_path` 검출, `cmd_vel` 발행 노드의 watchdog 부재 검출, 속도 적분 패턴 `+= .*linear.*dt` 검출).

## 6. ros2_manipulation.md 골격

- **§1 트리거**: `moveit`·`ros2_control` 의존, 벤더 드라이버(Techman 등), `FollowJointTrajectory`, 그리퍼·IO 제어.
- **§2 문서 성격 + 산업 4원칙** (로봇 제어 예시: 이벤트 구동 = 폴링 대신 컨트롤러 상태 이벤트 구독, 정지 우선 = fault 시 재시도 아닌 보호 정지).
- **§3 계층 정의 + 매핑 표**: 작업 오케스트레이션(작업 시퀀스·MES(Manufacturing Execution System)/PLC(Programmable Logic Controller) 연동·상위 상태기계) / 모션·동작(동작 프리미티브·궤적 생성) / 컨트롤러 IF(벤더 드라이버·ros2_control HW(Hardware) IF·그리퍼).
- **§4 벤더 위임형 vs 자체형 변형 규정**: 프로젝트 CLAUDE.md 에 **위임 경계 명시 의무** (모션계획·서보의 소관). 벤더 위임형 = 벤더 컨트롤러를 read-only 외부 경계로 취급(기존 외부 드라이버 보호 룰 정렬). 자체형 = ros2_control 주기·RT(Real-Time) 요구 명시.
- **§5 계층별 룰**: 오케스트레이션 — 동작 호출마다 timeout·retry·실패 복구 경로 의무, 외부 연동 프로토콜 명시. 모션·동작 — 프리미티브는 취소 가능한 action 의무, 속도·가속 제약 파라미터화. 컨트롤러 IF — 전송 실패·연결 끊김 검출·재연결 정책 의무.
- **§6 안전·진단 (cross-cutting)**: 정지 카테고리(즉시 차단 vs 감속 정지) 명시, fault 상태 전이·수동 리셋 여부 규정, 진단 발행.
- **§7 체크리스트 + 평가 태그** `[layer]` `[boundary]` `[stopcat]` `[recover]` **+ grep**.

## 7. ros2_tf.md 골격 (오해 교정 중심)

각 절: "코더가 흔히 틀리는 오해" 명시 → 원칙으로 교정.

- **§1 트리거**: `TransformBroadcaster`/`Buffer`/`Listener`, `lookup_transform`, `doTransform`, URDF(Unified Robot Description Format)/`robot_state_publisher`.
- **§2 트리 구조 원칙**: 단일 트리, frame 당 부모 1개·broadcaster 1개. localization 은 `map→base_link` 직접 발행 금지(`map→odom` 보정 발행). REP 103 축 규약(x 전방·y 좌·z 상, m·rad).
- **§2.x 이동로봇 의무 표준 체인 (★)**:

  `map → odom → base_footprint → base_link → <sensor>_link`

  | 구간 | 발행 주체 (유일) | 성격 |
  |---|---|---|
  | `map → odom` | localization (SLAM(Simultaneous Localization and Mapping)/AMCL(Adaptive Monte Carlo Localization) 등) | 동적, 불연속 허용 |
  | `odom → base_footprint` | **오도메트리 융합 노드(EKF) — 휠 단독 금지** (ros2_autonomous §4.x) | 동적, 연속 |
  | `base_footprint → base_link` | URDF/`robot_state_publisher` | 정적 |
  | `base_link → <sensor>_link` | URDF/`robot_state_publisher` | 정적 |

  명시적 위반 목록: ① `base_footprint` 생략 `odom→base_link` 직결(최다 위반) ② localization 의 `map→base_link` 직접 발행 ③ 센서 frame 을 `odom`/`map` 에 직접 부착 ④ 정적 구간을 코드에서 동적 broadcast ⑤ 한 구간 다중 broadcaster.
- **§3 시간 원칙**: TF = 시계열 버퍼(lookup 은 시각 보간). 센서 변환은 msg 의 `header.stamp` 로 lookup — `now()` 금지. `Time(0)` vs `now()` 차이, timeout 정책 의무. 미래 시각 발행 금지, 버퍼 보존 기간(기본 10초) 인지.
- **§4 발행 원칙**: 고정 변환 = static broadcaster(1회·TRANSIENT_LOCAL). 고정 변환 주기 발행 = 위반. URDF 고정 프레임은 `robot_state_publisher` 위임(수동 중복 발행 금지). 동적 TF 는 데이터 생성 시각 stamp.
- **§5 변환 계산 원칙**: 수동 행렬 곱·역변환 금지 — `lookup_transform`/`doTransform` 이 체인·역변환·보간 담당. `lookup_transform(target, source)` 방향 의미 명시.
- **§6 다중 로봇**: `frame_prefix` 규약.
- **§7 체크리스트 + 평가 태그** `[tf-tree]` `[tf-time]` `[tf-static]` `[tf-chain]` **+ grep** (lookup 인접 `now()` 검출, 동일 frame 다중 broadcaster 검출, 표준 체인 대조는 `view_frames` 산출물 + `ros2.md` §8.6.3 교차 참조).

## 8. 기존 ros2.md 수정 목록 (경미)

1. **§6 도메인 의존/충돌**: 신설 3파일 등록 + 트리거·우선순위 관계 명시.
2. **§3.7 TF/좌표계**: 표면 룰 유지 + 심화 원칙은 `ros2_tf.md` 위임 포인터 1줄.
3. **§8 합의 2 (rqt_graph) 반영 — 3개소**: §8.2 산출물 표에 `docs/rqt_graph.png` 1행, §8.3.2 P3 명령에 `rqt_graph` 1줄, §8.8 B 체크리스트에 정합 항목 1개 (followups 문서의 스펙 그대로).

## 9. 반영 절차

1. **v2 SSOT 작성** — 신설 3파일 + `ros2.md` 수정. 파일별 사용자 승인 후 진행 (다중 파일 일괄 작성 금지).
2. **SIL(Software-In-the-Loop) 검증** — 작성 직후 `dogfooding/` 에서 회고 entry 2~3개로 형식 결함 검증.
3. **v1 sync** — `kuks_claude_setup` 에 파일별 1 commit (`feat(claude_guideline):` prefix), 세션 격리 staging(명시 경로 add + `diff --cached` 검증) 준수. 대상 브랜치는 구현 계획에서 확정 (`docs/ros2-interface-audit-sop` 연장 vs 신규 브랜치 — 합의 2 가 해당 브랜치 소관이므로 연장이 유력).
4. **followups 갱신** — 합의 2 체크 완료 표시, 합의 4(v3 이식 대상)에 신설 3파일 추가 등록.

## 10. 비범위

- v3(`kuks_claude_skill_setup`) 이식 — 합의 4 에 등록만, 실행은 후속 세션.
- followups 합의 1(§3.9 설정·경로 룰)·합의 3(Timer/Thread 보강) — 기존 추적 유지, 이번 세션 미실행. 단 합의 3 의 timer 룰과 본 설계 제어 룰(고정 주기 루프)은 중복되지 않게 구현 시 교차 참조.
- 워크스페이스 `docs/claude_guideline/ros2.md`(v1 master 계열 작업 규칙)는 본 설계와 무관 — 수정하지 않음.

## 11. 검증 계획

- 각 신설 파일의 자체 점검 grep 이 실제로 위반 패턴을 검출하는지 예제 코드 조각으로 확인.
- SIL 검증 (§9-2).
- 기존 `ros2.md` 룰과의 충돌 여부 대조 (특히 §3.1 QoS·§3.7 TF·§3.3 executor).

## 12. 교차 검토 규약 (두 컴 round-trip)

본 문서의 권위 소스는 **`kuks_claude_setup` repo 의 `docs/designs/2026-07-18-ros2-industrial-layer-rules-design.md`** (브랜치 `docs/ros2-interface-audit-sop`) 이다. 워크스페이스 `docs/superpowers/specs/` 사본은 초안 스냅샷으로, 이후 수정은 repo 사본에만 한다.

### 12.1 다른 컴 (검토자) 절차

1. `git fetch origin && git checkout docs/ros2-interface-audit-sop && git pull --ff-only`
2. 본 문서 전체 + 배경 파일(`claude_guideline/coding/ros2.md`, `docs/followups/ros2-interface-audit-sop.md`) 읽기
3. 보완 의견은 본문을 직접 고치지 말고 **"§13 교차 검토 의견" 절에 append** (충돌 최소화·출처 식별). 항목 형식:

   | # | 대상 절 | 문제점 | 제안 | 상태 |
   |---|---|---|---|---|
   | R1 | §5 §4.x | (예) 슬립 검출 임계값 기준 부재 | (예) 비율 임계 + 지속시간 조건 명시 | 미처리 |

4. 현장 경험 기반 의견(안티패턴 사례·수치 기준) 우선. 완료 후 같은 브랜치에 commit(`docs(designs): 교차 검토 의견 R#~R#`)·push.

### 12.2 본 컴 (작성자) 절차

1. pull 후 §13 의견을 본문에 반영, 각 항목 `상태` 를 `반영(위치)` / `보류(사유)` 로 갱신
2. 반영 commit·push → 검토자가 재확인
3. **종료 조건**: §13 에 `미처리` 0건 → 스펙 확정, 구현(파일 작성) 단계 진입

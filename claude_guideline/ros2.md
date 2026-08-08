# ROS2 / 임베디드 작업 규칙

ROS2 워크스페이스 + 임베디드 / 외부 드라이버 결합 환경에 적용되는 도메인 SSOT (Single Source of Truth / 단일 근원). ROS2 프로젝트에서는 다른 가이드라인보다 먼저 읽는다.

프로젝트 고유 값(빌드 옵션 변형, 네트워크 설정, 패키지 경로, IP 등)은 본 문서가 아닌 워크스페이스 루트 `CLAUDE.md` 또는 [`local/`](local/) 의 override 문서에 둔다.

## 빌드 명령

- 워크스페이스 루트에서 `colcon build` 사용. `--symlink-install` 옵션은 src 원본 사용 규칙과 직결되므로 임의 제거 금지.
- 단일 패키지 빌드: `colcon build --packages-select <pkg> --symlink-install`.
- 빌드 후 반드시 `source install/setup.bash`. 새 패키지 추가 / 노드명 변경 시 재 source 필수.
- 프로젝트별 추가 cmake 인자(예: `-DROS_EDITION=...`, `-DHUMBLE_ROS=...`)는 워크스페이스 루트 `CLAUDE.md` 에서 정의한다.

## 설정 파일은 src 원본 사용

- rviz, yaml, JSON 등 설정 파일은 `install/share/...` 에 복사하지 않는다. **항상 src 폴더 원본을 수정**한다.
- launch 에서 경로 참조 시 `--symlink-install` 의존 또는 `get_package_share_directory()` 결과가 src 원본을 가리키도록 유지.

## COLCON_IGNORE 정책

- 의도적으로 빌드 제외된 디렉토리(ROS1 잔존, 외부 도구 빌드 트리, 미완성 패키지 등)는 IGNORE 제거 금지.
- 외부 빌드 시스템(예: PlatformIO 의 `.pio/`)은 colcon 빌드 대상이 아니다.

## 외부 드라이버 read-only 보호

- 외부 공식 저장소에서 가져온 vendored 코드는 수정 금지, config / launch overlay 만 변경 허용.
- 시스템 설치 라이브러리(`/usr/local/lib` 등)는 재컴파일·교체 금지.
- 수정이 불가피한 경우 wrapper 패키지 또는 launch overlay 로 처리.
- 구체 경로 목록은 [github.md](github.md) "Read-only 외부 vendored 저장소 가드" 와 워크스페이스 루트 `CLAUDE.md` / [`local/`](local/) 에서 정의한다.

## 임베디드 / 시리얼 함정 (사전 경고)

다음은 재현 빈도 높은 함정으로, 작업 시작 전 검토한다.

1. **시리얼 포트 점유 충돌**: `pio device monitor`, `cat /dev/ttyACM0`, 시리얼 브리지 노드 등이 동시에 같은 장치를 열 수 없다. 플래시 / 모니터 / 브리지 중 하나만 활성화한다 ([workflow.md](workflow.md) "펌웨어 다운로드 절차").
2. **장치 권한**: `/dev/ttyUSB*`, `/dev/ttyACM*` 접근 권한. `dialout` 그룹 가입 또는 udev 규칙 필요.
3. **Baud rate 불일치**: 펌웨어 빌드 설정과 호스트 측 시리얼 파라미터의 일치 필수. 프로젝트별 baud / framing 은 모듈 CLAUDE.md 에 명시한다.
4. **리셋 / 재연결 순서**: USB serial 재연결 시점에 보드 reset loop 또는 silent crash 가 발생할 수 있음. 호스트 측 자동 reconnect 동작과 충돌하지 않도록 수동 reset 시 호스트 노드 stop 권장.
5. **빌드 환경 함정**: PlatformIO `pio run` 만 입력하면 `[platformio]` 의 `default_envs` 가 빌드된다. 양산 펌웨어는 반드시 `pio run -e <env_name> -t upload` 로 명시한다.

## 실기·시험 기동 규율 (SIL/HIL)

본 절은 SIL (Software In the Loop) / HIL (Hardware In the Loop) 시험과 실기 구동에 공통 적용한다. 적용 시점은 측정 유무와 무관하게 **실기(실 하드웨어) 구동 전 전부**다. ROS2 는 동일 이름 노드의 중복 실행을 막지 않으므로(경고만) 기동 자체를 통제한다. 같은 토픽에 발행자가 2개 이상 생기면 이후 모든 측정이 무효다.

1. **정리 대상 선별 (2축)**: ⓐ 이번 절차가 띄울 **노드 이름**과 겹치는 것 (`ros2 node list`), ⓑ 측정·제어 대상 **토픽에 이미 발행자가 있는 것** (`ros2 topic info <topic> -v` — remap 으로 노드 이름이 달라도 잡힌다). 둘 중 하나라도 걸리면 종료한다(이전 launch 프로세스 포함). 그 외(드라이버·안전 감시·로깅 등)는 건드리지 않는다 — 전량 종료는 재기동 비용이 큰 하드웨어 초기화와 진행 중 기록을 함께 파괴한다.
2. **잔류 확인**: `ros2 node list` 는 daemon 캐시라 죽은 노드가 남거나 산 노드가 빠진다. `ps aux | grep -E 'ros2 launch|<실행 파일>'` 을 병행하고, 정리 후 `ros2 daemon stop && ros2 daemon start` 로 갱신해 재확인한다. 다중 호스트면 원격 노드는 해당 호스트에서 종료하거나 `ROS_DOMAIN_ID` 를 분리한다.
3. **고정 절차 기동**: 런치 파일은 **여러 개를 정해진 순서로** 올려도 된다(단일 런치로 합칠 필요 없음). 단 **절차서에 적힌 런치·순서 그대로만** 올리고, 절차에 없는 개별 `ros2 run` 을 얹지 않는다. 기동 절차 목록은 워크스페이스 루트 `CLAUDE.md` 또는 [`local/`](local/) 에 둔다.
4. **계층 얹기는 개발·디버그 한정**: 기존 그래프 위에 노드를 얹는 것 자체는 허용하되, 그 상태에서 나온 수치·판정은 **측정치로 보고 금지**. 기록 시 "얹기 상태"를 명시한다.
5. **기동 후 확인**: 측정 대상 토픽의 발행자 수가 기대값(보통 1)인지 `ros2 topic info <topic> -v` 로 확인한 뒤 측정한다.

근거: 2026-08-02 실사격 — `/mcl_pose` 발행자가 2개인 상태로 측정한 14.6 / 21.4 / 26.7 Hz 가 여러 인스턴스의 합계로 판명되어 전량 무효 처리 ([CHANGELOG.md](CHANGELOG.md) 1.16.0 트리거).

## 패키지 종류별 주의사항

| 패키지 종류 | 빌드 시스템 | 주의 |
|---|---|---|
| C++ | `ament_cmake` | `CMakeLists.txt` 의 `install(TARGETS ...)` 누락 시 설치 안 됨 |
| Python | `ament_python` | `setup.py` 의 `entry_points` 와 `package.xml` 동기화 필수 |
| 임베디드 | 외부 (예: PlatformIO) | colcon 영향 없음. 별도 빌드 사이클 |

## 모듈 CLAUDE.md 와의 관계

루트 / 본 가이드라인은 **워크스페이스 공통**(빌드 / launch / 토픽 / QoS / source / 외부 드라이버 경계). 모듈 CLAUDE.md 는 **하드웨어 핀맵·상수·외부 빌드 명령** 등 모듈 고유 규칙. 충돌 시 모듈 우선.

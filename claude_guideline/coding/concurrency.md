# coding/concurrency — 동시성 / 비동기 도메인 룰

상위: [coding/README.md](README.md) §10 (도메인 확장 인터페이스)

본 파일은 동시성 (threading · multiprocessing · async) 도메인 특화 룰. 상위 README §1~§9 와 충돌 없이 인벤토리·룰·체크리스트·평가 카테고리를 추가.

대상: C++ `std::thread` · `std::mutex` · `std::atomic`, Python `threading` · `multiprocessing` · `asyncio`, ROS 2 multi-threaded executor + callback group, FreeRTOS task.

---

## 1. 트리거 (자동 감지)

상위 [coding/README.md](README.md) §10.2 에 등록된 트리거 재명시:

- `threading`, `asyncio`, `multiprocessing` (Python)
- `std::thread`, `std::mutex`, `std::condition_variable`, `std::atomic`, `std::shared_mutex` (C++)
- `MutuallyExclusiveCallbackGroup`, `ReentrantCallbackGroup`, multi-callback ROS 노드
- `@asynccontextmanager`, `await`, `async def`
- `pthread_*`, FreeRTOS API (`xSemaphoreTake`, `xQueueSend`)

1개 이상 충족 시 본 도메인 활성. 다중 도메인 동시 활성 가능 (ros2 / embedded 와 함께).

---

## 2. 추가 인벤토리

상위 §9 (문서 양식) 의 함수표·변수표에 추가. 위치: `docs/<module>/concurrency.md` 또는 모듈 `docs/`.

### 2.1 동기화 객체 표

| # | 객체 | 종류 | 보호 자원 | 획득 위치 | 해제 위치 |
|---|---|---|---|---|---|
| 1 | `g_state_mtx` | `std::mutex` | `g_robot_state` | `state_update():84` | `state_update():91` |
| 2 | `data_ready_cv` | `std::condition_variable` | `g_queue` | `producer():42` | `consumer():18` |

종류 후보: Mutex / RecursiveMutex / SharedMutex(RWLock) / Spinlock / Lock / Event / Semaphore / Atomic / Condvar / Barrier / Latch.

### 2.2 공유 상태 표

| # | 변수 | 읽기 위치 | 쓰기 위치 | 보호 객체 |
|---|---|---|---|---|
| 1 | `g_robot_state` | `state_read()`, `controller_tick()` | `state_update()` | `g_state_mtx` |
| 2 | `g_counter` | `monitor_tick()` | `producer():120` | `std::atomic` (lock-free) |

보호 없으면 `"비보호"` 명시 — `[race]` 평가 카테고리 후보.

### 2.3 실행 컨텍스트 표

| # | 이름 | 종류 | 우선순위 / executor | 생성 위치 |
|---|---|---|---|---|
| 1 | `main_thread` | std::thread | normal | `main.cpp:18` |
| 2 | `sensor_task` | asyncio task | event loop | `sensor.py:42` |
| 3 | `motor_cb_group` | ROS callback group | MultiThreadedExecutor | `motor_node.cpp:60` |

종류: thread / task / coroutine / callback group / executor / worker pool.

### 2.4 채널 / 큐 표 (있을 시)

| # | 채널 | 종류 | 생산자 | 소비자 | 버퍼 크기 / backpressure |
|---|---|---|---|---|---|
| 1 | `cmd_queue` | `std::queue` + mutex | controller | motor_driver | 100, drop oldest |
| 2 | `image_q` | `asyncio.Queue(maxsize=5)` | camera_task | proc_task | 5, await on full |

---

## 3. 추가 룰

### 3.1 Race / 공유 상태

- 공유 상태는 **보호 객체 의무** — lock / atomic / immutable / 단일 thread 소유
- `volatile` 단독 사용 금지 (race 가드 부족 — 메모리 가시성만 보장, 원자성 X). 상위 [embedded/README.md](embedded/README.md) §3.2 정렬
- thread-local 가능한 경우 thread-local 우선
- 읽기-쓰기 비율 편향 시 `std::shared_mutex` / `RWLock` 검토

### 3.2 Lock 순서 / Deadlock

- 다중 lock 획득 시 **순서 일관성** (전역 순서 정의 의무 — 예: 주소 오름차순, 이름 알파벳, 명시적 ID)
- lock 해제는 RAII (`std::lock_guard`, `std::unique_lock`, Python `with`)
- `std::lock(m1, m2)` 또는 `std::scoped_lock` 으로 다중 lock 원자 획득
- 콜백 / 시그널 / observer 호출은 lock 외부에서 (재진입 dead-lock 회피)
- timeout 있는 `try_lock_for` / `wait_for` 권장 (무한 대기 회피)

### 3.3 Priority / Priority Inversion

- 우선순위 다른 thread 간 lock 공유 시 **priority inheritance** 또는 **priority ceiling** 사용
- 실시간 thread 는 mutex 사용 최소화 — atomic / lock-free 큐 / 더블 버퍼링 권장
- 상위 [embedded/README.md](embedded/README.md) §3.2 정렬

### 3.4 ISR ↔ Task (임베디드 동시 활성 시)

- ISR ↔ Task 통신은 ISR-safe API 만: `xQueueSendFromISR`, `xSemaphoreGiveFromISR`
- ISR 내 mutex / 일반 lock 금지 (priority inversion 위험)
- 자세한 ISR 룰은 [embedded/README.md](embedded/README.md) §3.1 따름

### 3.5 async / coroutine

- async 함수 내 **블로킹 호출 금지** (`time.sleep`, blocking I/O) — `asyncio.sleep`, `aiofiles` 등 async 등가물 사용
- `await` 사이의 상태는 race 가능 — `asyncio.Lock` 또는 task 단일 소유
- `asyncio.gather` 의 예외 전파 정책 명시 (`return_exceptions=True/False`)
- `Task` 누수 방지 — 모든 생성된 task 는 await 또는 cancel
- event loop 차단 함수는 `loop.run_in_executor` 로 thread pool 위임

### 3.6 multiprocessing

- 프로세스 간 공유는 `Queue` / `Pipe` / `shared_memory` / `Manager` 만
- pickle 가능 객체만 전달 (lambda · 로컬 함수 · 파일 핸들 금지)
- `fork` vs `spawn` 시작 방식 명시 (Linux fork 기본, Windows spawn)
- 자식 프로세스 종료 정책 (`join` / `terminate` / `kill`) 명시

### 3.7 콜백 / 옵저버

- 콜백 차단성 검토 — long-running (>10ms) 시 별도 thread / executor 위임
- 콜백 등록 / 해제는 lifetime 안전 (객체 소멸 후 콜백 호출 방지 — `weak_ptr` / `weakref`)
- 재진입 콜백 안전성: 재진입 가능 lock 또는 큐잉

### 3.8 ROS 2 Callback Group (ros2 도메인 동시 활성 시)

- multi-threaded executor + callback group 정책은 [ros2.md](ros2.md) §3.3 따름
- 본 파일은 callback group 내부의 공유 상태 / lock 룰만

### 3.9 테스트

- race / deadlock 재현은 **stress test** + **ThreadSanitizer** (`-fsanitize=thread`) / **AddressSanitizer**
- async 코드는 `pytest-asyncio` / `pytest-trio`
- 결정론적 테스트: 가능한 한 seed 고정 + barrier 동기화

---

## 4. 추가 종료 체크리스트

상위 §7 A/B/C/D 골격에 다음 항목 첨가.

### A. 기술 부채 방지 (동시성 특화)
- [ ] 공유 상태 모두 보호 (lock / atomic / immutable) — `[race]` 없음
- [ ] 다중 lock 획득 순서 정의 + 일관성 — `[deadlock]` 없음
- [ ] `volatile` 단독 보호 없음 (있으면 사유 + tech_debt.md)
- [ ] async 내 블로킹 호출 없음
- [ ] Task 누수 없음 (모두 await / cancel)
- [ ] ThreadSanitizer / pytest-asyncio 통과

### B. 이해 부채 방지 (동시성 특화)
- [ ] 동기화 객체 표 갱신 (§2.1)
- [ ] 공유 상태 표 갱신 (§2.2) — 비보호 항목 명시
- [ ] 실행 컨텍스트 표 갱신 (§2.3)
- [ ] 채널 / 큐 표 갱신 (§2.4, 있을 시)

### C. 의도 부채 방지 (동시성 특화)
- [ ] Lock 순서 정책 ADR (다중 lock 시)
- [ ] async vs thread vs process 선택 사유 ADR
- [ ] Priority 정책 ADR (priority inversion 위험 시)

### D. 위반 / 예외 / 인계 (동시성 특화)
- [ ] 비보호 공유 상태 사유 (있으면 tech_debt.md)
- [ ] long-running callback 사유

---

## 5. 평가 카테고리 (인라인 태그)

[code_review.md](../code_review.md) Add-on B 와 정합.

- `[race]` — 공유 변수 비보호 쓰기, race condition 후보
- `[deadlock]` — 다중 lock 획득 순서 일관성, 순환 의존
- `[timing]` — 콜백 차단성, 시간 budget, jitter
- `[reentrant]` — 재진입 가능 콜백에서 비-reentrant 호출
- `[priority]` — Priority inversion 위험
- `[async]` — async 내 블로킹 / Task 누수 / await 사이 상태 race
- `[mp]` — multiprocessing pickle / fork-spawn / 종료 정책
- `[atomic]` — atomic 사용 적합성 (memory_order, lock-free 가정)

---

## 6. 다른 도메인과의 의존 / 충돌

- **ros2**: multi-threaded executor + callback group. executor 선택은 [ros2.md](ros2.md) §3.3 권위. 본 파일은 그룹 내부의 race / lock 룰만.
- **embedded**: ISR ↔ Task 통신 + RTOS task. ISR 룰 · WCET · ISR-safe API 는 [embedded/README.md](embedded/README.md) §3.1, §3.4 권위. 본 파일은 Task 간 동기화·shared state.
- 충돌 시 우선순위: 상위 [coding/README.md](README.md) > ros2 / embedded > 본 파일 (concurrency 가 가장 일반). 즉 ROS 2 callback group 내부 동작은 ros2 가, ISR 룰은 embedded 가 우선.

---

## 7. 자체 점검 grep

```bash
TARGET=docs/<module>/concurrency_review.md  # 또는 docs/code_review/<주제>.md

# 1. 동기화 객체 표
grep -E "객체.*종류.*보호 자원" $TARGET

# 2. 공유 상태 표
grep -E "변수.*읽기 위치.*쓰기 위치.*보호 객체" $TARGET

# 3. 실행 컨텍스트 표
grep -E "이름.*종류.*(우선순위|executor)" $TARGET

# 4. 비보호 항목 검출
grep -E "\"비보호\"|보호 없음" $TARGET

# 5. 평가 태그
grep -oE "\[(race|deadlock|timing|reentrant|priority|async|mp|atomic)\]" $TARGET | sort -u
```

---

## 룰 (요약)

1. **공유 상태는 보호 객체 의무** §3.1 — `volatile` 단독 금지
2. **Lock 순서 일관성** §3.2 — 전역 순서 정의 + RAII
3. **Timeout 있는 lock / wait** §3.2 — 무한 대기 회피
4. **Priority inheritance / ceiling** §3.3 — 우선순위 다른 thread 공유 lock 시
5. **async 내 블로킹 금지** §3.5 — async 등가물 사용
6. **Task 누수 방지** §3.5 — 모두 await / cancel
7. **multiprocessing pickle 가능 객체만** §3.6
8. **콜백 차단성 검토** §3.7 — long-running 은 위임
9. **ThreadSanitizer / pytest-asyncio 통과** §3.9
10. **ISR 룰은 embedded 우선** §6 — `[ISR]` 은 embedded
11. **ROS callback group 정책은 ros2 우선** §6
12. **본 README 와 충돌 금지** — 상위 [coding/README.md](README.md) §1~§9 가 권위

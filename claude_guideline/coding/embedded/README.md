# coding/embedded — 임베디드 / RTOS 공통 룰

상위: [coding/README.md](../README.md) §10 (도메인 확장 인터페이스)

본 파일은 임베디드 도메인의 **공통** 룰. MCU 별 특화 (Infineon AURIX · Arduino · STM32 · ESP32 등) 는 향후 `embedded/<mcu>.md` 로 plug-in (상위 §10.6 서브-도메인 재귀).

본 README §1~§9 (공통 SOP) 와 충돌 없이 임베디드 도메인 특화 인벤토리·룰·체크리스트·평가 카테고리를 추가.

---

## 1. 트리거 (자동 감지)

상위 [coding/README.md](../README.md) §10.2 에 등록된 트리거 재명시:

- `__attribute__((interrupt))`, `ISR(`, `NVIC_`, `IRQHandler`
- FreeRTOS API (`xTaskCreate`, `xQueueSend`, `vTaskDelay`, `xSemaphoreTake`)
- STM32 HAL 매크로 (`HAL_*`)
- `.ld` linker script
- register-level access (`*((volatile uint32_t*)0x...)`)
- `volatile` 빈출 (파일당 10+회)

1개 이상 충족 시 본 도메인 활성. 사용자 명시 지정 시 그것 우선.

---

## 2. 추가 인벤토리

상위 §9 (문서 양식) 의 함수표·변수표에 추가하여 임베디드 특화 표 작성. 위치: `docs/embedded/` 또는 모듈 `docs/`.

### 2.1 ISR / 인터럽트 표

| # | 벡터 이름 | NVIC 우선순위 | 사용 자원 (레지스터 · 전역) | WCET (μs) | 위치 (file:line) |
|---|---|---|---|---|---|
| 1 | `TIM2_IRQHandler` | 5 | `g_timer_cnt`, `TIM2->SR` | 12 | `timer.c:84` |

### 2.2 Task / Thread 표

| # | 이름 | 우선순위 | stack (bytes) | 주기 (또는 event) | 위치 |
|---|---|---|---|---|---|
| 1 | `motor_ctrl_task` | osPriorityHigh | 2048 | 1 kHz | `motor.c:42` |

### 2.3 공유 자원 표 (ISR ↔ Task / Task ↔ Task)

| # | 자원 | 사용 ISR / Task | 보호 메커니즘 |
|---|---|---|---|
| 1 | `g_adc_buffer` | TIM2 ISR + adc_proc_task | DMA-double-buffer + atomic flag |

보호 메커니즘 후보: `disable IRQ` / `semaphore` / `mutex` / `atomic` / `volatile` (volatile 단독은 §3.2 위반).

### 2.4 하드웨어 인터페이스 표 (페리페럴)

| # | 페리페럴 | 핀맵 | 속도 / 모드 | 드라이버 위치 |
|---|---|---|---|---|
| 1 | UART2 | PA2/PA3 | 115200 8N1 | `bsp_uart.c:18` |
| 2 | SPI1 | PA5/PA6/PA7 | 10 MHz, mode 0 | `bsp_spi.c:12` |

핀맵·속도·모드 변경은 사전 승인 트리거 (상위 §1.2 "하드웨어 인터페이스").

### 2.5 메모리 맵 / Linker (선택)

플래시·SRAM·DTCM·CCM·외부 RAM 의 섹션 배치. MCU 별로 상세가 달라 `embedded/<mcu>.md` 로 위임 권장. 본 README 는 변경 시 ADR 의무만 강제.

---

## 3. 추가 룰

### 3.1 ISR 룰

- ISR 내 **블로킹 호출 금지** (mutex lock, vTaskDelay 등)
- ISR 내 **malloc / free / printf 금지** (heap 잠금 · stack 폭주)
- ISR ↔ Task 통신은 **queue / semaphore / atomic** 만 사용
- NVIC 우선순위 정책 명시 (선점 우선순위 vs 서브 우선순위 분리)
- **WCET 예산** ADR 기재 (상위 §9.4): 최대 실행 시간 추정 + 측정 방법

### 3.2 동기화

- `volatile` 단독 사용 금지 — race 가드 부족. atomic / disable IRQ / lock 동반
- 다중 lock 획득 순서 일관성 (deadlock 방지)
- Priority inversion 회피 — priority inheritance 또는 priority ceiling
- ISR 콜백에서 사용하는 자원은 ISR-safe API 만 (FreeRTOS `xQueueSendFromISR` 등)

### 3.3 메모리 / DMA

- DMA 버퍼는 **정렬 의무** (32-byte 권장) + cache 동기화 (`SCB_CleanDCache` / `SCB_InvalidateDCache`)
- DMA 버퍼는 캐시 가능 영역 vs 비캐시 영역 명시
- Task stack 크기 명시 + **stack overflow 가드** (FreeRTOS configCHECK_FOR_STACK_OVERFLOW)
- heap 사용 최소화 (가능하면 static 할당)

### 3.4 페리페럴 / HAL

- 핀맵·속도·모드 변경은 **사전 승인 트리거** (상위 §1.2)
- HAL (`HAL_*`) vs LL (`LL_*`) vs 레지스터 직접 접근의 **일관성** 유지 (모듈 내 혼용 금지)
- 페리페럴 초기화 실패 시 fallback 또는 안전 정지 명시 (상위 §1 의존성 3-tier "런타임 필수" 정렬)

### 3.5 빌드 / 플래시 / 검증

- cross-compile 검증 의무 (toolchain · `arm-none-eabi-gcc` 등 명시)
- flash + boot + 초기 안정 동작 (10초 이상) 검증
- ELF 심볼 사이즈 회귀 추적 (`.text` · `.data` · `.bss` · stack peak)
- SHIL 테스트 (상위 §5) 는 host 빌드 + on-target 양쪽 권장

---

## 4. 추가 종료 체크리스트

상위 §7 A/B/C/D 골격에 다음 항목 첨가.

### A. 기술 부채 방지 (임베디드 특화)
- [ ] ISR 내 블로킹 · malloc · printf · 긴 작업 없음
- [ ] WCET 예산 ADR 기재 (안전 분기 함수)
- [ ] DMA 버퍼 정렬 + cache 동기화
- [ ] Task stack 사용량 측정 (high-water mark)
- [ ] `volatile` 단독 사용 없음 (있으면 사유 + tech_debt.md)
- [ ] ELF 사이즈 회귀 확인

### B. 이해 부채 방지 (임베디드 특화)
- [ ] ISR 표 갱신 (§2.1)
- [ ] Task 표 갱신 (§2.2)
- [ ] 공유 자원 표 갱신 (§2.3)
- [ ] 페리페럴 표 갱신 (§2.4)
- [ ] 메모리 맵 변경 시 ADR + 표 갱신 (§2.5)

### C. 의도 부채 방지 (임베디드 특화)
- [ ] 페리페럴 핀맵·속도·모드 변경 → ADR (사전 승인 트리거)
- [ ] NVIC 우선순위 변경 → ADR
- [ ] HAL vs LL 선택 사유 기록
- [ ] 데이터시트 · 매뉴얼 인용 (상위 §1.4) — 페이지·절 명시

### D. 위반 / 예외 / 인계 (임베디드 특화)
- [ ] `volatile` 단독 · ISR 내 긴 작업 등 위반은 사유 + tech_debt.md 등록

---

## 5. 평가 카테고리 (인라인 태그)

코드 리뷰 / 종료 체크리스트 / 보고 시 사용. [code_review.md](../../code_review.md) Add-on C 와 정합.

- `[prio]` — Priority inversion, 우선순위 정책 위반
- `[ISR]` — ISR 내 블로킹 · malloc · printf · 긴 작업
- `[WCET]` — 인터럽트 latency · 응답성 budget 초과
- `[volatile]` — `volatile` 단독 보호 부족
- `[DMA]` — DMA 정렬 / cache 동기화 누락
- `[HW]` — 핀맵 · 속도 · 모드 변경 (사전 승인 트리거)
- `[stack]` — Task stack overflow · 사용량 미측정
- `[mem]` — 메모리 맵 · linker · 섹션 배치
- `[boot]` — 부팅 / 초기화 / fallback 부재

---

## 6. 다른 도메인과의 의존 / 충돌

- **concurrency 도메인 동시 활성**: ISR ↔ Task 가 본질적으로 concurrency. lock 순서 / race / async 룰은 [coding/concurrency.md](../concurrency.md) 따름. 본 파일은 ISR 특화 (atomic / disable IRQ / ISR-safe API) 만 정의.
- **ros2 도메인 동시 활성**: micro-ROS (rclc) 사용 시. QoS · executor 룰은 [coding/ros2.md](../ros2.md) 따름. 본 파일은 페리페럴·ISR·WCET 만.
- 충돌 시 우선순위: 상위 [coding/README.md](../README.md) > 도메인 파일. 도메인 간 충돌은 사용자 결정.

---

## 7. 자체 점검 grep

```bash
TARGET=docs/<module>/embedded_review.md  # 또는 docs/code_review/<주제>.md

# 1. ISR 표 헤더
grep -E "벡터 이름.*NVIC 우선순위.*WCET" $TARGET

# 2. Task 표 헤더
grep -E "이름.*우선순위.*stack" $TARGET

# 3. 공유 자원 표 헤더
grep -E "자원.*ISR.*보호 메커니즘" $TARGET

# 4. 페리페럴 표 헤더
grep -E "페리페럴.*핀맵.*속도" $TARGET

# 5. 평가 카테고리 태그
grep -oE "\[(prio|ISR|WCET|volatile|DMA|HW|stack|mem|boot)\]" $TARGET | sort -u
```

---

## 8. 서브-도메인 (향후 plug-in)

MCU 별 특화는 본 폴더 내 별도 파일로 (상위 §10.6 서브-도메인 재귀):

| 파일 | 대상 | 트리거 예 |
|---|---|---|
| `aurix.md` | Infineon AURIX | `<Ifx_Types.h>`, `Cpu0_Main.c`, `.dsl`, Tasking 컴파일러 |
| `arduino.md` | Arduino (AVR / SAMD) | `void setup()` + `void loop()`, `<Arduino.h>`, `platformio.ini` env arduino |
| `stm32.md` | STM32 | `stm32f4xx_hal.h`, `HAL_*` 매크로, `.ioc` (CubeMX) |
| `esp32.md` | ESP32 | `esp_log.h`, `freertos/FreeRTOS.h`, `idf.py`, `sdkconfig` |

각 서브 파일은 상위 §10.3 의 **5요건** 충족 + 본 README 의 §1 트리거 표에 자체 등록.

본 절은 확장 가능 근거만 명시. 실제 서브-도메인 파일은 필요 시점에 별도 작성.

---

## 룰 (요약)

1. **ISR 내 블로킹 · malloc · printf 금지** §3.1
2. **WCET 예산 ADR** — 안전 분기 함수 §3.1
3. **volatile 단독 금지** §3.2 — atomic / disable IRQ / lock 동반
4. **DMA 버퍼 정렬 + cache 동기화** §3.3
5. **Task stack 측정 + overflow 가드** §3.3
6. **핀맵 · 속도 · 모드 변경은 사전 승인 트리거** §3.4 (상위 §1.2)
7. **HAL vs LL 일관성** §3.4 — 모듈 내 혼용 금지
8. **데이터시트 · 매뉴얼 인용 의무** §4 C (상위 §1.4)
9. **다른 도메인 충돌 시 상위 룰 우선** §6 — concurrency · ros2
10. **본 README 와 충돌 금지** — 상위 [coding/README.md](../README.md) §1~§9 가 권위

---
name: manual-first
description: "매뉴얼/Datasheet 1차 source 참조 강제. 키워드 (datasheet, 데이터시트, manual, 매뉴얼, spec, 사양, Operation Conditions, Electrical Characteristics, 위반, 초과, non-compliance, violation, 무보증) 감지 시 자동 활성. 벤더 SDK/드라이버 매크로 → silicon (또는 device) spec 비약 금지."
argument-hint: "(자동 트리거 — 명시적 호출 시 인자 불필요)"
---

# Manual-First Datasheet Verification Rule (Auto-Load)

본 스킬은 외부 spec/datasheet 분석 시 거짓 단정 누적을 방지하기 위한 강제 룰. 다음 키워드 또는 작업 컨텍스트 감지 시 자동 활성:

- `datasheet`, `데이터시트`, `manual`, `매뉴얼`
- `spec`, `사양`, `Operation Conditions`, `Electrical Characteristics`
- `INL`, `DNL`, `ENRMS` 등 일반 spec 파라미터
- `AEC-Q100`, `ISO`, `IEEE`, `UL`, `UN` 등 외부 표준 / 인증
- spec 한계 논의에서의 단위 (`MHz`, `kHz`, `V`, `A`, `Ω` 등)
- `위반`, `초과`, `non-compliance`, `violation`, `무보증`, `fail`

본 스킬의 SSOT 룰: [`claude_guideline/manual.md`](../claude_guideline/manual.md). 본 파일은 자동 트리거 진입점 + 핵심 요약.

---

## 핵심 규칙 (3 줄 요약)

1. **벤더 SDK / 드라이버 매크로 ≠ silicon (또는 device) datasheet spec** — 둘은 별개로 검증
2. **1차 source (datasheet PDF) 없이 강한 단정어 ("위반", "초과", "무보증") 사용 금지**
3. **`manual/` (또는 `docs/manual/<vendor>/<product>/`) 가장 먼저 확인 → 없으면 사용자에게 요청 후 진행**

---

## 작업 전 체크리스트

- [ ] 본 작업이 외부 spec / datasheet / 표준에 의존하는가?
- [ ] 의존하면 1차 source (datasheet PDF) 정해진 위치에 있는가?
- [ ] 없으면 사용자에게 다운로드 요청 → **받기 전 spec 관련 결론 보류**
- [ ] 기존 문서 / AI 보고에 검증 안 된 spec 주장 있는가? (있으면 격하)

## 작업 중 룰

- 검증 등급 강제: **✓** (1차 source 직접) / **ⓦ** (다른 보고만) / **⚠** (UNVERIFIED)
- ✓ = file:line 또는 datasheet:page 인용 필수
- SDK / 드라이버 매크로 인용 시 "silicon (또는 device) spec 아님" 명시
- 강한 단정어 ("위반", "fail", "non-compliance" 등) = primary source page+table 인용 시에만

## 작업 후 체크리스트

- [ ] 모든 ✓ 항목 인용 있는가?
- [ ] SDK / 드라이버 매크로 → silicon spec 비약 있는가? (있으면 ⚠ 격하)
- [ ] 강한 단정어 = primary source 첨부?
- [ ] 정정 이력 명시?
- [ ] 미해결 ⚠ 항목 사용자에게 보고?

---

## Datasheet 다운로드 절차

1. `manual/` 먼저 확인
2. WebSearch 로 PDF URL
3. `curl -sSL -A "Mozilla/5.0" -o manual/<file>.pdf <URL>` 시도
4. 차단 시 미러 (mouser/farnell/alldatasheet) 또는 사용자 수동 다운로드
5. `file manual/<file>.pdf` 로 valid PDF 확인 (HTML 차단 페이지 X)
6. `pdftotext -layout <file>.pdf <file>.txt`
7. `grep` 으로 spec parameter 검색 → 컨텍스트 발췌

---

## 도입 사례 (왜 본 룰이 필요한가) — 추상화

대표 위반 패턴:

1. AI 가 벤더 SDK 의 `<PARAMETER>_MAX` 매크로를 보고 silicon datasheet spec 으로 비약
2. "datasheet 위반" 거짓 단정 → "외부 표준 (AEC-Q100 등) 위반", "정밀도 무보증" 등 downstream 거짓 결론 누적
3. 후속 검증/협업 워크플로 (병렬 워커, 외부 도구 등) 가 거짓 전제 위에서 작동 → 토큰 / 시간 낭비
4. 사용자가 datasheet PDF 직접 다운로드 후 진실 확인 → spec 안쪽 정상 (TYP 근방), SDK 매크로는 SW 보수 한계였을 뿐

본 사례 결과로 SSOT [`claude_guideline/manual.md`](../claude_guideline/manual.md) 강화 (사전/사후 체크리스트 + 검증 등급 + 다운로드 절차 + 위반 사례 추상화 추가) + 본 스킬 등록. 프로젝트별 구체 사례는 해당 프로젝트의 case study 파일에 보존.

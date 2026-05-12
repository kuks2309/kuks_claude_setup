# 사용자 지시 분석 SSOT (Step 2)

> **상태**: v0.3 — 일상 지시용 빠른 점검 3 항목. v0.2 의 5-stage / 6-차원 / 4-way 결정은 *연구성 작업* 용으로 분리 예정 (`research_subroutine.md`, TBD).

## 본 SSOT 의 목적 — 인지 부채(Cognitive Debt) 방지

사용자 지시 처리의 2 단계 메타 워크플로 중 **Step 2 (분석)**. 기록만 하고 분석 없이 진행하면 "엉터리 작업" ([본 세션 #19 지적](../../docs/user_instructions/user_instructions.md)).

분석은 **경량** — 매 지시마다 짧은 점검, 큰 결정 시에만 별도 절차 진입.

| Step | 이름 | 차단 부채 | SSOT |
|------|------|----------|------|
| 1 | 기록 | 의도 부채 | [user_instruction_handling_sop.md](user_instruction_handling_sop.md) |
| **2** | **분석** | **인지 부채** | **본 파일** |

## 빠른 점검 (3 항목)

매 지시 도착 시 다음 3 가지를 빠르게 점검 후 실행 진입.

### 1. 의도 명확성

의도가 명확한가? 모호하면 사용자에게 **1 줄 질문** 후 답변 대기. 추측 진행 금지.

### 2. 기존 자료 (grep 한 번)

동일·유사 작업·실수가 본 프로젝트에 이미 있는가? 다음 위치 빠르게 grep:

- `docs/user_instructions/user_instructions.md` — 지시 이력
- `docs/worklog/` — 과거 작업
- `docs/claude-mistake/INDEX.md` — 반복 실수 카탈로그

발견 시 사용자에게 1 줄 보고 후 진행 방향 (재사용 / 갱신 / 신규) 확정.

### 3. 외부 자료 필요성

본 프로젝트 자료만으로 부족한가? 그렇다면:

1. `manual/`, `docs/manual/`, `<package>/manual/` — 1차 source
2. 부재 시 공식 웹 / GitHub / MCP (Context Hub, `document-specialist` 등)

인용 의무: `file:line` 또는 URL + 발췌. 출처 없는 spec 단정 금지.

## 큰 결정 시 (외부 자산 채택·새 SSOT·분류 시스템 설계)

위 3 항목으로 부족한 *연구성 작업* — 별도 SSOT 의 5-stage 검증 절차 적용:

- (TBD) `research_subroutine.md` — Preflight → Need Analysis → Parallel Search → Evaluate (6 차원) → Decide (Adopt/Extend/Compose/Build) → Implement
- 잠정: [ECC `skills/search-first/SKILL.md`](https://github.com/affaan-m/everything-claude-code/blob/main/skills/search-first/SKILL.md) 직접 참조 (MIT)

## 후속 작업 (v0.4+ 후보)

- `research_subroutine.md` SSOT 분리 — 큰 결정용 5-stage / 4-way / 6-차원 평가 이전
- SOP `user_instruction_handling_sop.md` §1 흐름도에 본 SSOT 진입점 명시
- 본 SSOT 의 docs/claude_guideline/ 로컬 사본 sync

## 변경 이력

- **v0.3** (2026-05-13) — 5-stage / 6-차원 / 4-way 결정 제거, 일상 지시용 3 항목 점검으로 축소. 연구성 작업 절차는 `research_subroutine.md` 로 분리 예정.
- **v0.2** (2026-05-13) — ECC `search-first` 5-stage 차용 (3-5 단계 추가). 매 지시 적용 시 과도하다는 사용자 피드백으로 v0.3 축소 결정.
- **v0.1** (2026-05-11) — 1·2 단계 (기존 기록 + 매뉴얼/외부) 초안.

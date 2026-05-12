# 사용자 지시 분석 SSOT (Step 2)

> **상태**: 초안 v0.2 — 1~5 단계 정의 (ECC `search-first` 5-stage 차용). 추가 단계 후속.

## 본 SSOT 의 목적 — 인지 부채(Cognitive Debt) 방지

사용자 지시 처리의 2 단계 메타 워크플로 중 **Step 2 (분석)** 의 절차 SSOT.

| Step | 이름 | 차단 부채 | SSOT |
|------|------|----------|------|
| 1 | 기록 | 의도 부채 (Intent Debt) | [user_instruction_handling_sop.md](user_instruction_handling_sop.md) |
| **2** | **분석** | **인지 부채 (Cognitive Debt)** | **본 파일** |

기록만 하고 분석 없이 진행하면 "엉터리 작업" — 사용자 #19 (2026-05-11 04:30 KST) 지적.

## 분석 절차

사용자 지시 도착 시 다음 순서로 분석한다.

### 1 단계 — 기존 기록 검토 (유사한 내용 찾기)

같은 또는 유사한 지시가 과거에 있었는지 확인. 발견 시 (a) 재실행 금지, (b) 기존 결과 재사용, (c) 과거 실수 회피.

검토 대상:

| # | 위치 | 무엇을 찾는가 |
|---|------|-------------|
| 1 | `docs/user_instructions/user_instructions.md` | 동일·유사한 지시 원문 (grep, 시간 역순) |
| 2 | `docs/worklog/` | 같은 영역의 과거 작업 기록 |
| 3 | `docs/claude-mistake/` | 같은 영역의 과거 실수 (INDEX.md §메타 패턴·§미해결 우선 훑기) |
| 4 | `docs/code_review/`, `docs/analysis/`, `docs/issues_and_fixes/` | 분야별 누적 분석·이슈 |
| 5 | `~/.claude/projects/<project>/memory/` | 크로스 세션 feedback / 학습 |

발견 항목이 있으면 사용자에게 1 줄 보고 후 진행 방향 확정 ("기존 결과 재사용 / 갱신 / 신규 진행" 중 어느 것인지).

### 2 단계 — 관련 매뉴얼 검토 (부재 시 외부 조사)

지시가 외부 spec / 도메인 지식 / 신규 라이브러리 / 새 도구를 요구하면 1차 소스를 먼저 확인. 매뉴얼 부재 시에만 외부 조사로 fallback.

**검토 순서**:

1. 매뉴얼 폴더 검토 (프로젝트 로컬 1차 source):
   - `manual/` (프로젝트 루트 또는 모듈 루트) — datasheet PDF, vendor doc, 1 차 spec
   - `docs/manual/` 또는 `<package>/manual/` — 프로젝트별 로컬 매뉴얼
2. 매뉴얼 부재 시 외부 자료 조사:
   - 공식 웹 문서 (vendor site, official spec / API reference)
   - GitHub (관련 라이브러리 README, issue, example, release notes)
   - Context Hub / MCP 활용 가능 (`chub`, `document-specialist` 에이전트, `context7` 등)

인용 규칙: 매뉴얼은 `file:line` 또는 `datasheet:page`, 외부 자료는 URL + 발췌. 출처 없는 spec 단정 금지.

> **병렬화 권고**: 1단계와 2단계는 독립적이므로 동시 실행 가능 (ECC `search-first` Phase 2 의 parallel search 패턴).

### 3 단계 — 발견 자료 평가 (스코어링)

1·2단계에서 발견된 자료(기존 기록 + 외부 자료) 각각을 다음 6 차원으로 평가. ECC `search-first` Phase 3 (Evaluate) 차용.

| 차원 | 질문 | 비중 |
|------|------|------|
| **기능 적합성** | 본 지시가 요구하는 기능을 얼마나 cover? | HIGH |
| **유지보수성** | 최근 업데이트, 활발한 commit, 안정 버전? | HIGH |
| **커뮤니티/검증** | star/fork/contributor, PR 활동 (SSOT 인 경우 도입 프로젝트 수) | MEDIUM |
| **문서 품질** | README, 예제, API 문서 명확성 | MEDIUM |
| **라이선스** | 본 프로젝트와 호환 (MIT/Apache 우선, GPL 주의) | HIGH (gate) |
| **의존성** | 외부 MCP/env/도구 강결합? air-gapped fallback 가능? | HIGH |

**검증 의무**: 자료 의 self-reported 메타(README 카운트, "X stars" 등) 는 `gh api` 또는 동등 1차 source 로 cross-check. drift 발견 시 신뢰도 격하.

### 4 단계 — 결정 (Adopt / Extend / Compose / Build)

3단계 평가 결과를 다음 4-way 분기로 결정. ECC `search-first` Phase 4 (Decide) 차용.

| 분기 | 조건 | 산출물 |
|------|------|--------|
| **Adopt as-is** | 정확 일치 + 유지보수 양호 + 라이선스 호환 | 자료 채택, 본 SSOT 에 참조 등록 |
| **Extend / Wrap** | 부분 일치 + 좋은 기반 | 자료 채택 + 본 프로젝트 어댑터/래퍼 작성 |
| **Compose** | 약한 후보 다수 | 2-3 개 결합, 결합 SSOT 작성 |
| **Build custom** | 적합 후보 없음 (탐색은 했으니 정보 기반) | 자체 작성, 발견 자료를 영감/참조로 명시 |

**Gate**: 4-way 결정이 모호하면 사용자에게 평가 결과 1줄 보고 후 분기 확정 의무 (자율 결정 금지).

### 5 단계 — Step 3 (실행) 진입 브리지

4단계 결정 산출물을 Step 3 (실행) 으로 인계. ECC `search-first` Phase 5 (Implement) 차용 + 본 SOP Step 5 (사전 승인) 게이트 통합.

**산출물 형식**:

```markdown
## 분석 산출물 (Step 2 → Step 3)
- 지시 원문: <user_instructions.md entry ref>
- 분석 결과:
  - 작업 유형: <bug/feature/refactor/...>
  - 도메인: <ROS2/embedded/web/docs/...>
  - 결정 분기: <Adopt|Extend|Compose|Build>
  - 채택 자료: <list with refs>
- 사전 승인 트리거: <코드 수정? sub-agent 3+? push? 새 폴더?> → STOP 여부
- 실행 계획 1줄: ...
```

본 산출물이 SOP Step 5 (사전 승인) 의 입력. 트리거 해당 시 STOP, 사용자 승인 후 Step 6 진입.

## 입력 자료 (분석 재료)

- [docs/projects_analysis/instruction_classification_analysis.md](../../docs/projects_analysis/instruction_classification_analysis.md) — D1-D13 차원 + 10 통찰 + 8 anti-pattern (562줄)
- [request_giving.md](../../docs/claude_guideline/request_giving.md) — 사용자 측 지시 작성 가이드 (분석 절차의 대응 면)

## 출처 / 차용

본 5-stage 절차는 **ECC `skills/search-first/SKILL.md`** (https://github.com/affaan-m/everything-claude-code, MIT) 의 5-Stage 워크플로 (Preflight/Need Analysis/Parallel Search/Evaluate/Decide/Implement) 를 본 프로젝트의 1·2 단계 (기존 기록 + 매뉴얼·외부) 와 통합·재정렬한 결과. 검증 이력: `gh api` 로 실제 자산 카운트 cross-check, license MIT 확인 (2026-05-13).

차용 시점 권고: 외부 자산 self-reported 메타데이터 (README 카운트 등) 는 1차 source (`gh api`, 공식 spec) 로 검증 후 채택.

## 후속 작업 (v0.3+ 추가 단계 예정)

다음 차원·메커니즘은 방법론 연구 후 본 SSOT 에 추가:

- 작업 유형 분류 (D1: bug/feature/refactor/...) — 3단계 평가 차원 추가 또는 별도 단계
- 도메인 식별 (D2) + 가역성·위험 등급 (D4)
- 모호어 검출 (D7 vocabulary_alignment) — anti-pattern 8 종 매핑
- 반복성·anti-pattern 감지 (D5) / 문서 분류 적합성 (D12)
- 분석 실패 시 fallback (사용자에게 무엇을 묻는가)
- SOP `user_instruction_handling_sop.md` §1 흐름도에 본 SSOT 진입점 통합

---

**Note**: 후속 단계 추가 시 본 문서 v0.3+ 로 minor bump + CHANGELOG 갱신 + README.md 진입점 표에 행 추가 + SOP §1 흐름도 연결.

# Claude 실수 기록

Claude (LLM 어시스턴트) 가 본 프로젝트 작업 중 일으킨 **실수** 와 그 사유, 재발 방지책을 누적 기록한다. 동일한 실수의 반복을 막고, 후속 세션이 학습 자료로 활용한다.

## 본 SSOT 범위

본 폴더는 **실수** 를 기록한다. 실수는 가이드라인에 명시 규칙이 없거나 모호한 영역에서의 잘못된 판단·추측을 가리킨다.

**포함 사례**

- 매뉴얼·데이터시트·SDK 문서 오독
- 코드·환경·도구 동작에 대한 검증 없는 가정
- 필요한 컨텍스트 (기존 자료·세션 히스토리·관련 파일) 조사 누락
- 모호한 사용자 표현을 질문 없이 추측

**해결 방향**: 지식·컨텍스트 보강 (가이드라인 신규 작성, 메모리 추가, 매뉴얼 인용 보강).

**범위 외**: 가이드라인에 명시된 규칙을 어긴 사건은 본 폴더의 기록 대상이 아니다 — 해결 방향이 "강제 메커니즘 보강" 으로 본질이 달라지므로 별도 기록 체계가 필요하다.

**Boundary 판정**: 한 사건이 본 폴더 범위 (지식 공백) 와 명시 규칙 위반에 모두 해당하면 본 폴더의 기록 대상이 아니다 — 명시 규칙이 1+ 어겨졌다면 "지식 공백" 으로 분류하지 않고 별도 체계 (규칙 위반 기록) 에서 다룬다.

## 책임 경계 (필독)

본 폴더 (`kuks_claude_setup_new/claude-mistake/`) 는 **일반화 SSOT** — 형식·규칙·운용 가이드만 둔다.

- **여기에 두는 것**: `README.md` (본 파일), 형식 변경 이력
- **여기에 두지 말 것**: 실제 사건 entry (`YYYY-MM-DD.md`), 카테고리 인덱스 (`INDEX.md`), 프로젝트별 closure 데이터
- **사건 entry 작성 위치**: 각 다운스트림 프로젝트의 `docs/claude-mistake/YYYY-MM-DD.md`. 본 SSOT 폴더에 사건을 작성하면 다른 프로젝트에 무관한 사건이 노출되는 책임 경계 침범.

## 파일 구조

- **한 사건 = 한 파일** — 한 파일 안에 다중 entry 금지. 표준 markdown frontmatter 파서는 파일 최상단 1 블록만 인식하므로, 다중 entry 시 2 번째부터의 YAML frontmatter 가 본문 텍스트로 처리되어 INDEX 자동 생성·grep 분석에 누락된다.
- **파일명**: `YYYY-MM-DD-NNN.md` 또는 `YYYY-MM-DD-NNN_<짧은제목>.md` (NNN 은 같은 날 순번 `001`+)
- **시간순 누적**: 폴더 내 파일명 정렬로 자연 보장 (최신 = 가장 큰 NNN). 별도 prepend 작업 불필요.

## 항목 형식

각 파일은 YAML frontmatter (4 필드) + 본문 5 절로 구성된다.

````markdown
---
id: YYYY-MM-DD-NNN
category: manual-misread | wrong-assumption | context-missing | intent-guess
status: open | closed
reflected_assets:
  - <가이드라인/메모리/체크리스트 링크>
---

# YYYY-MM-DD HH:MM (KST) — <짧은 제목>

## 무엇을 했는가
Claude 가 시도한 행동 / 작성한 내용을 객관적으로 기술.

## 무엇이 잘못이었나
어떤 결과가 발생했는지, 어떤 의도와 어긋났는지.

## 사용자 지적
사용자가 어떻게 교정했는지 (인용 또는 요약).

## 사유 / 가설
Claude 가 왜 그 실수를 했는지. §카테고리 정의 enum 1 개로 분류한 뒤, 그 분류를 뒷받침하는 1~2 문단을 적는다.

## 재발 방지
같은 실수를 막기 위해 무엇을 바꿔야 하는지. `reflected_assets` 에 등재한 자산의 갱신 위치 (앵커 포함) 를 명시.

> `status: open` 일 때는 본 절 마지막에 `**owner**: claude | user | auto-rule` 한 줄을 부착해 closure 책임자를 명시한다. `closed` entry 에는 부착하지 않는다.
````

## Frontmatter 필드 정의

| 필드 | 필수 | 값 |
|------|------|---|
| `id` | 예 | `YYYY-MM-DD-NNN` (같은 날 사건은 NNN 증가) |
| `category` | 예 | 아래 §카테고리 정의 enum 4 종 중 1 개 |
| `status` | 예 | `open` (closure 미충족) / `closed` (충족) |
| `reflected_assets` | 예 | 재발 방지가 반영된 자산 링크 배열. open 시에는 빈 배열 가능하나 closure 시 1+ 필수 |

**`reflected_assets` 경로 컨벤션**: 다운스트림 프로젝트 root 기준 상대 경로. 가능하면 `파일.md#앵커` 또는 `파일.md:L번호` 까지 명시한다. 예: `docs/claude_guideline/coding.md#impl-pre-confirm`, `docs/claude_guideline/iteration_anti_pattern.md:L21-23`.

## 카테고리 정의

명시 규칙이 없거나 모호한 영역의 실수만 본 폴더에 들어오므로, 카테고리는 "지식 공백의 종류" 로 분류한다.

- **`manual-misread`** — 외부 매뉴얼·데이터시트·SDK 문서를 읽었으나 잘못 해석. 재발 방지는 통상 매뉴얼 발췌·인용 보강.
  예: STM32 HAL 함수의 timeout 인자 단위를 ms 로 가정하여 코드 작성 후 실제로는 tick 단위였음을 사용자가 정정.
- **`wrong-assumption`** — 코드·환경·도구의 동작을 검증 없이 가정. 재발 방지는 통상 사전 검증 단계 추가.
  예: 사용자가 "정확히 기록" 을 요청했을 때 메타 데이터를 최대치로 원할 거라 가정하고 9 필드 frontmatter 제안.
- **`context-missing`** — 필요한 컨텍스트 (기존 자료·세션 히스토리·관련 파일) 를 조사하지 않고 작성. 재발 방지는 통상 사전 조사 체크리스트.
  예: 자매 SSOT 가 다운스트림에 함께 설치되지 않을 가능성을 조사하지 않고 두 README 에 하드 마크다운 링크 작성.
- **`intent-guess`** — 모호한 사용자 표현을 질문 없이 추측. 재발 방지는 통상 모호어 사전 질문 규칙 강화. (단, 가이드라인에 "모호어 사전 질문" 이 명시 규칙으로 등재되어 있으면 본 카테고리가 아니라 규칙 위반.)
  예: "간단히" 라는 표현을 "1 줄" 으로 해석할지 "치트시트 형식" 으로 해석할지 묻지 않고 첫 번째로 가정.

새 카테고리 추가가 필요하면 본 README 의 enum 리스트를 먼저 갱신한다 (다운스트림 임의 추가 금지).

## 사용 규칙

- 사용자가 직접 지적한 실수는 그 즉시 본 폴더의 다운스트림 (`docs/claude-mistake/`) 에 기록한다.
- 사용자가 지적하지 않았더라도 Claude 가 스스로 인지한 실수도 기록할 수 있다.
- 기록 후, 가이드라인 / 메모리 / 체크리스트에 재발 방지 규칙을 반영한다 (단순 기록만으로는 학습이 닫히지 않음).
- 민감한 컨텍스트 (개인 정보, 운영 비밀) 가 포함되는 실수는 기록 위치를 `docs/claude_guideline/local/` (gitignore) 로 옮긴다.

## Closure 규칙 (학습 루프 닫기)

각 entry 는 다음 조건을 모두 만족할 때만 `status: closed` 로 표기한다. 미충족 entry 는 다운스트림 `docs/claude-mistake/INDEX.md` §미해결 항목 표에 등재 (INDEX.md 운용은 다운스트림 선택 사항 — 사건 누적 시 권장).

- **`reflected_assets` 1+ 명시** — 실제로 갱신된 파일 (가이드라인·audit 룰·hook·메모리 등) 의 링크가 1개 이상이어야 한다.
- **TBD 금지** — `reflected_assets` 항목이 "TBD", "추후", "후보" 로 끝나면 open 상태. 동일 세션 또는 7일 이내 closure 의무.
- **카테고리 부착** — frontmatter `category` 가 §카테고리 정의 enum 중 1 개여야 한다. 다운스트림 `docs/claude-mistake/INDEX.md` §카테고리 × 사건 매트릭스 에 한 행 추가 (INDEX 운용 시).
- **open 시 owner 명시** — `status: open` entry 는 §항목 형식 의 재발 방지 절 말미에 `**owner**:` 한 줄로 closure 책임자를 명시.

## 기존 실수 검토 시점

- **세션 시작 (자동)** — SessionStart hook 이 다운스트림 `docs/claude-mistake/INDEX.md` §메타 패턴 + §미해결 항목 두 절을 자동 주입한다 (hook 미설치 다운스트림은 수동 `head -50 docs/claude-mistake/INDEX.md`). 본 SSOT 에 INDEX 가 없는 것이 정상.
- **작업 시작 전 (수동)** — 동일 영역 / 모듈에서 기존 실수가 있었는지 다운스트림 `docs/claude-mistake/` 폴더를 빠르게 훑는다.
- **사용자 정정 직후** — 같은 세션의 다음 entry / 작업 전 정정한 카테고리의 `### 재발 방지` 절을 재독한다 (카테고리 학습 미적용 차단).

## 설치 방법

본 컨벤션은 단일 README 만으로 운용된다. 프로젝트 루트에서 다음을 실행하면 `docs/claude-mistake/` 가 생성되고 본 README 가 배치된다.

```bash
mkdir -p docs/claude-mistake
curl -fsSL https://raw.githubusercontent.com/kuks2309/kuks_claude_setup/master/claude-mistake/README.md \
  -o docs/claude-mistake/README.md
```

설치 후, 프로젝트 루트의 `CLAUDE.md` "도메인 문서 SSOT" 표에 다음 한 줄을 추가한다.

```markdown
| Claude 실수 기록 (재발 방지) | `docs/claude-mistake/README.md` (다운스트림 프로젝트 root 기준) |
```

## SSOT 경계 재확인

**SSOT 에는 본 README 만**. 사건 entry (`YYYY-MM-DD.md`) 와 카테고리 인덱스 (`INDEX.md`) 는 다운스트림 `docs/claude-mistake/` 에서만 운용. 본 SSOT 폴더에 사건이나 INDEX 가 들어가는 것은 책임 경계 위반.

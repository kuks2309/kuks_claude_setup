# Claude 규칙 위반 기록

Claude (LLM 어시스턴트) 가 본 프로젝트 작업 중 **명시 규칙을 어긴 사건** 과 그 경위, 강제 메커니즘 보강책을 누적 기록한다. 규칙이 있음에도 미준수가 반복되는 패턴을 가시화하고, 가이드라인·hook·audit 의 강제력을 점검한다.

## 본 SSOT 범위

본 폴더는 **규칙 위반** 을 기록한다. 규칙 위반은 가이드라인·SOP·체크리스트에 명시된 규칙을 알고 있었거나 알 수 있었음에도 어긴 사건을 가리킨다.

**포함 사례**

- "사용자가 지시한 것만 수행" 류 핵심 원칙 위반 (임의 추가·임의 삭제·요청 외 변경)
- 다중 파일 작업 시 파일별 명시 승인 절차 미준수
- iteration anti-pattern 류 규칙 위반 (2회 반복 부분 수정, 모호어 추측, 임의 추가분 일괄 감사 누락, 단일 파일 구조 사전 승인 누락)
- 정공법 우선 (tech-debt 회피) 류 규칙을 우회·shim·workaround 로 무력화
- 검증 없이 완료·성공 선언 (verification-before-completion 류 위반)
- 사용자 요청 범위를 임의 확장 (scope creep)

**핵심 질문**: "왜 알면서 어겼나" 또는 "왜 규칙이 보이지 않았나" — 규칙 가시성·강제력의 점검.

**해결 방향**: 강제 메커니즘 보강 (hook 추가·audit 룰 강화·체크리스트 가시성 향상·SessionStart 주입). 단순 "다음부터 잘하기" 다짐은 closure 가 되지 않는다.

**범위 외**: 가이드라인에 명시 규칙이 없거나 모호한 영역에서의 잘못된 판단·추측은 본 폴더의 기록 대상이 아니다 — 해결 방향이 "지식·컨텍스트 보강" 으로 본질이 달라지므로 별도 기록 체계가 필요하다.

**Boundary 판정**: 한 사건이 본 폴더 범위 (규칙 위반) 와 지식 공백에 모두 해당하면 **본 폴더 기록을 우선** 한다 — 명시 규칙이 1+ 어겨졌다면 "지식 공백" 으로 분류하지 않는다. 강제 메커니즘 보강이 우선 닫혀야 같은 사건이 재발하지 않기 때문.

## 책임 경계 (필독)

본 폴더 (`kuks_claude_setup_new/claude-rule-violation/`) 는 **일반화 SSOT** — 형식·규칙·운용 가이드만 둔다.

- **여기에 두는 것**: `README.md` (본 파일), 형식 변경 이력
- **여기에 두지 말 것**: 실제 사건 entry (`YYYY-MM-DD.md`), 카테고리 인덱스 (`INDEX.md`), 프로젝트별 closure 데이터
- **사건 entry 작성 위치**: 각 다운스트림 프로젝트의 `docs/claude-rule-violation/YYYY-MM-DD.md`. 본 SSOT 폴더에 사건을 작성하면 다른 프로젝트에 무관한 사건이 노출되는 책임 경계 침범.

## 파일 구조

- **한 사건 = 한 파일** — 한 파일 안에 다중 entry 금지. 표준 markdown frontmatter 파서는 파일 최상단 1 블록만 인식하므로, 다중 entry 시 2 번째부터의 YAML frontmatter 가 본문 텍스트로 처리되어 INDEX 자동 생성·grep 분석에 누락된다.
- **파일명**: `YYYY-MM-DD-NNN.md` 또는 `YYYY-MM-DD-NNN_<짧은제목>.md` (NNN 은 같은 날 순번 `001`+)
- **시간순 누적**: 폴더 내 파일명 정렬로 자연 보장 (최신 = 가장 큰 NNN). 별도 prepend 작업 불필요.

## 항목 형식

각 파일은 YAML frontmatter (4 필드) + 본문 5 절로 구성된다. 실수 기록과 달리 4 번째 절은 **"위반 경위 / 가시성 분석"** — 규칙이 알려져 있었는지, 어디서 가시성이 끊겼는지 점검한다.

본 SSOT 의 §어긴 규칙 절과 §위반 경위 / 가시성 분석 절은 역할이 분리된다 — §어긴 규칙 = **규칙의 명시 인용만** (파일·절·줄). §위반 경위 = **가시성·강제력 점검만** (왜 못 봤나 / 왜 강제력이 없었나). 두 절에 동일 내용을 중복 기재하지 않는다.

````markdown
---
id: YYYY-MM-DD-NNN
category: user-intent-only | per-file-approval | iteration-loop | tech-debt-shortcut | verify-skip | scope-creep
status: open | closed
reflected_assets:
  - <강화된 규칙/hook/audit/체크리스트 링크>
---

# YYYY-MM-DD HH:MM (KST) — <짧은 제목>

## 무엇을 했는가
Claude 가 시도한 행동 / 작성한 내용을 객관적으로 기술.

## 어긴 규칙
어떤 가이드라인의 어떤 절·줄을 어겼는지. 가이드라인 파일명 + §절명 + (가능하면) `:L번호` 까지 명시. **규칙의 명시 인용만** — 가시성 분석 / 못 본 이유는 다음 §위반 경위 절로.

## 사용자 지적
사용자가 어떻게 교정했는지 (인용 또는 요약).

## 위반 경위 / 가시성 분석
규칙을 알고 있었는가 / 세션 시작 시 주입되었는가 / 가이드라인이 모호했는가 / hook 이 부재였는가. **"왜 알면서 어겼나" 또는 "왜 규칙이 보이지 않았나" 만**. §어긴 규칙의 인용을 반복하지 않는다.

## 재발 방지 (강제력 보강)
같은 위반을 막기 위해 어떤 강제 메커니즘을 추가·강화하는지. `reflected_assets` 에 등재한 자산의 갱신 위치 (앵커 포함) 를 명시.

> `status: open` 일 때는 본 절 마지막에 `**owner**: claude | user | auto-rule` 한 줄을 부착해 closure 책임자를 명시한다. `closed` entry 에는 부착하지 않는다.
````

## Frontmatter 필드 정의

| 필드 | 필수 | 값 |
|------|------|---|
| `id` | 예 | `YYYY-MM-DD-NNN` (같은 날 사건은 NNN 증가) |
| `category` | 예 | 아래 §카테고리 정의 enum 6 종 중 1 개 |
| `status` | 예 | `open` (closure 미충족) / `closed` (충족) |
| `reflected_assets` | 예 | 강제 메커니즘 보강이 반영된 자산 링크 배열. open 시에는 빈 배열 가능하나 closure 시 1+ 필수 |

**`reflected_assets` 경로 컨벤션**: 다운스트림 프로젝트 root 기준 상대 경로. 가능하면 `파일.md#앵커` 또는 `파일.md:L번호` 까지 명시한다. 본 SSOT 폴더의 자산은 강화된 가이드라인 절, 신규 hook 스크립트, audit 룰, 체크리스트 등이 주로 등재된다. 예: `docs/claude_guideline/iteration_anti_pattern.md#L21-23`, `.claude/hooks/per_file_approval.sh`.

## 카테고리 정의

규칙 위반의 "어느 규칙이 무시되었나" 로 분류한다.

- **`user-intent-only`** — "사용자가 지시한 것만 수행" (루트 `CLAUDE.md` 핵심 원칙 #1) 위반. 임의 추가·임의 삭제·요청 외 변경.
  예: 사용자가 함수 하나 수정 요청했는데 같은 파일의 다른 함수도 "스타일 통일" 명목으로 임의 정리.
- **`per-file-approval`** — 다중 파일 작업 시 파일별 명시 승인 없이 다음 파일로 진행. 짧은 응답 ("진행?", "??") 을 다음 파일 작성 권한으로 오인.
  예: 사용자가 "좋습니다" 한 마디 후 자동으로 다음 파일 2~3 개를 연속 작성.
- **`iteration-loop`** — iteration anti-pattern 류 규칙 위반. 2회 반복 부분 수정 / 모호어 추측 / 임의 추가분 일괄 감사 누락 / 단일 파일 구조 사전 승인 누락.
  예: 사용자 메시지의 "정확히 기록" 같은 모호어를 묻지 않고 임의 해석 후 구조 제안.
- **`tech-debt-shortcut`** — "정공법 우선" 류 규칙 위반. 우회·shim·hack·workaround 로 본질 회피.
  예: 모듈 import 오류를 근본 원인 (순환 참조) 해결 대신 try/except 로 silent fallback.
- **`verify-skip`** — 검증 없이 완료·성공 선언. 빌드·테스트·관찰 가능 지표 확인 누락. verification-before-completion 류 규칙 위반.
  예: 코드 수정 후 빌드·테스트 실행 없이 "수정 완료" 보고.
- **`scope-creep`** — 사용자 요청 범위를 임의 확장 (요청한 fix 외 리팩토링·정리·관련 없는 변경 동반).
  예: 버그 fix 요청에 무관한 import 정리, 변수명 변경, 주석 추가 동반.

새 카테고리 추가가 필요하면 본 README 의 enum 리스트를 먼저 갱신한다 (다운스트림 임의 추가 금지).

## 사용 규칙

- 사용자가 직접 지적한 규칙 위반은 그 즉시 본 폴더의 다운스트림 (`docs/claude-rule-violation/`) 에 기록한다.
- 사용자가 지적하지 않았더라도 Claude 가 스스로 인지한 위반도 기록할 수 있다.
- 기록 후, 가이드라인 / hook / audit / 체크리스트에 강제력 보강을 반영한다 (단순 기록만으로는 학습이 닫히지 않음).
- 민감한 컨텍스트 (개인 정보, 운영 비밀) 가 포함되는 위반은 기록 위치를 `docs/claude_guideline/local/` (gitignore) 로 옮긴다.

## Closure 규칙 (학습 루프 닫기)

각 entry 는 다음 조건을 모두 만족할 때만 `status: closed` 로 표기한다. 미충족 entry 는 다운스트림 `docs/claude-rule-violation/INDEX.md` §미해결 항목 표에 등재 (INDEX.md 운용은 다운스트림 선택 사항 — 사건 누적 시 권장).

- **`reflected_assets` 1+ 명시** — 실제로 갱신된 자산 (강화된 가이드라인 절·신규 hook·audit 룰·체크리스트 등) 의 링크가 1개 이상이어야 한다. **단순 "기록만" 으로는 closure 불가** — 강제 메커니즘 보강이 본 폴더 closure 의 핵심.
- **TBD 금지** — `reflected_assets` 항목이 "TBD", "추후", "후보" 로 끝나면 open 상태. 동일 세션 또는 7일 이내 closure 의무.
- **카테고리 부착** — frontmatter `category` 가 §카테고리 정의 enum 중 1 개여야 한다. 다운스트림 `docs/claude-rule-violation/INDEX.md` §카테고리 × 사건 매트릭스 에 한 행 추가 (INDEX 운용 시).
- **open 시 owner 명시** — `status: open` entry 는 §항목 형식 의 재발 방지 절 말미에 `**owner**:` 한 줄로 closure 책임자를 명시.

## 기존 위반 검토 시점

- **세션 시작 (자동)** — SessionStart hook 이 다운스트림 `docs/claude-rule-violation/INDEX.md` §메타 패턴 + §미해결 항목 두 절을 자동 주입한다 (hook 미설치 다운스트림은 수동 `head -50 docs/claude-rule-violation/INDEX.md`). 본 SSOT 에 INDEX 가 없는 것이 정상.
- **작업 시작 전 (수동)** — 동일 영역 / 카테고리에서 기존 위반이 있었는지 다운스트림 `docs/claude-rule-violation/` 폴더를 빠르게 훑는다.
- **사용자 정정 직후** — 같은 세션의 다음 작업 전 정정한 카테고리의 `### 재발 방지` 절을 재독한다 (강제 메커니즘 미적용 차단).

## 설치 방법

본 컨벤션은 단일 README 만으로 운용된다. 프로젝트 루트에서 다음을 실행하면 `docs/claude-rule-violation/` 가 생성되고 본 README 가 배치된다.

```bash
mkdir -p docs/claude-rule-violation
curl -fsSL https://raw.githubusercontent.com/kuks2309/kuks_claude_setup/master/claude-rule-violation/README.md \
  -o docs/claude-rule-violation/README.md
```

설치 후, 프로젝트 루트의 `CLAUDE.md` "도메인 문서 SSOT" 표에 다음 한 줄을 추가한다.

```markdown
| Claude 규칙 위반 기록 (강제력 보강) | `docs/claude-rule-violation/README.md` (다운스트림 프로젝트 root 기준) |
```

## SSOT 경계 재확인

**SSOT 에는 본 README 만**. 사건 entry (`YYYY-MM-DD.md`) 와 카테고리 인덱스 (`INDEX.md`) 는 다운스트림 `docs/claude-rule-violation/` 에서만 운용. 본 SSOT 폴더에 사건이나 INDEX 가 들어가는 것은 책임 경계 위반.

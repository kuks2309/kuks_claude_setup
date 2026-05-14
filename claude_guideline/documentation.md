# 문서 작성 규칙

워크스페이스의 모든 마크다운 자산이 따르는 작성 메타 룰 SSOT. 어휘 / 어투 / 디렉터리 네이밍 / 파일명 / SSOT 경로 / 표준 폴더를 한 곳에서 정의.

## SSOT 경로 (Authoring vs Mirror)

본 가이드라인 자산의 **authoring SSOT** 는 `kuks_claude_setup/claude_guideline/` 1 곳뿐.

| 구분 | 위치 | 역할 |
|------|------|------|
| **Authoring SSOT** | `kuks_claude_setup/claude_guideline/` | 룰을 수정·신설하는 위치 |
| **Generated mirror** | `docs/claude_guideline/` | 다운스트림 설치본 (`install.sh` / `update.sh` 산출). **직접 수정 금지** |

- 룰 변경이 필요하면 authoring SSOT 수정 → `update.sh` 재실행으로 mirror 갱신.
- mirror 직접 수정 시 다음 `update.sh` 에서 덮어쓰임. `audit.sh` `[tree-diff]` / `[mirror-only-file]` 가드가 drift 검출.
- 본 레포 내부 cross-reference 는 bare 상대경로 (`[claude_md.md](claude_md.md)`) 사용. 다운스트림 사용자 실행 명령은 `docs/claude_guideline/...` 절대 표기.

## 용어 표준 (Terminology SSOT)

| 개념 | KO prose | EN / 제품명 | 코드 / CLI 토큰 | 파일명 |
|---|---|---|---|---|
| skill | **스킬** | Skill (Title) | `skill` | `SKILL.md` (번들) / `skills/<kebab>.md` (인라인) |
| agent | **에이전트** / 서브에이전트 | Agent (Title) | `agent`, `sub-agent` | — |
| workflow | **워크플로** | workflow | `workflow` | — |
| user instruction | **사용자 지시사항** (명사) / "사용자가 지시한 사항" (서술구) | (영문 사용 금지 — 한국어 SSOT) | — | — |
| guideline | **지침** (umbrella) / **규칙** (도메인) / **원칙** (불변량) | guideline | — | — |

- `워크플로우` (잘못된 표기) → `워크플로`
- `사용자 요청` / `요청사항` / `request` → `사용자 지시사항`
- prose 의 `SKILL` (all-caps) 금지 — 파일명 / CLI 토큰 한정

## 어투 규칙

- `claude_guideline/**` (메타 규칙) = **평어 (`-한다`)**
- `skills/**`, `agents/**`, 패키지 README, 루트 `README.md` = **존댓말 (`-합니다`)**
- 한 파일 내 평어 / 존댓말 혼용 금지 (`audit.sh` 가 검출).

## 디렉터리 / 파일 명명

- 디렉터리 표준: **kebab-case** (예: `claude-mistake`, `pptx-design-styles`).
- Legacy snake-case (`claude_guideline/`, `conversation_backup/`) 는 외부 cross-reference 비용으로 유예. 신규 디렉터리는 kebab 강제.
- 한글 디렉터리명 (`hwp스킬/`) 은 후속 PR 에서 ASCII rename.
- 파일명과 H1 헤딩은 같은 어휘를 사용 (`documentation.md` ↔ `# 문서 작성 규칙`).
- 다국어 README 는 H1 도 언어별로 분기 (`README.md` = 영문 H1, `README_ko.md` = 한국어 H1).

## docs/ 표준 폴더

다운스트림 프로젝트 `docs/` 의 표준 폴더 정의:

| 폴더 | 정의 | 책임 |
|------|------|------|
| `docs/user_instructions/` | 사용자 원문 시간 누적 | [user_instruction_recording.md](user_instruction_recording.md) |
| `docs/worklog/` | 일반 작업 결과 / 산출물 (시간 누적, 최신 위) | 일반 작업 로그 |
| `docs/code_review/` | 코드 리뷰 / 평가 | 주제별 |
| `docs/analysis/` | 분석 / 리서치 | 주제별 |
| `docs/refactoring/` | 리팩토링 계획·결과 | 주제별 |
| `docs/troubleshooting/` | 트러블슈팅 | 주제별 |
| `docs/issues_and_fixes/` | 이슈·정정 이력 | 시간 누적 |
| `docs/claude-mistake/` | Claude 의 반복 실수 카탈로그 | INDEX.md + 케이스별 |
| `docs/manual/` | 외부 매뉴얼 / 데이터시트 (선택) | [manual.md](manual.md) |
| `docs/claude_guideline/` | mirror — 직접 수정 금지 | `update.sh` 산출 |

## 폴더 신규 생성

새 표준 폴더 추가 시 사용자 명시 승인 필수 ([coding.md](coding.md) §사전 승인 트리거). 추가 후 본 표 갱신.

## 변경 절차

본 룰은 SSOT. 변경 시 사용자 승인 필수.

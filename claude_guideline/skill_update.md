# 자산 등록 / 스킬 업데이트

신규 / 갱신 자산 (스킬·에이전트·hook·가이드라인·템플릿) 을 본 SSOT 레포 (`kuks_claude_setup/`) 에 등록하는 절차와 자동화 정책 정의.

## 자산 분류와 SSOT 위치

| 카테고리 | 워크스페이스 (개발 / 검증) | SSOT 레포 (등록 후) |
|---|---|---|
| Slash command / 인라인 스킬 | `.claude/commands/`, `.claude/skills/` | `skills/<name>.md` |
| Claude Skills 번들 (multi-file) | `.claude/skills/<name>/` | `<name>/SKILL.md + scripts/ + references/` |
| Hook 스크립트 | `.claude/hooks/<name>.sh` | `tools/hooks/<name>.sh` (또는 `skills/<name>/`) |
| 가이드라인 | `kuks_claude_setup/claude_guideline/<file>.md` (authoring SSOT) | 동일 — mirror `docs/claude_guideline/` 는 `update.sh` 산출 |
| 커스텀 sub-agent | `.claude/agents/<name>.md` | `agents/<name>.md` |
| 도메인 README (이슈·실수·지시) | `docs/<domain>/README.md` | `<domain>/README.md` |

위 카테고리에 명확히 속하지 않는 신규 자산은 SSOT 레포 README 에서 적합 폴더 결정 또는 사용자 승인 후 새 폴더 추가 ([coding.md](coding.md) §사전 승인 트리거).

## 자동화 정책 (자동 활성 vs 명시 호출)

모든 자산은 다음 4 표현 중 하나만 가질 수 있다. CLAUDE.md 핵심 원칙 #1 ("사용자가 지시한 사항만 수행") / #2 ("임의로 기능을 추가하거나 변경하지 않는다") 합치 의무.

| 표현 | 의미 | 핵심 원칙 |
|------|------|----------|
| **명시 호출** | 사용자가 `/<skill>` 또는 명시 자연어로 호출. 호출 전 미작동 | 합치 |
| **권고 트리거 (advisory)** | 키워드 매칭 시 "이 스킬 참조할까요?" 1줄 제안. 승인 후 작동 | 합치 |
| **자동 인용 (passive cite)** | 키워드 시 본 SSOT 룰 *문서만* 인용 (작업 트리거 X) | 합치 |
| **자동 활성 (auto-activate)** ← **금지** | 키워드·이벤트 즉시 *작업 수행* (다운로드 / 파일 생성 / `git add` / memory 기록 포함) | **위반** |

### 금지 표현

다음 표현은 핵심 원칙 #1·#2 위반이므로 사용 금지:

- "키워드 감지 시 자동 활성", "키워드 (...) 등장 시 자동 활성화"
- "MANDATORY", "반드시 ... 업데이트", "사용자 개입 없이 완전 자동"
- "다음 순서" (단정형), "절대 사용 금지" (일률 적용 헤더)

→ "사용자가 `기록` 또는 `기록해` 라고 지시하면" / "본 SSOT 가 권장하는 순서 (사용자 합의 후 적용)" / "자동 인용" 으로 약화 표기.

### 자동 트리거 허용 화이트리스트 (3 종)

좁은 예외:

1. **자동 인용 (passive cite)** — 작업 트리거 없이 문서만 참조.
2. **PostToolUse 로컬 jsonl 관찰** — 머신 로컬 한정 도구 사용 로그 누적 (단, 다음 세션 Claude 행동 변경하는 영속 memory 갱신은 별도 사용자 opt-in).
3. **idempotent 디렉토리 생성** — `mkdir -p` 같이 기존 데이터를 덮어쓰지 않고 사용자가 곧 직접 파일을 쓸 디렉토리 한정. 신규 `.md` 자동 생성은 본 예외 밖.

`audit.sh [auto-trigger-vocab]` 룰이 본 금지 표현을 검출.

### 등록 안 해도 되는 경우 — 머신 로컬 학습 캐시

다음은 SSOT 레포 추적 대상 외, 본 등록 절차 미적용:

- `project-autolearn` 의 `.omc/patterns.md`, `.omc/observations/`
- `~/.claude/projects/*/memory/learned_patterns.md` (auto memory)
- 기타 머신 로컬 학습 캐시 (`.gitignore` 강제)

## 등록 절차

```text
[워크스페이스에서 검증]
       ↓
[SSOT 레포 clone / pull]
       ↓
[자산 복사 (placeholder 추상화)]
       ↓
[메타 갱신 — README / CHANGELOG / VERSION]
       ↓
[commit + push (사용자 명시 승인)]
       ↓
[워크스페이스 측 sync (필요 시)]
```

1. **워크스페이스에서 검증.** 자산이 의도대로 동작함을 실제 확인 후 등록 — 검증 안 된 자산은 SSOT 미등록. 가이드라인 자산은 authoring SSOT (`kuks_claude_setup/claude_guideline/`) 에서 직접 검증 ([documentation.md](documentation.md) §SSOT 경로).
2. **SSOT 레포 clone / pull.** 로컬 사본 최신화.
3. **자산 복사.** 위 표의 "SSOT 레포 위치" 로 옮긴다. 워크스페이스 고유 경로 (IP, 사설 endpoint 등) 는 placeholder / 환경변수로 추상화 ([local/README.md](local/README.md) 참조).
4. **메타 갱신.**
   - `README.md` Tier 표 / 진입점 추가
   - `CHANGELOG.md` 항목 추가
   - 필요 시 `VERSION` 갱신 (semver)
   - `templates/CLAUDE.md.template` 동기화 (해당 시)
5. **commit + push.** "기록" 단축어 적용 — 단, 본 SSOT 원격 push 는 사용자 명시 확인 ([github.md](github.md) §Push 전 확인).
6. **워크스페이스 sync.** `update.sh` 재실행 또는 mirror 폴더 (`docs/claude_guideline/`) 갱신.

## 변경 절차

본 룰은 SSOT. 변경 시 사용자 승인 필수.

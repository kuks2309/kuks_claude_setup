# CLAUDE.md 작성 가이드

본 SSOT 는 CLAUDE.md 파일의 정의 / 구조 / 작성 절차 / 검증 / 변종 차단 룰을 정의한다.

## 1. 정의

CLAUDE.md 는 Claude Code 가 프로젝트 작업 시 **자동 로드** 하는 메타 지침 파일.

- **위치**: 프로젝트 루트 (필수) + 모듈 단위 (선택, override 계층)
- **명명**: 대문자 `CLAUDE.md` 만 허용 — 소문자 `claude.md` 는 Claude Code 가 자동 로드하지 않음
- **인코딩**: UTF-8 마크다운
- **분량**: 50~60 줄 (얇은 진입점) — SSOT 위임형 패턴 권장

## 2. 핵심 원칙 (모든 CLAUDE.md 가 포함해야 하는 8 대 원칙)

다운스트림 프로젝트의 CLAUDE.md 본문 또는 본 §2 SSOT 링크로 포함한다.

### 2.1 시간 흐름 순서

1. **모든 의도와 결정을 즉시 기록한다** — 의도 부채 방지 ([user_instruction_recording.md](user_instruction_recording.md))
2. **객관적 사실로 판단한다** — 코드·로그·매뉴얼 인용, 추측·기억·일반 지식 금지 ([manual.md](manual.md))
3. **모르는 것은 "확인되지 않음" 으로 명시한다** — 할루시네이션 금지
4. **사용자가 지시한 사항만 수행한다** — 범위 임의 확장 금지 ([coding.md](coding.md))
5. **관련 이론을 철저히 조사한 후 시작한다** — 공식 문서·매뉴얼·기존 코드 우선
6. **코딩 전 구조를 제시하고 사용자 승인을 받는다** ([iteration_anti_pattern.md](iteration_anti_pattern.md))
7. **임의로 기능을 추가하거나 변경하지 않는다** — 범위 이탈 사전 차단
8. **검증·보고는 파일·줄·실제 출력을 인용한다** — "동일합니다" 금지

### 2.2 추가 원칙 (선택)

- 같은 실수를 다른 형태로 반복하지 않는다 ([iteration_anti_pattern.md](iteration_anti_pattern.md))

## 3. 표준 구조 (Thin SSOT 위임형)

CLAUDE.md 본문은 SSOT 링크만, 룰 authoring SSOT 는 `kuks_claude_setup/claude_guideline/` 1 곳. 다운스트림 프로젝트는 `docs/claude_guideline/` mirror 를 참조하되 직접 수정하지 않는다 ([documentation.md](documentation.md) §SSOT 경로).

### 3.1 권장 템플릿 ([templates/CLAUDE.md.template](../templates/CLAUDE.md.template) 참조)

```markdown
# Claude 작업 지침

## 핵심 원칙

(§2 8 대 원칙 본문 또는 SSOT 링크)

## 프로젝트 성격

<프로젝트 1-2줄 설명 + SSOT 원격 링크>

## 참조 자료 규칙

(도메인별 참조 자료가 추가되면 본 절에 SSOT 링크 작성)

## 문서 작업 규칙 (먼저 읽기)

### Claude 작업 지침 (메타 규칙)

- 진입점 → docs/claude_guideline/README.md
  - 사용자 지시 기록 (Step 1) → user_instruction_recording.md
  - 작업 절차 체크리스트 → workflow.md
  - 코드 작업 규칙 → coding.md
  - GitHub 워크플로 + "기록" 단축어 → github.md
  - 기술 부채 방지 → tech_debt.md
  - 반복 수정 회피 → iteration_anti_pattern.md
  - 매뉴얼 인용 → manual.md
  - 문서 작성 메타 룰 → documentation.md
  - ROS2 / 임베디드 → ros2.md
  - 자산 등록 / 자동화 정책 → skill_update.md
  - CLAUDE.md 작성 가이드 → claude_md.md
  - 프로젝트별 override → local/

### 도메인 문서

- 진입점 → docs/README.md

## 모듈 CLAUDE.md (override 계층)

(현재 모듈 CLAUDE.md 없음. 추가 시 본 절에 등록하며 충돌 시 모듈 규칙이 루트보다 우선한다.)

## 도메인 문서 SSOT

(도메인 추가 시 docs/README.md 진입점 표에 등록)

규칙 변경이 필요하면 해당 README 수정 여부를 먼저 사용자에게 문의한다.
```

## 4. 작성 절차

### 4.1 신규 프로젝트 시작 시

1. 템플릿 복사: `cp kuks_claude_setup/claude_guideline/templates/CLAUDE.md.template <project>/CLAUDE.md`
2. 프로젝트 성격 1-2줄 작성 (목적, 도메인, 외부 SSOT 링크)
3. 적용할 SSOT 도메인 문서 식별 (ROS2 / 임베디드 / AI / Web 등)
4. 도메인 문서 SSOT 표 채움
5. `install.sh` 로 `docs/claude_guideline/` 동기화
6. 사용자 검토 → 승인 → 첫 commit

### 4.2 모듈 CLAUDE.md 추가 시

1. 루트 CLAUDE.md 의 "모듈 CLAUDE.md" 절에 등록
2. 모듈별 **특수 규칙만** 작성 (루트 8 대 원칙 자동 상속, 중복 작성 금지)
3. override 시 명시: "본 모듈은 X 룰을 다음과 같이 변경 적용함"

### 4.3 룰 변경 시

1. 사용자 승인 필수 (8 대 원칙 #4 적용)
2. SSOT 파일 변경 → 영향받는 CLAUDE.md 동기화
3. CHANGELOG / VERSION 갱신
4. push 전 사용자 명시 확인 ([github.md](github.md) §Push 전 확인)

## 5. 검증 체크리스트

신규 / 수정 후 확인:

- [ ] 8 대 원칙 전부 포함 (또는 §2 SSOT 링크)
- [ ] 프로젝트 성격 1-2줄 명시
- [ ] 도메인 문서 SSOT 표 채움
- [ ] 모듈 CLAUDE.md 가 있다면 모두 등록
- [ ] 외부 SSOT 링크 작동 (404 없음, 상대경로 정확)
- [ ] 명명 규약: 대문자 `CLAUDE.md` (소문자 `claude.md` 금지)
- [ ] 50~60 줄 (얇은 진입점) — 두꺼우면 SSOT 로 분리
- [ ] 변경 사항 사용자 승인 받음
- [ ] `audit.sh` dry-run 통과 (린트·구조·SSOT 정합성)

## 6. Variant 차단 (anti-pattern 방지)

다음 변형 금지 — `audit.sh` 가 자동 감지:

| Variant | 위반 사유 | 자동 정정 |
|---|---|---|
| 소문자 `claude.md` | Claude Code 자동 로드 안 됨 | rename → `CLAUDE.md` |
| 같은 워크스페이스의 분기 사본 (`current/CLAUDE.md` vs `_old/CLAUDE.md`) | 정보 손실, 동기화 부담 | `_old` 정리, single source 통일 |
| 본문에 SSOT 룰 직접 복제 (예: 350 줄 + 두꺼운 CLAUDE.md) | SSOT 위반, 변경 시 다중 동기화 | docs/claude_guideline/ 링크로 분리 |
| 8 대 원칙 누락 | 거버넌스 표준 미충족 | 누락 원칙 추가 |
| 모듈 CLAUDE.md 미등록 | 루트가 모듈 존재 모름 | 루트 "모듈 CLAUDE.md" 절에 추가 |

## 7. 모듈 override 패턴

| 패턴 | 사례 | 권장 |
|---|---|---|
| **상속** (모듈이 상위 룰 그대로 따름) | 단일 도메인 모듈 | OK |
| **부분 override** (특정 룰만 모듈에서 변경) | 오프라인 동작 / 특수 빌드 환경 | 명시 권장 |
| **자체 완결** (모듈이 독립 도메인) | WSL2 전용 / 외부 toolchain | 별도 SSOT 권장 |

## 8. 변경 절차

본 룰은 SSOT. 변경 시 사용자 승인 필수. 변경 후:

1. 다운스트림 CLAUDE.md 의 "참조 자료 규칙" 절에 본 SSOT (`claude_md.md`) 가 등록되어 있는지 확인
2. README.md 진입점 표 갱신
3. CHANGELOG.md / VERSION (semver) 갱신
4. `install.sh` / `update.sh` 의 FILES 배열에 본 파일 포함 확인
5. 본 SSOT 가 적용된 다른 프로젝트 CLAUDE.md 동기화 안내 (CHANGELOG 통해)

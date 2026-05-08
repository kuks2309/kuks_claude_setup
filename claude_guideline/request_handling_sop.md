# 사용자 지시사항 처리 표준 절차 (SOP)

매번 사용자 지시가 도착하면 다음 9 단계를 **순차 실행** 하고 각 단계마다 **✓ 체크** 후 다음 단계로 진행한다. 단계 skip 또는 ✓ 체크 누락은 거짓 단정 / 중복 작업 / 미승인 변경 등의 위험을 초래한다 (실제 사례 §11 참조).

본 SOP 는 SSOT 룰. 변경 시 사용자 승인 필수.

---

## 1. 흐름도 (한눈에)

```
[사용자 지시 도착]
   ↓
[Step 1] 지시 명확화                ────→  ✓ 체크: 작업 범위/의도 명확
   ↓
[Step 2] requirements.md 기록        ────→  ✓ 체크: 시간 역순 추가, grep 확인
   ↓
[Step 3] 기존 자료 검색 (5종)        ────→  ✓ 체크: 중복/과거 실수 인지
   ↓
[Step 4] 적용 SSOT 룰 식별           ────→  ✓ 체크: 룰 명시, 충돌 없음
   ↓
[Step 5] 사전 승인 판단              ────→  ✓ 체크: 트리거 시 STOP, ask user
   ↓
[Step 6] 실행 (TodoWrite 추적)       ────→  ✓ 체크: 단계별 완료
   ↓
[Step 7] 검증 (manual.md §9)         ────→  ✓ 체크: 거짓 단정 / 미인용 / 정정 잔존 0
   ↓
[Step 8] requirements.md 결론 갱신    ────→  ✓ 체크: 동일 항목 안에 추가
   ↓
[Step 9] 1-2줄 결과 보고             ────→  ✓ 체크: 보고 완료
   ↓
[완료]
```

---

## 2. Step 1 — 지시 명확화

- 모호하면 user 에 즉시 1줄 질문 (긴 추측 금지)
- 작업 유형 분류:
  - 분석 (read-only 조사)
  - 수정 (코드 / 문서 변경)
  - 신규 작성 (파일 생성)
  - 검증 (기존 결과 cross-check)
  - 외부 연동 (push / 다운로드 / 외부 도구)
- 작업 범위 1줄 요약 자체 작성 → user 와 일치 여부 즉시 확인 가능

**✓ 체크**: 작업 범위 / 의도 명확. 모호하면 STOP 후 질문.

---

## 3. Step 2 — requirements.md 기록

본 프로젝트 루트의 `docs/request/requirements.md` (또는 동등 경로 — 프로젝트별 [`local/`](local/) override 가능).

기록 형식:
```markdown
## YYYY-MM-DD HH:MM KST — <짧은 제목>

### 요청
> "<사용자 원문 인용>"

### 처리
- (현재 단계에서 알고 있는 처리 계획 초안)

### 결론 / 산출물
- (Step 8 에서 갱신)

---
```

**룰**:
- KST 시각, 시간 역순 (최신 위)
- 항목 추가 즉시 (작업 완료 후 일괄 X)
- 동일 요구사항 단순 재확인은 생략 가능
- 비밀번호 / NDA 정보는 마스킹

**✓ 체크**: 항목 추가 완료. `grep "^## " docs/request/requirements.md | head -3` 로 시간 역순 확인.

---

## 4. Step 3 — 기존 자료 검색 (5종)

다음 5개 위치를 **모두 확인** (skip 시 중복 작업 / 과거 실수 재현 위험):

| # | 위치 | 확인 내용 |
|---|------|----------|
| 1 | `docs/<관련 분석명>/` | 기존 분석 결과 / MASTER 문서 |
| 2 | `.omc/research/<관련>/` | 워커 보고 / 임시 분석 |
| 3 | `manual/` | datasheet PDF / 외부 1차 source |
| 4 | `docs/claude_guideline/` | 적용할 SSOT 룰 (manual.md, github.md 등) |
| 5 | `~/.claude/projects/<프로젝트>/memory/` | feedback / 과거 실수 기록 |

**✓ 체크**: 5종 모두 검색 완료. 중복 작업 / 기존 정정 / 과거 실수 인지.

---

## 5. Step 4 — 적용 SSOT 룰 식별

본 프로젝트의 `docs/claude_guideline/` 에서 적용 룰 식별:

| 룰 파일 | 적용 트리거 |
|---------|-----------|
| [manual.md](manual.md) | 외부 spec / datasheet / INL/DNL/AEC-Q100 등 키워드 — auto skill `manual-first` |
| [github.md](github.md) | commit / push / 기록 명령 |
| [workflow.md](workflow.md) | 펌웨어 플래시 등 절차 |
| [documentation.md](documentation.md) | 문서 양식 / 작성 메타 룰 |
| [iteration_anti_pattern.md](iteration_anti_pattern.md) | 정정 라운드 의심 (2회 이상 부분 수정) |
| [skill_update.md](skill_update.md) | 신규 스킬 / 자산 등록 |

**✓ 체크**: 적용 룰 명시 (1개 이상). 룰 간 충돌 없음.

---

## 6. Step 5 — 사전 승인 판단

다음 트리거 해당 시 **STOP, ask user**:

| 트리거 | 사유 |
|--------|------|
| 코드 (`Source/` 또는 동등 코드 디렉토리) 수정 | 사용자 명시 승인 필수 |
| sub-agent 스폰 (3명 이상 또는 큰 비용) | 사용자 승인 |
| 외부 SSOT 원격 push (예: 벤더 SSOT 클론 → 원격) | "기록" 단축어 적용 대상이지만, 외부 SSOT 는 push 직전 사용자 명시 확인 (github.md "Push 전 확인" 절 + 일반 룰 "단 push 는 별도 확인") |
| `.gitignore` 우회 / 빌드 산출물 commit | github.md vendored 보호 |
| 비밀번호 / NDA / 자격증명 노출 가능 | 즉시 STOP |
| 새 폴더 / 모듈 / 패키지 생성 | coding.md 사전 승인 |

**✓ 체크**: 트리거 해당 → STOP. 미해당 → 다음 step.

---

## 7. Step 6 — 실행

- `TodoWrite` 로 sub-step 추적 (3 step 이상 작업 시 강제)
- 각 sub-step 완료마다 todo 갱신 (in_progress → completed)
- 병렬 가능한 작업은 single message multi tool call

**✓ 체크**: 모든 todo completed, 미완 항목 없음.

---

## 8. Step 7 — 검증 ([manual.md §9](manual.md) 사후 체크리스트)

- ✓ 표시 항목 = file:line 또는 datasheet:page 인용 있는가?
- 벤더 SDK / 드라이버 매크로 → silicon datasheet spec 비약 있는가? (있으면 ⚠ 격하)
- 강한 단정어 ("위반"/"초과"/"non-compliance"/"fail") = primary source 첨부?
- 미검증 추론을 ✓ 로 표시한 곳 없는가?
- 정정 잔존 (오류 흔적 본문 embedded) 없는가?
- 정정 이력 (vN → vN+1) 명시?

**✓ 체크**: 검증 통과. 미해결 ⚠ 항목은 사용자에게 명시.

---

## 9. Step 8 — requirements.md 결론 / 산출물 갱신

- Step 2 와 **같은 항목 안** "결론 / 산출물" 절 추가/갱신
- 시간 역순 유지 (순서 변경 X)
- 산출물 목록: 신규 파일 / 갱신 파일 / commit hash / push 결과 등

**✓ 체크**: 갱신 완료. 다른 항목 순서 변경 없음.

---

## 10. Step 9 — 1-2줄 결과 보고

- 일상 작업: 1-2줄 (workflow.md §보고 형식)
- 다음 시점 추가 명시:
  - 사전 승인 트리거 변경 착수 전
  - 우회 / workaround 사용 결정 전
  - "기록" 명령 처리 시 (commit 범위 보고)
  - 작업 범위 외 변경이 발견된 경우
  - 정정 라운드 / 큰 변경

**✓ 체크**: 보고 완료. 사용자 추가 지시 대기.

---

## 11. SOP 위반 시 영향 (실제 사례)

본 SOP 의 step 을 skip 하거나 ✓ 체크 누락 시 다음 패턴 발생 (SOP 도입 트리거 사례: 임베디드 분석 세션):

| skip 한 step | 발생한 문제 |
|--------------|-------------|
| Step 2 (요구사항 기록) | 추후 이력 추적 불가, 동일 요구 반복 |
| Step 3 (기존 자료 검색) | 외부 spec 이 `manual/` 에 있는데 다시 다운로드 시도 / 워커가 같은 분석 반복 |
| Step 4 (manual-first 룰) | "TYP=권장" 역방향 비약 같은 거짓 단정 (벤더 SDK 매크로 → silicon spec 비약) |
| Step 5 (사전 승인) | 코드 수정 / 큰 변경 사용자 동의 없이 진행 |
| Step 7 (검증) | 일괄 정정 적용 (`replace_all`) 후 verbose 결과 — 함수명 / 도메인 용어 일괄 치환 후 가독성 손상 |

**핵심 원칙**: 각 step 사이의 ✓ 체크는 다음 step 진행 전 명시적 확인. "한 번에 다 처리" 보다 "1 step 1 verify".

상세 case study (정정 라운드 5회 사례) 는 본 SSOT push 대상 외 — 도입 프로젝트 로컬의 정정 이력 문서에 보존.

---

## 12. 변경 절차

본 룰은 SSOT 이므로 변경 시 **사용자 승인 필수**. 변경 후:
1. CLAUDE.md §0 표 갱신 확인
2. README.md 표 / 원본 미반영 목록 동기화 확인
3. Skill 파일 (필요 시) 동기화
4. CHANGELOG / VERSION (semver) 갱신

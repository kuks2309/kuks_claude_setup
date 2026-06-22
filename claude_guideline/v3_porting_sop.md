# v3 번들 이식 SOP — Self-Contained

v1/v2 SSOT(Single Source of Truth) 작성·정제 후 **v3 (`kuks_claude_skill_setup`) 번들 이식 의무화**. v1 까지만 sync 하고 v3 이식 또는 계획이 없으면 본 SOP(Standard Operating Procedure) 위반.

## 핵심 모토

> v1/v2 작성·sync 만으로는 작업 종료가 아니다 — v3 이식 또는 명시적 이식 계획이 동반돼야 한다.

본 프로젝트의 최종 목적은 v3 번들 이식. v1/v2 단계는 **SSOT 정제 트랙**이며, 정제된 SSOT 가 v3 번들 구조로 재가공돼 타깃 프로젝트에 install 가능한 형태가 되는 것이 종착점.

---

## 설치 위치

- **본 파일**: 대상 프로젝트의 `docs/claude_guideline/v3_porting_sop.md` 에 배치
- 본 파일이 위 경로에 없으면 본 정책은 활성화되지 않는다

---

## 1. 3 단계 트랙 정의

| 트랙 | 위치 | 목적 | 산출물 |
|---|---|---|---|
| **v2** | `/home/amap/Project/claude_code/kuks_claude_setup_new/` (비-git) | SSOT 작성·revision 워크스페이스 | `claude_guideline/<name>.md` 플랫 SSOT |
| **v1** | `/home/amap/Project/claude_code/kuks_claude_setup/` (git, origin=`kuks2309/kuks_claude_setup`) | git sync 배포 위치 | v2 와 동일 파일 |
| **v3** | `/home/amap/Project/claude_code/kuks_claude_skill_setup/` (origin=`kuks2309/kuks_claude_agent_setup` + fito=`FitoControl/FITO_claude_skill_install`) | **번들 이식 최종 목적지** | `<bundle>/domains/<name>.md` + `<bundle>/claude.snippet.md` + `<bundle>/checks/` + `<bundle>/ci/` + `<bundle>/install.sh` |

v2 작성은 [[feedback-v1-v2-migration-workflow]] §1, v1 sync 는 §2, v3 이식이 §3 — 본 SOP 가 §3 의 권위 SSOT.

---

## 2. v1/v2 → v3 매핑 규약

### 2.1 SSOT 파일 → 번들 매핑

| v1/v2 SSOT | v3 번들 |
|---|---|
| `claude_guideline/coding.md` 또는 `claude_guideline/coding/*.md` | `coding/` |
| `claude_guideline/code_review.md` | `code_review/` |
| `claude_guideline/sw_structure.md` | `sw_structure/` |
| `claude_guideline/external_reference_handling.md` | `external_reference/` |
| `claude_guideline/user_instruction_recording.md` | `user_instruction/` |
| `claude_guideline/github.md` 또는 `claude_guideline/remote_push_policy.md` | `git_workflow/` |
| `claude_guideline/iteration_anti_pattern.md` | `issue_fix/` (예정) |
| 신규 SSOT | 적합한 기존 번들 또는 사용자 명시 승인 후 신규 번들 신설 |

### 2.2 플랫 SSOT 의 부분 → 번들 구성요소 분해

| v1/v2 SSOT 의 부분 | v3 번들 구성요소 | 비고 |
|---|---|---|
| 도메인별 룰 (ros2 / embedded / concurrency 등) | `<bundle>/domains/<domain>.md` | 도메인 1 파일 |
| 도메인 공통 룰 | `<bundle>/<core>.md` (예: `coding/coding.md`, `coding/conventions.md`) | 코어 1~여러 파일 |
| 자체 점검 grep | `<bundle>/checks/<name>.sh` | 실행 가능 스크립트 |
| CI(Continuous Integration) 훅 | `<bundle>/ci/<name>.yaml` 또는 `<bundle>/ci/<name>.sh` | 선택적 |
| CLAUDE.md 등록 포인터 한 줄 | `<bundle>/claude.snippet.md` | 순수 포인터, 룰 본문 금지 |
| 설치 절차 | `<bundle>/install.sh` | 번들 단위, 도메인 선택 옵션 `--all` 또는 도메인 지정 |
| 도메인 README | `<bundle>/README.md` 또는 `<bundle>/domains/README.md` | 도메인 목록·요약 |

---

## 3. 이식 절차

새 SSOT 작성 또는 기존 SSOT 의 큰 수정 시 다음 단계를 거친다.

### 3.1 v2 작성·검증 ([[feedback-v1-v2-migration-workflow]] §1)

`kuks_claude_setup_new/claude_guideline/<name>.md` 에 self-contained SSOT 작성.

### 3.2 v1 sync ([[feedback-v1-v2-migration-workflow]] §2)

`kuks_claude_setup/claude_guideline/<name>.md` 로 cp, 별도 `docs/<topic>` 브랜치에서 commit + push.

### 3.3 v3 이식 (★ 본 SOP 의 핵심)

#### 3.3.1 매핑 결정

§2.1 표에 따라 v3 번들 결정. 신규 번들 필요 시 사용자 명시 승인 (`[[project-kuks-agent-setup]]` 의 "루트 중앙 디스패처 금지" 룰 준수).

#### 3.3.2 분해

§2.2 표에 따라 SSOT 의 각 부분을 번들 구성요소로 분해:

- 룰 본문 → `<bundle>/domains/<domain>.md` 또는 `<bundle>/<core>.md`
- 자체 점검 grep → `<bundle>/checks/<name>.sh`
- CLAUDE.md 등록 포인터 한 줄 → `<bundle>/claude.snippet.md` (마커 `kuks_agent_setup:<bundle>` 사용)

#### 3.3.3 번들 install.sh 갱신

번들의 `install.sh` 가 새 도메인 / 새 코어 파일을 install 대상에 포함하도록 수정. 도메인 선택 인자 패턴 유지 (`./install.sh <타깃> [도메인...|--all]`).

#### 3.3.4 sync 룰 적용 (dual-remote)

v3 (`kuks_claude_skill_setup/`) 은 origin + fito 두 remote 모두 push 대상. `claude_guideline/remote_push_policy.md` 적용 — push 전 `git remote -v` 확인 → 모든 remote 에 push → SHA(Secure Hash Algorithm) 일치 검증.

### 3.4 즉시 이식이 어려운 경우

번들 구조 결정 필요, 다른 SSOT 와 조정 필요, 사용자 검토 대기 등의 사유로 즉시 이식이 어려우면 **이식 계획 follow-up 등록**으로 §3.3 을 대체 가능.

위치: `docs/followups/<sop-name>-v3-porting.md` (v1 repo, 같은 docs 브랜치).

양식:

```markdown
# v3 Porting Follow-up: <SOP-NAME>

- **소스 (v1)**: `claude_guideline/<name>.md`
- **소스 (v2)**: `kuks_claude_setup_new/claude_guideline/<name>.md`
- **목표 번들**: v3 의 `<bundle>/` 또는 신규 번들 `<new-bundle>/`
- **분해 계획**:
  - 룰 본문 → `<bundle>/domains/<domain>.md`
  - 자체 점검 grep → `<bundle>/checks/<name>.sh`
  - 스니펫 → `<bundle>/claude.snippet.md`
- **블로커**: (있을 시) 번들 구조 결정 / 다른 SSOT 조정 / 사용자 검토 대기 등
- **일정**: 다음 세션 / N 일 내 / TBD(To Be Determined)
```

follow-up 파일도 git 추적 (별도 docs 브랜치, 또는 SSOT 와 같은 브랜치).

---

## 4. 종료 게이트 (★ 강제)

SSOT 작업의 종료로 인정받으려면 다음 4 항목 모두 충족:

1. **v2 SSOT 작성·검증 완료**
2. **v1 sync commit·push 완료**
3. **v3 이식 완료** 또는 **명시적 v3 이식 follow-up 파일 등록**
4. **CLAUDE.md 진입표 등록** (v1 의 workspace 와 v3 번들의 `claude.snippet.md` 양쪽)

조건 3 이 가장 중요 — v3 이식 또는 follow-up 둘 중 하나는 반드시. **v2 작성 + v1 sync 만으로 종료 선언 = 본 SOP 위반**.

---

## 5. 위배 사례 backfill

본 SOP 작성 (2026-06-21) 이전의 v1/v2 SSOT 작업은 v3 이식 누락 가능성. 본 SOP 활성화 시점에 다음을 점검·backfill:

### 5.1 점검 대상

`kuks_claude_setup_new/claude_guideline/` 와 `kuks_claude_setup/claude_guideline/` 의 모든 SSOT 파일.

### 5.2 backfill 절차

각 SSOT 에 대해:

1. v3 `kuks_claude_skill_setup/` 에서 매핑된 번들 위치에 해당 도메인 파일이 존재하는지 확인
2. 존재하지 않으면 follow-up 파일 (`docs/followups/<name>-v3-porting.md`) 등록 또는 즉시 이식

### 5.3 알려진 위배

- `claude_guideline/coding/ros2.md` (§8 인터페이스 감사 SOP 등 2026-05~06 작업) — `kuks_claude_skill_setup/coding/domains/ros2-coding.md` 가 untracked 상태, §8 SOP 미반영. follow-up 등록 또는 이식 필요.
- `claude_guideline/remote_push_policy.md` (2026-06-21 신설) — v3 `git_workflow/` 번들 미반영. follow-up 등록 필요.
- 기타 v2 `claude_guideline/` 의 모든 파일 — 각각 v3 매핑 점검 의무.

---

## 6. 자체 점검 grep

```bash
V2=/home/amap/Project/claude_code/kuks_claude_setup_new/claude_guideline
V3=/home/amap/Project/claude_code/kuks_claude_skill_setup
V1=/home/amap/Project/claude_code/kuks_claude_setup

# v2 SSOT 중 v3 미반영 + follow-up 미등록 검출
for f in $V2/*.md $V2/**/*.md; do
    [ -f "$f" ] || continue
    name=$(basename "$f" .md)
    # v3 어딘가에 해당 키워드가 등장하는지 (간이 매칭)
    found_v3=$(grep -lrI "$name" $V3 2>/dev/null | grep -v '/.git/' | head -1)
    # follow-up 파일 존재 여부
    followup="$V1/docs/followups/${name}-v3-porting.md"
    if [ -z "$found_v3" ] && [ ! -f "$followup" ]; then
        echo "❌ $name: v3 미반영 + follow-up 미등록 (본 SOP §4 종료 게이트 위반)"
    elif [ -z "$found_v3" ]; then
        echo "⚠ $name: v3 미반영 (단 follow-up 등록됨)"
    else
        echo "✅ $name: v3 반영 확인 (또는 키워드 매칭)"
    fi
done
```

---

## 7. 종료 체크리스트

### A. 기술 부채 방지
- [ ] v3 매핑 결정 완료 (§2.1 표 또는 신규 번들 사유)
- [ ] §2.2 표에 따른 분해 완료 (룰 / grep / snippet / install)
- [ ] v3 번들의 `install.sh` 가 새 자산 포함 (도메인 선택 옵션 유지)
- [ ] §6 자체 점검 grep 통과 (❌ 0건)

### B. 이해 부채 방지
- [ ] v3 의 해당 번들 `claude.snippet.md` 가 타깃 CLAUDE.md 등록 가능 (포인터 한 줄, 룰 본문 금지)
- [ ] v3 번들의 `README.md` 가 새 도메인 명시
- [ ] v3 매핑이 §2.1 표에 정합 (신규 번들 시 표 갱신)

### C. 의도 부채 방지
- [ ] 즉시 이식 못 한 경우 follow-up 파일 등록 (`docs/followups/<sop-name>-v3-porting.md`)
- [ ] 신규 번들 신설 시 사용자 명시 승인 기록 ([[project-kuks-agent-setup]] 의 "루트 중앙 디스패처 금지" 준수)

### D. 위반 / 예외 / 인계
- [ ] §5 위배 사례 backfill 점검 결과 명시
- [ ] §4 종료 게이트 4 항목 충족 여부 명시 ("위반 없음" 한 줄도 가능)

---

## 룰 (요약)

1. **v3 이식 의무화** §3 — v1/v2 SSOT 작업은 v3 이식 또는 명시적 follow-up 동반 의무
2. **3 단계 워크플로** §1 — v2 작성 → v1 sync → v3 이식 (3 단계 모두 완료해야 종료)
3. **매핑 규약 준수** §2 — v1/v2 SSOT 의 부분을 v3 번들 구성요소로 분해 (룰/grep/snippet/install)
4. **즉시 불가 시 follow-up 등록 의무** §3.4 — `docs/followups/<name>-v3-porting.md`
5. **v3 는 dual-remote** §3.3.4 — origin + fito 양쪽 push, `remote_push_policy.md` 적용
6. **신규 번들은 사용자 명시 승인** §3.3.1 — "루트 중앙 디스패처 금지" 룰 (project_kuks_agent_setup memory)
7. **종료 게이트 4 항목** §4 — v2 / v1 / v3(이식 또는 follow-up) / CLAUDE.md 등록 모두 충족
8. **자체 점검 grep §6** — v2 SSOT 와 v3 미반영 + follow-up 미등록 검출, ❌ 0건 의무
9. **backfill 점검 의무** §5 — 본 SOP 활성화 시점에 기존 SSOT 들의 v3 이식 상태 점검
10. **v2 작성 + v1 sync 만으로 종료 선언 금지** §4 — 본 SOP 위반

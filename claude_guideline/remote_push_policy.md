# 다중 원격 저장소 동기 정책 (Remote Push Policy) — Self-Contained

Git push 시 **등록된 모든 remote 에 동기**하기 위한 SSOT(Single Source of Truth). 본 파일 1개로 자체 완결.

## 설치 위치

- **본 파일**: 대상 프로젝트의 `docs/claude_guideline/remote_push_policy.md` 에 배치
- 본 파일이 위 경로에 없으면 본 정책은 활성화되지 않는다. 새 프로젝트 적용 시 본 파일을 위 경로로 복사하는 것이 첫 단계.

## 모토 — 한쪽에만 올리지 않는다

다중 remote 가 등록된 저장소는 한 remote 에만 push 하면 **미러 불일치(divergence)** 가 발생한다. 불일치한 미러는 다음 작업자가 어느 remote 가 권위 소스인지 알 수 없게 만든다. 모든 remote 를 동등 권위로 유지한다.

---

## 1. push 전 표준 절차 (★ 강제 게이트)

작업자는 push 전에 다음 3단계를 거친다. 한 단계라도 생략 시 본 정책 위반.

### 1.1 등록된 모든 remote 열거

```bash
git remote -v
```

출력에 `(fetch)` + `(push)` 짝으로 등록된 모든 remote 가 나온다. **폴더명만 보고 remote 를 추정하지 않는다** — 폴더명과 origin repo 명이 다를 수 있다 (§2 예시).

### 1.2 각 remote 의 현재 브랜치 상태 확인

```bash
BR=$(git branch --show-current)
for r in $(git remote); do
    echo "[$r/$BR]"
    git ls-remote --heads $r $BR | head -1
done
```

세 가지 가능한 결과:

| 결과 | 의미 | 조치 |
|---|---|---|
| **A. 모두 동일 SHA**(Secure Hash Algorithm) | 이미 동기 | 추가 push 불요. 새 커밋 push 시 §1.3 그대로 |
| **B. 한쪽이 ahead, 다른 쪽이 같음/뒤짐** | 일부 remote 누락 push | ahead 인 remote 의 HEAD 를 다른 remote 에도 push |
| **C. 양쪽이 서로 다름 (divergent)** | fast-forward 불가 | 사용자 **명시 승인 후에만** 결정 (force-push 또는 merge) |

### 1.3 모든 remote 에 push

순차적으로 명시 push (권장 — 출력 명확):

```bash
git push origin $BR
git push fito $BR
# ... 등록된 모든 remote
```

또는 일괄:

```bash
for r in $(git remote); do
    git push $r $BR
done
```

push 중 한 remote 가 실패하면 다른 remote 의 결과와 무관하게 미러 불일치 발생 — §3 자체 점검 grep 필수.

---

## 2. 폴더명과 origin repo 명이 다를 수 있다

`git clone <url> <folder>` 또는 `git clone <url>` 후 `mv` 로 폴더명을 바꾸면, 폴더명과 origin repo 명이 일치하지 않는다. **폴더명 ≠ origin repo 명** 인 경우는 흔하다.

예 (관찰된 매핑):

```text
로컬 폴더:       kuks_claude_skill_setup
origin remote:   github.com/kuks2309/kuks_claude_agent_setup
fito remote:     github.com/FitoControl/FITO_claude_skill_install
```

위 예에서 폴더명·origin·fito 가 모두 다르다. 추측 금지, 매번 `git remote -v` 로 확인.

---

## 3. 자체 점검 grep

push 후 모든 remote 가 로컬 HEAD 와 일치하는지 검증:

```bash
LOCAL=$(git rev-parse HEAD)
BR=$(git branch --show-current)
for r in $(git remote); do
    REMOTE_SHA=$(git ls-remote $r $BR | cut -f1)
    if [ "$LOCAL" = "$REMOTE_SHA" ]; then
        echo "✅ $r: 동기 ($REMOTE_SHA)"
    else
        echo "❌ $r: 불일치 — 로컬=$LOCAL, $r=$REMOTE_SHA"
    fi
done
```

❌ 가 1건 이상이면 본 정책 위반 — 종료 체크리스트 §6 D 에 기재.

---

## 4. force-push 가드

다음 경우 force-push (`git push --force` 또는 `--force-with-lease`) 는 **사용자 명시 승인 후에만** 실행:

- §1.2 결과가 C (divergent)
- 커밋 history rewrite 후 push (`git rebase`, `git commit --amend`, `git reset`)
- 백업 브랜치(`backup/*`) 의 force-push

이유: 미러 환경에서 한 remote 의 force-push 는 다른 remote 와의 동기를 깨뜨린다. 깨진 미러의 복구는 어렵다 (어느 쪽이 권위 소스인지 의사 결정 필요).

`--force-with-lease` 가 `--force` 보다 안전 (다른 작업자의 push 를 우연히 덮어쓰지 않음). 가능하면 lease 형식 사용.

---

## 5. 새 remote 추가 규약

새 remote 추가 절차:

```bash
git remote add <name> <url>
git fetch <name>          # 존재 검증 — 404 / 권한 오류 즉시 검출
```

- remote 이름은 관습 사용: `origin` / `upstream` / `fork` / 조직 명(`fito`, `lab`)
- 추가 직후 `fetch` 실패 (`Repository not found`, `Permission denied`) 시 즉시 `git remote remove <name>` 으로 정리. 잘못된 remote 가 등록된 채로 두면 후속 push 실패 원인.

---

## 6. 종료 체크리스트

push 작업 종료 시 다음 4 항목 모두 충족.

### A. 동기 (Sync)

- [ ] `git remote -v` 로 등록 remote 전수 확인 (§1.1)
- [ ] 모든 remote 에 push 완료 (§1.3)
- [ ] §3 자체 점검 grep 으로 모든 remote SHA 가 로컬 HEAD 와 일치

### B. 안전 (Safety)

- [ ] force-push 사용 시 사용자 명시 승인 기록 (§4)
- [ ] 새 remote 추가 시 `fetch` 로 존재 검증 (§5)

### C. 기록 (Record)

- [ ] commit message 에 변경 사유 명시 (커밋 단위 = 작업 단위 분리)
- [ ] 다중 remote 환경에서 동기화 후 어느 remote 가 trigger 인지 PR / 이슈 본문에 명시 (필요 시)

### D. 위반 / 예외 / 인계

- [ ] §3 ❌ 발생 시 원인 + 후속 조치 명시
- [ ] divergent 미해결 시 사유 + 다음 작업자 지침 명시 (예: "fito 가 권위 소스 — origin 을 fito 로 reset 필요")
- [ ] 무위반이면 "위반 없음" 한 줄

---

## 7. 적용 범위 자동 판정

| 범위 | 조건 | 처리 |
|---|---|---|
| **다중 remote** | `git remote -v` 결과 2개 이상 | 전 절차 적용 |
| **단일 remote** | 1개 (대부분 `origin`) | §1.2 / §3 의 다중 비교 단계 생략, 단일 remote push 만 |
| **remote 없음** | 0개 | 본 정책 무관 (로컬 전용 repo) |

판정은 작업 시작 시 1회 수행. 작업 중 remote 변경 시 재판정.

---

## 룰 (요약)

1. **push 전 `git remote -v` 의무** §1.1 — 매번 확인
2. **다중 remote 면 전부 push** §1.3 — 한쪽만 올리는 것 금지
3. **폴더명 추정 금지** §2 — 폴더명 ≠ origin repo 명 가능
4. **§3 SHA 일치 검증** — push 후 모든 remote 의 HEAD 일치 확인
5. **force-push 는 사용자 명시 승인** §4
6. **새 remote 는 `fetch` 로 존재 검증** §5
7. **divergent (C) 는 사용자 결정** §1.2
8. **종료 체크리스트 §6** — A 동기 / B 안전 / C 기록 / D 위반 4 절 모두
9. **`--force-with-lease` 가 `--force` 보다 안전** §4
10. **잘못 추가한 remote 즉시 제거** §5 — 미정리 상태 유지 금지

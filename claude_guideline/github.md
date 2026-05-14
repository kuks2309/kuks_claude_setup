# Git / GitHub 작업 규칙

Git / GitHub 작업의 단일 근원 SSOT. "기록" 자연어 단축어, commit / push 승인, 브랜치 정책, 커밋 메시지 규칙을 모두 본 파일이 책임진다.

## "기록" 명령 처리 (자연어 단축어)

사용자가 "기록" 또는 "기록해" 라고 지시하면 다음 4 단계를 모두 수행한다:

1. 관련 docs (`docs/user_instructions/user_instructions.md`, `docs/issues_and_fixes/issues_and_fixes.md` 등) 에 SSOT 형식대로 entry 추가
2. 변경 파일 staging (`git add <명시 파일>`)
3. 커밋 생성 (`git commit`, 작업 단위 1 커밋)
4. push (`git push` 현재 추적 분기로)

**근거**: 사용자 명시 지시 (2026-05-08 / 05-09 재확인) — "기록" 은 단축어 워크플로이며 commit + push 모두 포함.

### 단축어의 예외

- "커밋만" / "푸쉬만" 처럼 단계 한정 시 그 범위만 수행 (단축어 적용 X).
- 외부 vendored / SSOT 클론의 원격 push 는 본 단축어 대상이지만, push 직전 사용자 명시 확인 필수 (§Push 전 확인 절).
- 파괴적 명령 (`git push --force`, `git reset --hard` 등) 은 본 단축어 적용 외, 사용자 명시 승인 후에만 실행.

## 작업 단위 = 커밋 단위 = push 단위

서로 다른 영역 / 의도의 변경은 별도 commit 으로 분리하고 각자 push 한다.

```bash
git add <영역 A 파일들>
git commit -m "<type>(<scope-A>): ..."
git push

git add <영역 B 파일들>
git commit -m "<type>(<scope-B>): ..."
git push
```

복합 변경을 하나의 commit 으로 묶지 않는다.

## 일반 Git 작업 규칙

- 사용자 명시 요청 없이 commit / push 수행 금지. "기록" / "커밋" / "푸쉬" 자연어 단축어는 예외.
- 코드 수정 후에는 staging 까지만 수행하고 commit 은 사용자 지시 ("기록" 또는 "커밋") 로 진행.
- 파괴적 명령 (`git push --force`, `git reset --hard`, 브랜치 삭제, `git clean -f` 등) 은 사용자 명시 승인 후에만 실행.
- 외부 vendored 저장소 (read-only 가드 목록) 에는 절대 push 하지 않는다.

## 브랜치 / PR 정책

본 워크스페이스 (kuks_claude_setup 자산 큐레이션) 기본은 **현재 추적 분기 직접 push 모델** — PR / feature branch / merge 워크플로 미사용.

- 일상 변경: `master` 직접 commit + push.
- **예외 — 대규모 재구조화**: 사용자가 명시한 경우 (예: `feature/<name>` 분기 + worktree) feature branch 사용. merge 시 사용자 명시 승인 필수.
- 브랜치 네이밍 / 리뷰어 / merge 정책 강제 없음 — 사용자 판단.

## 커밋 메시지

- 권장 형식: `<type>(<scope>): <subject>`
- 타입 예: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`
- 본문에 변경 사유와 관련 이슈 번호 (있다면) 명시 권장
- 동일 세션 worklog 존재 시 본문 prose 를 `Worklog: docs/worklog/YYYY-MM-DD.md` 한 줄 링크로 대체 가능 — SSOT 는 worklog, commit message 는 요약
- worklog 만 별도 정리하는 커밋은 `docs(worklog): YYYY-MM-DD 정리` 로 분리

## Push 전 확인

다음 조건 모두 만족 후 push:

- [ ] 사용자 명시 지시 ("기록" / "푸쉬" / 직접 push 명령) 가 있다
- [ ] 외부 vendored / SSOT 클론이면 push 직전 사용자 명시 확인 받았다
- [ ] 파괴적 명령이면 사용자 명시 승인 받았다
- [ ] 변경 파일이 의도 범위 내 ([workflow.md](workflow.md) 종료 전 체크리스트)

## 변경 절차

본 룰은 SSOT. 변경 시 사용자 승인 필수.

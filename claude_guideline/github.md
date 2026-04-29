# GitHub 워크플로

Git 및 GitHub 관련 작업 규칙의 단일 근원.

## 기록 요청 처리 규칙

사용자가 "기록" 또는 "기록해" 등의 지시를 내리면 다음을 **모두** 수행한다.

1. 요구사항 기록(`docs/request/requests.md`) 및 이슈 기록(`docs/issues_and_fixes/issues_and_fixes.md`) 갱신
2. 변경 파일 staging (`git add`)
3. 커밋 생성 (`git commit`)
4. 원격 저장소로 푸쉬 (`git push`)

## 일반 Git 작업 규칙

- 사용자가 명시적으로 요청하지 않은 commit/push 는 수행하지 않는다.
- 코드 수정 후에는 staging 까지만 수행하고, commit 은 사용자 지시(예: "기록")를 받아 진행한다.
- 파괴적 명령(force push, `reset --hard`, 브랜치 삭제 등)은 사용자 명시 승인 후에만 실행한다.
- read-only 로 지정된 외부 저장소에는 절대 push 하지 않는다 (프로젝트별 read-only 저장소는 CLAUDE.md "프로젝트 성격" 섹션 참조).

## 커밋 메시지

- 형식: `<type>(<scope>): <subject>` (기존 커밋 로그와 일관성 유지)
- 타입 예: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- 본문에 변경 사유와 관련 PRD/ADR 번호 명시 권장

## Push 전 확인

- 변경 파일이 사용자가 요청한 범위 내인지 재확인
- 비밀(.env, 키, 토큰)이 포함되지 않았는지 확인
- 대상 저장소가 의도한 저장소인지 (원본 저장소가 아닌지) 확인

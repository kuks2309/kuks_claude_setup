# 작업 절차 체크리스트 (Workflow Checklist)

작업 단위마다 **시작 전 / 종료 전** 점검 항목 SSOT (Single Source of Truth / 단일 근원). 항목별 세부 규칙은 영역별 SSOT 가 책임지며 본 파일은 진입 체크리스트만 둔다.

## 작업 시작 전

- [ ] 사용자 지시 원문을 [user_instruction_recording.md](user_instruction_recording.md) 형식대로 **즉시 기록** 했는가? (작업 시작 전)
- [ ] 워크스페이스 루트 `CLAUDE.md` + 관련 SSOT 룰을 확인했는가?
- [ ] 모듈 CLAUDE.md (있다면) 를 먼저 읽었는가?
- [ ] 관련 기존 자료·매뉴얼·실수 기록을 조사했는가?
- [ ] 사전 승인 트리거 ([coding.md](coding.md) §사전 승인) 에 해당하는가?
- [ ] 외부 vendored / read-only 경로 ([github.md](github.md) §외부 SSOT) 를 건드리는가?
- [ ] 임의 수정·범위 초과를 하지 않을 것을 확인했는가?

## 작업 종료 전

- [ ] 사용자 지시 범위 안에서만 작업했는가?
- [ ] 요청하지 않은 기능·파일·주석을 추가하지 않았는가?
- [ ] 중복 코드·함수·변수를 점검했는가?
- [ ] 임시 디버그 print / 진단 stub 을 제거했는가? ([tech_debt.md](tech_debt.md))
- [ ] 빌드와 기본 동작이 깨지지 않는가?
- [ ] 변경 파일이 의도 범위 내인가? (`git status --short`, `git diff --cached --name-only`)
- [ ] 사용자 명시 승인 또는 자연어 단축어 ("기록" / "커밋" / "푸쉬") 없이 commit / push 하지 않았는가? ([github.md](github.md) §"기록" 명령)
- [ ] 본 작업 중 발생한 실수는 도메인 실수 기록 (예: `docs/claude-mistake/`) 에 남겼는가?

## 보고 형식

다음 시점에만 변경 사유·영향·확인을 명시한다:

- 사전 승인 트리거 변경 착수 전
- 우회 / workaround 사용 결정 전
- "기록" 명령 처리 시 (commit 범위 보고)
- 작업 범위 외 변경이 발견된 경우
- 정정 라운드 또는 큰 변경

일상 작업 종료 시에는 1~2줄 결과 보고로 충분하다.

## 변경 절차

본 룰은 SSOT. 변경 시 사용자 승인 필수.

## 본 파일이 다루지 않는 것

도메인 / 영역별 절차는 별도 SSOT 가 책임지며 본 체크리스트는 진입점만 둔다:

| 영역 | SSOT 파일 |
|------|----------|
| 사용자 지시 원문 기록 | [user_instruction_recording.md](user_instruction_recording.md) |
| 코드 작업 규칙 / 사전 승인 | [coding.md](coding.md) |
| 기술 부채 (우회·임시 코드) | [tech_debt.md](tech_debt.md) |
| Git / GitHub / "기록" 명령 | [github.md](github.md) |
| 외부 매뉴얼·데이터시트 | [manual.md](manual.md) |
| ROS2 / 임베디드 / 펌웨어 플래시 | [ros2.md](ros2.md) |
| 반복 수정 회피 | [iteration_anti_pattern.md](iteration_anti_pattern.md) |
| 문서 작성 메타 룰 | [documentation.md](documentation.md) |

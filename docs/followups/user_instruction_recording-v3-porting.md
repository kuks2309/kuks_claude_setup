# v3 Porting Follow-up: user_instruction_recording

- **소스 (v1)**: `claude_guideline/user_instruction_recording.md`
- **소스 (v2)**: `kuks_claude_setup_new/claude_guideline/user_instruction_recording.md`
- **목표 번들**: v3 의 `user_instruction/` 번들 — **이미 동명 자산 존재 (`recording.md`)**
- **현재 v3 `user_instruction/` 구조** (2026-06-21 시점, tracked):
  - `recording.md` (코어 — v1/v2 `user_instruction_recording.md` 의 v3 동등 가능성 높음)
  - `claude.snippet.md`
  - `install.sh`
- **분해 계획**:
  - **우선 작업**: v1/v2 `user_instruction_recording.md` 와 v3 `user_instruction/recording.md` 의 **내용 diff 점검** (`diff <v1/v2-소스> <v3-recording>`) — 동기 상태이면 본 follow-up 즉시 종결 (v3 반영 완료로 격상)
  - 차이가 있으면: v1/v2 의 최신 변경분(설치 위치·형식·룰 등 항목)을 v3 `recording.md` 에 반영
  - CLAUDE.md 등록 포인터·`install.sh` 는 이미 v3 에 존재 — 추가 작업 없음 가능
- **블로커**: diff 점검 미실시 (5분 내 작업)
- **일정**: 다음 세션 시작 시 diff 1회 — 동기 시 follow-up 종결, 아니면 차이 분석 후 이식
- **dual-remote 의무**: 이식 commit 시 v3 의 origin + fito 양쪽 push

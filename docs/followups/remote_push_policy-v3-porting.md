# v3 Porting Follow-up: remote_push_policy

- **소스 (v1)**: `claude_guideline/remote_push_policy.md`
- **소스 (v2)**: `kuks_claude_setup_new/claude_guideline/remote_push_policy.md`
- **목표 번들**: v3 의 `git_workflow/` 번들 (v3_porting_sop.md §2.1 매핑 표 정합)
- **현재 v3 `git_workflow/` 구조** (2026-06-21 시점, tracked):
  - `git_workflow.md` (코어)
  - `claude.snippet.md`
  - `install.sh`
- **분해 계획**:
  - 룰 본문 → `git_workflow/git_workflow.md` 의 한 절로 통합 (예: "§N. 다중 원격 저장소 동기 정책") **또는** 별도 `git_workflow/remote_push_policy.md` 신설 (단일 파일 vs 분리는 §3.3.2 분해 결정)
  - §3 SHA(Secure Hash Algorithm) 일치 검증 grep → `git_workflow/checks/remote_push_policy.sh` (신규 디렉토리·파일)
  - CLAUDE.md 등록 포인터 → `git_workflow/claude.snippet.md` 의 기존 git_workflow 마커 내에 한 줄 추가
  - `install.sh` 갱신 → `checks/` 스크립트 설치 포함
- **블로커**:
  - `git_workflow.md` 의 기존 내용 확인 필요 (중복 / 충돌 회피)
  - "단일 파일 통합" vs "별도 파일 분리" 의사 결정 (단일 파일이 단순, 분리가 모듈성 우위)
- **일정**: 다음 세션 (블로커 해소 가능 시 즉시 이식)
- **dual-remote 의무**: 이식 commit 은 v3 의 origin (`kuks2309/kuks_claude_agent_setup`) + fito (`FitoControl/FITO_claude_skill_install`) 양쪽 push — 본 SSOT(Single Source of Truth) 자체가 정의한 룰 적용

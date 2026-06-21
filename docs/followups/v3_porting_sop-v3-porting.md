# v3 Porting Follow-up: v3_porting_sop

- **소스 (v1)**: `claude_guideline/v3_porting_sop.md`
- **소스 (v2)**: `kuks_claude_setup_new/claude_guideline/v3_porting_sop.md`
- **목표 번들**: TBD(To Be Determined) — 본 SOP(Standard Operating Procedure) 는 메타 SOP(v3 이식 절차 자체를 정의)이므로 v3 의 어느 번들에도 자연스럽게 들어가지 않음. 다음 옵션 사용자 검토 필요:
  - **(A)** v3 에 신규 메타 번들 `v3_porting/` 신설 — v3 가 자기 이식 SOP 를 보유 (셀프 부트스트랩)
  - **(B)** `git_workflow/` 번들에 통합 — 이식 = 워크플로의 한 측면으로 분류
  - **(C)** v3 자체에는 이식 안 함 — v1/v2 단계에서만 적용되는 룰로 정의 (v3 는 이식 결과물이므로 본 SOP 가 필요 없음 — 합리적 옵션)
- **분해 계획** (옵션 A/B 선택 시):
  - 룰 본문 → `<bundle>/v3_porting_sop.md` 또는 `<bundle>/domains/v3-porting.md`
  - §6 자체 점검 grep → `<bundle>/checks/v3-porting.sh` (실행 가능 스크립트)
  - CLAUDE.md 등록 포인터 한 줄 → `<bundle>/claude.snippet.md` 의 v3 이식 라인
  - `install.sh` 갱신 → 새 자산 설치 포함
- **블로커**:
  - 매핑 결정 (옵션 A/B/C 중 하나, 사용자 검토 대기)
  - 옵션 A 선택 시 `project_kuks_agent_setup` memory 의 "루트 중앙 디스패처 금지" 룰 정합성 검증 + 신규 번들 신설 사용자 명시 승인
  - 옵션 C 가 가장 단순 — v1/v2 만 적용되는 룰이라면 v3 에는 무관
- **일정**: 사용자 옵션 선택 후 다음 세션 (옵션 C 면 즉시 종결)

# Changelog

본 폴더 (`claude_guideline/`) 의 변경 이력. 형식: [Keep a Changelog](https://keepachangelog.com/) + semver.

## 2.0.0 — 2026-05-13

v2 전면 재구조화. 단일 책임 원칙으로 SSOT 분리, 영역 간 중복 제거.

### Added

- [user_instruction_recording.md](user_instruction_recording.md) — 사용자 지시 원문 기록 SSOT (이전 `user_instruction_handling_sop.md` 9-step 중 Step 2 만 단일 책임으로 분리).
- [README.md](README.md) §영역 매트릭스 — 11 개 SSOT 의 영역 매핑 표.
- [coding.md](coding.md) §단일 파일 작업 분기 표 — 의도 명확 / 모호 × 파일 종류별 분기.
- [tech_debt.md](tech_debt.md) §정공법 범위 초과 절차 — 자율 실행 금지 + 강제 보고 절차.
- [iteration_anti_pattern.md](iteration_anti_pattern.md) §Iteration Loop 탈출 규칙 — 2 회째 부분 수정 요청 시 의도 재확인 → 전체 재작성.
- [skill_update.md](skill_update.md) §자동화 정책 — 4 표현 (명시 호출 / 권고 / passive cite / 금지) + 화이트리스트 3 종.
- [documentation.md](documentation.md) §SSOT 경로 (Authoring vs Mirror) — `kuks_claude_setup/claude_guideline/` 단일 authoring + `docs/claude_guideline/` mirror.
- [documentation.md](documentation.md) §용어 표준 (Terminology SSOT) — 스킬 / 에이전트 / 워크플로 / 사용자 지시사항 / 지침 표준 표기.
- [documentation.md](documentation.md) §docs 표준 폴더 — 다운스트림 `docs/` 의 표준 폴더 정의.
- [ros2.md](ros2.md) §펌웨어 다운로드 절차 — v1 의 `workflow.md` 에서 이관.

### Changed

- [workflow.md](workflow.md): 순수 cross-domain 체크리스트로 축소. 도메인 특수 (펌웨어 플래시) 분리 → `ros2.md` 이관.
- [github.md](github.md): "기록" 단축어 + 브랜치 / PR 정책 + Worklog SSOT 분리 명시. 직접 push 모델 default, feature branch 는 명시 예외.
- [claude_md.md](claude_md.md): 권장 템플릿 갱신 — `user_instruction_handling_sop.md` 참조 제거, `user_instruction_recording.md` 진입.
- [README.md](README.md) Tier 표: Step 0 ★★ 위치를 `user_instruction_recording.md` 로 교체.
- 모든 SSOT 가 자기 영역만 책임지도록 cross-reference 만 두고 중복 정의 제거.

### Removed

- `user_instruction_handling_sop.md` — 9-step + 12 절의 큰 SOP (253 줄) 폐기. 기록 책임은 `user_instruction_recording.md`, 검색·승인·실행·검증·보고 책임은 `workflow.md` / `coding.md` / `github.md` 등 영역별 SSOT 가 분담.
- `user_instruction_analysis.md` — v1.8.7 에서 `user_instruction_handling_sop.md §12` 로 통합 후 폐기. v2 에서는 큰 결정 / 연구성 절차는 별도 SSOT (`research_subroutine.md`, TBD) 로 재분리 예정.
- v1 `workflow.md` 의 §펌웨어 다운로드 절차 → `ros2.md` 이관.

### Migration

다운스트림 프로젝트 마이그레이션 가이드:

1. `bash docs/claude_guideline/update.sh` — mirror 갱신
2. 워크스페이스 루트 `CLAUDE.md` 의 "참조 자료 규칙" 절 갱신:
   - `user_instruction_handling_sop.md` 참조 → `user_instruction_recording.md` 로 교체
3. 도메인 문서 SSOT 표에 v2 신규 SSOT (e.g. `documentation.md` §SSOT 경로) 참조 필요 시 추가
4. `audit.sh` dry-run 으로 drift 검출 후 정정

## 1.x — 이전 이력

v1.8.7 까지의 이력은 git log (master branch) 참조:

```bash
git log --oneline master -- claude_guideline/CHANGELOG.md
```

또는 `master` branch 의 `claude_guideline/CHANGELOG.md` 직접 열람.

v2 는 v1.8.7 (commit `051d600`) 에서 분기 (`feature/claude_guideline-restructure`).

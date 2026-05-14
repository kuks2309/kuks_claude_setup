# Claude 작업 지침

Claude 가 다운스트림 프로젝트 (ROS2 / 임베디드 / 일반 SW 등) 에서 어떻게 일할지 정의하는 메타 규칙의 단일 근원 (SSOT / Single Source of Truth / 단일 근원).

본 폴더의 규칙은 **다운스트림 프로젝트의 워크스페이스 루트 `CLAUDE.md`** (본 SSOT 저장소에는 없음 — [templates/CLAUDE.md.template](../templates/CLAUDE.md.template) 참조) 의 "문서 작업 규칙" 섹션에서 진입한다. CLAUDE.md 에는 복제하지 않는다.

## 진입점 (읽는 순서)

**Tier 표기**: ★★ 시작점 (모든 작업의 출발), ★ 필독 (모든 프로젝트 공통), ◆ 도메인 특화 (해당 프로젝트일 때만), ◇ override.

| 순서 | Tier | 영역 | 파일 |
|---|---|---|---|
| 0 | ★★ | 사용자 지시 기록 (Step 1) — 의도 부채 차단 | [user_instruction_recording.md](user_instruction_recording.md) |
| 1 | ★ | 작업 절차 체크리스트 (시작 / 종료 + 보고 형식) | [workflow.md](workflow.md) |
| 2 | ★ | 코드 작업 규칙 (작업 범위 / 사전 승인 / 코딩 스타일) | [coding.md](coding.md) |
| 3 | ★ | GitHub 워크플로 + "기록" 단축어 + 브랜치 정책 | [github.md](github.md) |
| 4 | ★ | 기술 부채 방지 (정공법 우선 / 우회 3 조건) | [tech_debt.md](tech_debt.md) |
| 5 | ★ | 반복 수정 회피 (Iteration Loop 탈출) | [iteration_anti_pattern.md](iteration_anti_pattern.md) |
| 6 | ★ | 매뉴얼 / 데이터시트 인용 (passive cite) | [manual.md](manual.md) |
| 7 | ★ | 문서 작성 메타 룰 (SSOT 경로 / 용어 / 어투) | [documentation.md](documentation.md) |
| 8 | ◆ | ROS2 / 임베디드 + 펌웨어 플래시 절차 | [ros2.md](ros2.md) |
| 9 | ◆ | 자산 등록 / 자동화 정책 (auto-activate 금지) | [skill_update.md](skill_update.md) |
| 10 | ★ | CLAUDE.md 작성 가이드 (8 대 원칙 + 템플릿) | [claude_md.md](claude_md.md) |
| — | ◇ | 프로젝트별 비공개 override (gitignore) | [local/](local/) |
| — | — | hook 스크립트 모음 | [hooks/](hooks/) |

## 영역 매트릭스

각 SSOT 가 책임지는 단일 영역. 상호 cross-reference 만 두고 중복 정의 없음.

| 영역 | SSOT |
|------|------|
| 사용자 원문 기록 | [user_instruction_recording.md](user_instruction_recording.md) |
| 작업 전후 체크리스트 | [workflow.md](workflow.md) |
| 코드 수정 범위 / 승인 | [coding.md](coding.md) |
| 우회 / workaround / 임시 코드 | [tech_debt.md](tech_debt.md) |
| 문서·작성 반복 수정 | [iteration_anti_pattern.md](iteration_anti_pattern.md) |
| Git / GitHub / commit / push | [github.md](github.md) |
| 외부 매뉴얼 인용 | [manual.md](manual.md) |
| 문서 메타 룰 / 용어 / 명명 | [documentation.md](documentation.md) |
| ROS2 / 임베디드 / 펌웨어 | [ros2.md](ros2.md) |
| 자산 등록 / 자동화 정책 | [skill_update.md](skill_update.md) |
| CLAUDE.md 작성 | [claude_md.md](claude_md.md) |

## 변경 이력

[CHANGELOG.md](CHANGELOG.md)

## 규칙 변경

본 폴더의 규칙은 단일 근원이므로, 변경이 필요하면 해당 파일을 수정하기 전에 사용자 승인을 받는다.

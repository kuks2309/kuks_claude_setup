# Claude 실수 카테고리 인덱스

`claude-mistake/` 의 사건을 카테고리·메타 패턴별로 색인. 매 세션 시작에 본 파일을 먼저 훑어 동일 카테고리 재발을 차단한다.

<!-- LLM-HINT: SESSION-START-READ -->
## 메타 패턴 (모든 사건의 상위 카테고리)

| 메타 패턴 | 정의 | 차단 트리거 |
|-----------|------|------------|
| **사전 스캔 없이 생성 모드 진입** | 행동 시작 전 (1) 기존 자산 인벤토리 / (2) 관련 SSOT 상호 충돌 / (3) 직전 정정 사항 확인을 생략하고 바로 작성·수정 시작 | 신규 문서·룰·코드 작성 전 `ls SSOT/` + `grep "기존 자료"` + `head INDEX.md` 의무 실행 |
| **SSOT 무비판 채용** | SSOT 텍스트가 모호하거나 다른 SSOT 와 충돌하는데도 그대로 채용 | 새 SSOT 룰 적용 전 동일 영역 SSOT 2개 이상 cross-check |
| **카테고리 학습 미적용 (세션 내)** | 같은 세션에서 한 번 정정한 카테고리 룰을 다음 entry/작업에 적용하지 않음 | 사용자 정정 직후 같은 카테고리의 다른 entry/작업 전 `### 재발 방지` 재독 |

<!-- LLM-HINT: END -->

## 카테고리 × 사건 매트릭스

| 카테고리 | 사건 | 상태 | 반영 자산 |
|---------|------|-----|----------|
| `iteration-loop` | [2026-05-07](2026-05-07.md) ONE_LINERS.md 5회 반복 수정 | closed | [iteration_anti_pattern.md](../claude_guideline/iteration_anti_pattern.md) |
| `pre-search-skip` | [2026-05-07](2026-05-07.md) 동종 자료 검색 누락 | closed | [iteration_anti_pattern.md §1](../claude_guideline/iteration_anti_pattern.md) |
| `ambiguous-word-guess` | [2026-05-07](2026-05-07.md) "한 줄" 단어 추측 | closed | [iteration_anti_pattern.md §2](../claude_guideline/iteration_anti_pattern.md) |
| `ssot-inventory-skip` | [2026-05-11 04:50](2026-05-11.md) SSOT 자산 인벤토리 누락 | closed | [documentation.md v1.8.1](../claude_guideline/documentation.md), [audit.sh `[hint]`](../claude_guideline/audit.sh) |
| `category-misclass` | [2026-05-11 04:50](2026-05-11.md) `request/` 분류 오류 | closed | [audit.sh `[request-misclass]`](../claude_guideline/audit.sh) |
| `ssot-conflict-uncritical` | [2026-05-11 05:10](2026-05-11.md) SOP §3 ↔ documentation.md 충돌 무비판 채용 | closed (v1.8.2) | [user_instruction_handling_sop.md §3/§9](../claude_guideline/user_instruction_handling_sop.md), [CHANGELOG v1.8.2](../claude_guideline/CHANGELOG.md) |
| `category-learning-miss` | [2026-05-11 05:10](2026-05-11.md) 같은 세션 동일 카테고리 재발 | open | (TBD) SessionStart hook + audit.sh order rule |

## 미해결 항목 (open) — closure 의무

| 사건 | 미해결 항목 | 책임 자산 (TBD) |
|-----|------------|----------------|
| 2026-05-11 05:10 | 카테고리 학습 자동 강제 메커니즘 | SessionStart hook 으로 본 INDEX.md top-N 주입 |
| 2026-05-11 05:10 | `user_instructions/*.md` 안 결과 요약 헤딩 검출 룰 | `audit.sh` `[user-instructions-misclass]` 룰 확장 |

## 운용 규칙

- **신규 entry 작성 시**: 본 파일에 카테고리·상태·반영 자산 한 행 추가. open 상태면 "미해결 항목" 표에도 한 행 추가.
- **closure 의무**: open 상태로 7일 이상 방치 금지. closure 시점에 status → closed, 반영 자산 링크 명시.
- **카테고리 신설 기준**: 동일 메타 패턴 2건 이상이면 메타 패턴 표에 한 행 추가.
- **세션 시작 검토**: 작업 영역과 무관하게 본 파일 §메타 패턴 + §미해결 항목 두 절은 매 세션 1회 확인.

## 관련 자산

- [README.md](README.md) — 사건 형식·운용 규칙 (SSOT)
- [../claude_guideline/audit.sh](../claude_guideline/audit.sh) — 자동 검출 룰
- [../claude_guideline/CHANGELOG.md](../claude_guideline/CHANGELOG.md) — 가이드라인 변경 이력

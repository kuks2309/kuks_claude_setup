# Changelog

## 1.14.1 — 2026-08-01

사이클 훅 오탐 수선 — 거부/에러로 끝난 tool 호출을 집계에서 제외. reload 검증 실사격에서 실증.

### 변경

- `claude_guideline/hooks/stop_check_code_record_reflected.py`: PreToolUse 게이트가 **거부한** Write/Edit 도 transcript 에 tool_use 로 남아 "코드 수정"으로 집계되던 오탐 제거 — tool_result `is_error` 를 id 매칭으로 걸러 실제 성공한 수정만 집계.
- `claude_guideline/hooks/pre_tool_use_require_module_docs_read.py`: 대칭 수선 — 거부/에러난 Read 는 내용이 전달되지 않았으므로 읽기 의무 충족으로 인정하지 않음.

### 트리거

reload 적용 확인 실사격(2026-08-01): 읽기 게이트가 Write 를 정상 거부했는데, 같은 턴의 Stop 기록 게이트가 그 **거부된** Write 를 코드 수정으로 집계해 차단 — 파일이 생성된 적 없는 가짜 수정에 이력 entry 를 요구하는 오탐. 합성 5 케이스(오탐 재현 PASS 화·성공 수정 회귀 BLOCK·기록 반영 PASS·거부 Read DENY 유지·성공 Read ALLOW) 검증.

### 호환성

patch bump. 동작 완화는 오탐 경로뿐 — 실제 수정·미독에 대한 강제는 동일.

## 1.14.0 — 2026-08-01

타 PC 작업분(2026-07-31 push, 9bb1555~c137f62 — GitHub 35개 CLAUDE.md 전수 감사 후속 T9-1·T16-1·T13-1·T3-1)의 릴리스 보정. 해당 5 커밋이 VERSION·CHANGELOG 미갱신 상태로 push 되어 다운스트림 update.sh 가 감지하지 못하던 것을 본 entry 로 완결.

### 변경

- `claude_guideline/templates/CLAUDE.md.template`: 구판 5원칙 본문 → claude_md.md §2 "8대 원칙" SSOT 위임 1줄 교체 + 선택 절 4종(독립 프로젝트 선언·보호 자산 목록·도메인 SSOT 표 트리거 열·룰 우선순위 3계층) + 보호 자산 금지 충돌 해제 승인 절차(해제 승인 → 구조 제시 → 승인 후 수정).
- `claude_guideline/documentation.md`: **NEW §경로 이식성** — 절대 경로 금지·프로젝트 루트 기준 상대 경로·외부 경로 `<placeholder>`·`$HOME` 표기, 실측 로그 인용은 원문 유지 예외.
- `claude_guideline/audit.sh`: 루트 CLAUDE.md 내용 검사 블록 — variant 6종 자동 감지(`[lowercase-claude-md]`·`[template-placeholder]`·`[stale-todo]`·`[prechecked-report]`·`[pledge-checklist]`·`[snippet-only-skeleton]`). 픽스처 3종 검증(6건 검출·오탐 0).
- `claude_guideline/claude_md.md`: §6 Variant 차단 표 3행 추가(사전 체크 [X] 보고·다짐 선언형 체크리스트·snippet-only 골격 부재) — audit.sh 룰과 정합.

### 트리거

사용자 지시 (2026-08-01): "리모트에서 다른 pc 에서 개선된 사항을 확인하고 먼저 리스트화 해주세요" → "순서대로 동기화해주세요" — 확인 과정에서 무버전 push 발견, 릴리스 보정 승인.

### 호환성

minor bump. 규칙·검사 추가만 — 다운스트림은 update.sh 로 수신 (templates/ 는 저장소 전용, 설치 대상 아님).

## 1.13.1 — 2026-07-31

사이클 훅 저장소 경계 오판 수선 + `code_updates/` 폴더 스캐폴드 편입 — 1.13.0 배선 직후 워크스페이스 실전 첫 발동에서 발견.

### 변경

- `claude_guideline/hooks/pre_tool_use_require_module_docs_read.py`, `stop_check_code_record_reflected.py`: 상위 탐색이 저장소 경계(`.git`)를 넘어 부모 워크스페이스의 `docs/claude_guideline/` 까지 올라가, 자체 이력 체계(CHANGELOG)를 가진 **중첩 비도입 저장소**를 도입 프로젝트로 오판하던 것을 정정 — `.git` 경계에서 탐색 중단 (같은 레벨에 `docs/claude_guideline/` 이 있으면 도입 우선 판정). 경계 케이스 2종 포함 15 케이스 재검증 통과.
- `claude_guideline/install.sh`, `update.sh`: 표준 폴더 스캐폴드에 `docs/code_updates/` + stub README 추가 — 1.10.0 에서 (옵션) 해제된 의무 폴더가 자동 생성 목록에 빠져 있던 정합 공백 해소.

### 트리거

1.13.0 배선 직후 본 워크스페이스에서 Stop 훅 실전 첫 발동: SSOT 저장소(`kuks_claude_setup`, 루트에 `claude_guideline/` 보유·자체 CHANGELOG 관리) 내부의 install.sh/update.sh 수정을 도입 프로젝트 코드로 오판해 code_updates 기록을 요구. 정탐 구조는 유효했으나 경계 판정 결함 실증.

### 호환성

patch bump. 기존 다운스트림은 update.sh 재실행으로 수신.

## 1.13.0 — 2026-07-31

"수정 전 읽기 → 수정 → 수정 후 기록" 사이클을 매번 기계 강제하는 훅 2종 추가. 문면·체크리스트(1.12.0)만으로는 세션이 빼먹을 수 있던 사이클을 도구 계층에서 차단.

### 변경

- `claude_guideline/hooks/pre_tool_use_require_module_docs_read.py` (신규, PreToolUse Edit|Write|MultiEdit): 코드 수정 시도 순간, 그 모듈의 `architecture/inventory.md`·`code_updates/` 를 이번 세션 transcript 에서 읽은 적 없으면 수정 거부 + 읽기 요구. 인벤토리 부재 모듈은 통과(생성은 Stop 훅 몫). guideline 도입 프로젝트(상위 `docs/claude_guideline/`)에서만 발동, `docs/`·`code_updates/`·`.claude/`·scratchpad·비코드 파일 제외.
- `claude_guideline/hooks/stop_check_code_record_reflected.py` (신규, Stop): 매 응답 종료 시(세션 종료 아님) 이번 턴의 코드 수정이 `code_updates/`·`inventory.md` 반영 없이 끝나려 하면 1회 차단(`stop_hook_active` 가드) + 기록 반영 요구.
- `claude_guideline/hooks/README.md`: §제공 hook 표 2행 + §설치(사이클 훅 2종) 절.
- `claude_guideline/install.sh`, `update.sh`: `HOOK_FILES` + chmod 대상에 2종 추가.
- 검증: 합성 transcript 11 케이스 (PreToolUse 5 — 미독 거부/읽은 후 허용/비도입 허용/인벤토리 부재 허용/기록 파일 허용, Stop 6 — 미기록 차단/code_updates 반영 통과/인벤토리 반영 통과/루프 가드/전 턴 무관/비도입) 전부 통과.

### 트리거

사용자 지시 (2026-07-31):

> "코딩중에 기존 기록을 읽어야 합니다. 그리고 코딩후에 수정 내용 반영"
> "매번 하지 않으면 코드 엉망이 되어서 만든 것인데 코드 수정전 읽고 수정후 기록 이것이 되풀이되어야 코드의 품질이 좋아짐"

근본 원인: 1.12.0 까지 사이클은 규칙 문면 + 자기 점검 체크리스트 층만 존재 — 세션이 빼먹어도 물리적 차단 없음 (약어→1.8.7 Stop 훅, 주석 오염→1.11.0 PostToolUse 훅과 동형의 강제층 공백).

### 호환성

minor bump. 다운스트림은 update.sh 수신 후 `.claude/settings.json` 에 PreToolUse·Stop 등록 필요 (hooks/README §설치 참조). 미등록 시 규칙·체크리스트 층은 기존대로 동작.

## 1.12.0 — 2026-07-31

인벤토리 운용 기본값 전환 — "없으면 생성하지 않음(별도 승인)" 을 "없으면 수정 파일 범위만큼 즉시 생성(증분)" 으로 뒤집고, 코드 수정 전 모듈 문서(인벤토리·code_updates) 읽기를 의무화.

### 변경

- `claude_guideline/coding.md` §함수·전역 변수 인벤토리 갱신:
  - **수정 전 읽기 의무**: 코드 수정 전 해당 모듈 `architecture/inventory.md` + `code_updates/` 최근 entry 를 먼저 읽는다.
  - **없으면 생성이 기본값**: 인벤토리 부재 시 이번 작업 단위에서 수정 대상 파일 범위만큼 생성 (구판 "최초 생성은 별도 승인" 폐기 — 모듈·저장소 전체 일괄 소급만 별도 승인).
  - 미등재 파일은 내부 로직만 수정해도 행 추가.
- `claude_guideline/workflow.md`: 작업 시작 전 체크에 "수정 대상 모듈 인벤토리·code_updates 읽기 (없으면 생성)" 항목 추가 (7 → 8 항목).
- `claude_guideline/documentation.md` §인벤토리 문서: **증분 작성** 규정(수정이 닿는 파일부터 등재), 템플릿에 §커버 파일(진행도 목록) 추가, 확장 표 옵션(상수 표·ROS2 인터페이스 표) 명시.

### 트리거

사용자 지적 (2026-07-31):

> "현재는 코드 수정을 하게 되면 수정할 파일의 문서를 읽어야 하는데 문서 생성이 안되는경우가 많음. 문서에는 변수 리스트 테이블, 함수 리스트 테이블 등등에 대한 코드 정보가 포함되어야 하는데 없는것 같음"

근본 원인: 1.11.0 이 과잉 범위 방지를 위해 인벤토리 최초 생성을 opt-in(별도 승인)으로 규정 → 문서가 없는 모듈은 영구히 없는 채로 유지. 수정 전 문서 읽기 절차도 미명문화.

### 호환성

minor bump. 다운스트림은 update.sh 로 수신. 기존 인벤토리 없는 모듈은 다음 코드 수정 시점부터 파일 단위로 채워지기 시작.

## 1.11.1 — 2026-07-31

update.sh 비원자성 결함 수선 — 1.11.0 병합 직후 워크스페이스 실배포 검증에서 발견.

### 변경

- `claude_guideline/update.sh`:
  - **자기 갱신 원자화**: update.sh 를 FILES 루프의 `curl -o` 직접 덮어쓰기에서 분리 — 실행 중인 스크립트의 inode 를 truncate 하여 중단(line offset 붕괴로 syntax error)을 유발하던 것을 `.new` 다운로드 후 `mv` 교체로 변경 (구 inode 는 실행 중 프로세스가 유지).
  - **VERSION 기록을 맨 끝으로 이동**: 설치 도중 VERSION 이 먼저 갱신되면 중단된 설치가 "이미 최신"으로 위장되어 재실행이 no-op — 모든 파일 설치 성공 후 `$UPSTREAM_VERSION` 을 마지막에 기록.
  - VERSION·update.sh 백업은 명시 목록으로 유지.

### 트리거

워크스페이스 1.10.0 → 1.11.0 실전 업데이트 중 실증: update.sh 가 자기 자신을 덮어쓰다 syntax error 로 중단, VERSION 은 이미 1.11.0 기록 → 재실행 "[OK] 이미 최신" no-op, `git_workflow.md` 등 후속 파일 누락 방치.

### 호환성

patch bump. 구판(≤1.11.0) update.sh 로 1.11.1 을 받는 첫 실행은 여전히 구판 코드로 동작하므로, 실패 시 1 회 재실행 (VERSION 이 조기 기록된 경우 VERSION 삭제 후 재실행).

## 1.11.0 — 2026-07-29

아래 1.10.0 수정 이력 규칙의 SIL(Software-In-the-Loop) 테스트(3 라운드, G12~G17)에서 발견된 결함 6 건 수선 + 주석 규율·인벤토리 갱신 의무 신설 + 주석 changelog 기계 강제층(PostToolUse 훅) 도입.

### 변경

- `claude_guideline/coding.md`:
  - G12: 낡은 주석 삭제·교정 범위를 "이번 수정이 닿는 선언·함수"로 한정, 범위 밖 오염 주석은 발견 보고 → 승인 시 별도 정리.
  - G16: 프로젝트 컨벤션이 명시 요구하는 관례 블록(Doxygen `@version` 등) 예외.
  - **NEW §주석 규율** — 담을 것(물리 제약·수치 근거·의도·외부 제약)/함수 헤더 역할 1 줄/담지 말 것(자명한 what·이력·리뷰어 말 걸기).
  - **NEW §함수·전역 변수 인벤토리 갱신** — 함수/전역 변수의 추가·삭제·시그니처 변경 시 같은 작업 단위에서 인벤토리 표 갱신 (내부 로직만 변경 시 불요, 최초 생성은 별도 승인 작업).
- `claude_guideline/documentation.md`:
  - G13: entry 커밋 항목 자기참조 해소 — 같은 커밋이면 커밋 제목, 분리 커밋이면 코드 커밋 hash.
  - G14: `code_updates/` 최초 생성 시 README.md 동반 생성.
  - G15: 파일명 `<주제>` 영문 소문자·언더바 명시.
  - **NEW §인벤토리 문서** — `architecture/inventory.md` 위치·형식(목적/함수 표/전역 변수 표), 현재 상태 전용(이력 금지). `architecture/` 표 행에 병기.
- `claude_guideline/workflow.md`: 종료 체크에 인벤토리 갱신 항목 추가 (10 → 11 항목).
- `claude_guideline/hooks/post_tool_use_check_history_comments.py` (신규, G17): Edit/Write/MultiEdit 로 코드 파일에 추가되는 주석의 이력 패턴(날짜·버전 태그·값 변천 화살표·"기존/이전" 서술어) 검출 시 `{"decision":"block"}` — `code_updates/` 기록으로 유도. `TODO(YYYY-MM-DD)`·NOLINT·noqa·비코드 파일 화이트리스트. 합성 7 케이스 검증 통과.
- `claude_guideline/hooks/README.md`: §제공 hook 표 + §설치(PostToolUse 훅) 절 추가.
- `claude_guideline/install.sh`, `update.sh`: `HOOK_FILES` + chmod 대상에 신규 훅 추가.

### 트리거

사용자 지시 (2026-07-28~29):

> "SIL 테스트 해봅시다. 주석 오염에 대한 방지는?"
> "권장 안으로 하고 설치해서 재 검증해주세요"
> "특히 주석 부분 강화하고 코드 수정시마다 함수, 변수 테이블을 업데이트 해야 하는데.."

SIL 산출물: 워크스페이스 `kuks_claude_setup_new/dogfooding/code_updates/` (로컬 전용) — TC1 오염 파일 버그 수정 회고, TC3 적대적 주석 경계 판정 6 케이스, TC4 방지 실효층 분석.

### 호환성

minor bump. **재번호 주의**: 본 항목과 아래 1.10.0 은 `feat/code-review-sop` 에서 각각 1.10.0 / 1.9.0 으로 발행되었으나, master 가 같은 기간 별도의 1.9.0(git_workflow, 2026-07-05)을 발행하여 병합 시 번호가 충돌 → 브랜치 두 항목을 한 단계씩 재번호. 브랜치 계보 설치본(VERSION 1.9.0/1.10.0)은 `update.sh` 재실행으로 1.11.0 동기.

## 1.10.0 — 2026-07-28

(`feat/code-review-sop` 에서 1.9.0 으로 발행 → 병합 시 재번호 — 위 1.11.0 §호환성)

코드 수정 이력의 기록처를 `code_updates/` 로 일원화하고, 코드 주석에 changelog 성 이력을 남기는 것을 금지. 위치 룰(1.8.0)만 있고 코드 작업 절차와 연결되지 않아 수정 이력이 코드 주석에 누적되며 낡은 서술로 오염되던 공백을 수선.

### 변경

- `claude_guideline/coding.md`: **NEW §수정 이력 기록 (code_updates/)** — 코드 수정 완료 시 `code_updates/` 기록 의무, 주석에 changelog 성 이력(날짜·버전·이전 값) 작성 금지, 주석은 현재 코드의 사실만 기술하고 낡은 주석은 삭제·교정, silent bug 가설 이력의 배출구도 동일.
- `claude_guideline/workflow.md`: 작업 종료 전 체크리스트에 `code_updates/` 기록·주석 changelog 금지 점검 항목 추가 (9 → 10 항목).
- `claude_guideline/manual.md`: §추정 금지·실측 검증 의 silent bug 가설 이력 보존처를 "코드 또는 모듈 CLAUDE.md" → "해당 코드의 `code_updates/`" 로 정정 (주석 이력 허가증으로 과잉 일반화되던 문구 제거).
- `claude_guideline/documentation.md`: **NEW §code_updates 기록 형식** — 날짜별 `YYYY-MM-DD_<주제>.md` (변경 빈도 낮으면 단일 로그 역순 누적, 폴더당 한 방식), 최신 위, 필수 4 항목(대상/변경/사유/커밋). `code_updates/` 표 행의 (옵션) 표기 해제 + 의무·형식 링크.
- `claude_guideline/README.md`: coding.md 행 설명에 "수정 이력 기록" 추가.

### 트리거

사용자 지시 (2026-07-28):

> "해당 코드가 있는 폴더에 docs 폴더에 수정 이력을 병기하라고 지침을 요청했는데 왜 이렇게 해서 오염된 정보로 코드를 이상하게 만드는지"

근본 원인: 1.8.0 이 `code_updates/` 를 문서 배치 계층(documentation.md + audit.sh)에만 성문화하고, 코드 작업 절차 계층(coding.md·workflow.md)에 기록 의무·주석 금지를 연결하지 않음. manual.md 의 "코드 … 에 보존" 문구가 주석 이력을 정당화하는 방향으로 작용.

## 1.9.0 — 2026-07-05

Git 커밋·푸시 워크플로 규칙 `git_workflow.md` 를 진입점에 신규 추가 (멀티 세션 커밋 안전 심화). `kuks_claude_skill_setup` 의 `git_workflow` 번들(v1.4.0)을 SSOT 규칙본으로 반영.

### 변경

- `claude_guideline/git_workflow.md` **신규**: solo/team 모드 판정(README 기록 우선·미선언 시 문의·기록), 세션 격리 staging(멀티 세션이 working tree 공유 시 이번 세션 파일만), 세션 격리 훅(track/reminder/stage-gate — 타 세션 미커밋 파일 캡처 하드 차단), 다중 원격 미러, GitHub 정책 강제(선택). 훅은 규칙이 아닌 실행 도구라 SSOT 는 규칙만 배포하고 훅은 `git_workflow` 번들 install.sh 로 다운스트림 설치.
- `claude_guideline/README.md` §진입점: `git_workflow.md` 행(3+, ★) 추가.
- `claude_guideline/install.sh` FILES[]: `git_workflow.md` 배포 대상 추가.

### 트리거

사용자 요청 (2026-07-05): "kuks_claude_skill_setup 의 (git_workflow) 수정 내용은 반영되어야지" — 번들에서 완성한 git_workflow v1.4.0 을 SSOT 저장소 가이드라인으로 반영. 배경: VSCode 한 창의 다중 Claude 탭이 단일 working tree 를 공유해 한 세션의 `git add` 가 타 세션 미커밋 파일을 캡처하는 레이스 실증 → 세션 격리 규칙·훅 정립.

### 미결 (다음)

- 기존 `github.md`(커밋/푸쉬/PR)와 `git_workflow.md` 의 **역할분담·정합** (중복 정리).
- 세션 격리 훅(Python + settings.json 등록)을 본 SSOT 의 hooks 배포 모델(shell + curl)에 맞춰 통합할지 결정.

### 호환성

minor bump (1.8.7 → 1.9.0). 규칙 추가만 — 기존 가이드라인·구조 변경 없음. 다운스트림은 `update.sh` 로 `git_workflow.md` 보충.

## 1.8.7 — 2026-06-03

`hooks/` 에 Stop 훅 `stop_check_abbreviations.py` 추가. 응답에 풀어쓰지 않은 약어가 있으면 정지를 차단하고 "원어(한국어 의미, 약어)" 형태로 풀어쓰도록 강제 — 약어 남용 재발 차단. SessionStart 전용이던 hooks 폴더가 Stop 이벤트(.py)까지 확장됨.

### 변경

- `claude_guideline/hooks/stop_check_abbreviations.py` (신규): stdin 의 `transcript_path` 로 마지막 assistant 메시지를 읽어 `ABBREVIATIONS` 배열의 `(정규식, 풀어쓴 키워드)` 쌍을 검사. 약어가 풀어쓰기 없이 단독 사용되면 `{"decision":"block","reason":...}` 출력. `stop_hook_active` 가드로 무한 루프 방지. 추적 약어는 스크립트 상단 배열에서 편집.
- `claude_guideline/hooks/README.md`: §제공 hook 표에 행 추가 + §설치(Stop 훅) 절 + python 자가 검증 예시 추가. §신규 hook 추가 시 형식을 `<event>_<purpose>.{sh,py}` 로 확장.
- `claude_guideline/install.sh`, `update.sh`: `HOOK_FILES` 배열 + chmod 대상에 `stop_check_abbreviations.py` 추가.

### 트리거

사용자 지시 (2026-06-03):

> "응답 검사 훅을 만들어주세요." (약어를 계속 사용하는 문제 재발 방지)
> "방금 만든 hook을 upload 할 것" (feat/code-review-sop 브랜치)

근본 원인: 약어 사용 금지 지시에도 습관적으로 약어를 풀어쓰지 않고 사용. 강제 메커니즘(Stop 훅) 부재. China 워크스페이스에서 검증 후 SSOT 에 승격.

## 1.8.6 — 2026-05-11

docs/ 표준 폴더 전체를 install/update 자동 생성 대상으로 확장 + "빈 폴더 금지" 정책 폐기. 이전까지 v1.8.5 의 SOP 의존 3개 폴더만 자동 생성되었으나, SOP 가 의존하지 않는 일반 카테고리 폴더 (architecture / usage / issues_and_fixes / assets / code_review / refactoring / analysis / test / troubleshooting / api) 도 신규 프로젝트에서 사용자가 수동 mkdir 해야 했던 마찰 해소.

### 변경

- `claude_guideline/documentation.md` §docs/ 표준 폴더:
  - **수정**: "처음 생성 시에는 `docs/README.md` 하나만 두고 … 활동 발생 시 추가 (빈 폴더 금지)" 정책 폐기. install/update 가 모든 표준 폴더를 자동 생성하며, 활동 미발생 폴더는 README 만 남고 비어 있어도 정상.
- `claude_guideline/audit.sh`:
  - §7 `[empty]` 룰을 `[no-readme]` 로 정정. 빈 폴더 자체는 OK, README.md 부재만 정보성 권고. `N_ISSUE+=1` 카운트도 제거 (강제 X).
- `claude_guideline/install.sh`, `update.sh`:
  - 자동 생성 폴더 4종 → 13종 확장: architecture, usage, issues_and_fixes, assets, user_instructions, worklog, claude-mistake, code_review, refactoring, analysis, test, troubleshooting, api.
  - 각 폴더에 역할·SSOT 링크를 담은 stub README 자동 배치 (`write_stub` 헬퍼 함수). claude-mistake/README.md 만 SSOT 원격 다운로드.
  - 기존 README 가 있으면 덮어쓰지 않음 (모든 stub 작성에 `if [ -f ... ]` 가드).

### 트리거

사용자 지적 (2026-05-11):

> "폴더 /home/amap/Project/claude_code/docs 에 있는 폴더는 다 설치하게 만들어야 하지 않을까요?"
> "'처음 생성 시에는 docs/README.md 하나만 두고, 아래 폴더는 해당 활동이 실제로 발생하면 그 시점에 추가한다(빈 폴더 금지).' ← 수정해야 합니다. 잘못 만들어진 정책임"

근본 원인: v1.8.5 가 SOP 의존 3개 폴더만 자동화하고 나머지 표준 폴더는 기존 정책("활동 발생 시 추가") 을 따랐으나, 신규 프로젝트가 SSOT 표준 구조를 한 번에 받지 못해 사용자가 폴더마다 수동 mkdir 해야 하는 마찰 누적. 정책 자체가 install 자동화와 충돌.

### 호환성

patch bump (1.8.5 → 1.8.6). 기존 다운스트림은 `bash docs/claude_guideline/update.sh` 실행 시 누락 폴더 자동 보충. 기존 README 는 보존. audit.sh 의 `[empty]` 경고를 받던 다운스트림은 본 룰 정정으로 경고 사라짐.

## 1.8.5 — 2026-05-11

SOP 가 의존하는 표준 폴더(`docs/claude-mistake/`, `docs/user_instructions/`, `docs/worklog/`)를 install/update 가 자동 생성하도록 정정. 이전까지는 `claude_guideline/` 만 자동 설치되고 나머지 3개 폴더는 사용자가 수동 mkdir 해야 했음 — SOP 흐름에 폴더 부재 시 어떻게 만드는지 절차 누락.

### 변경

- `claude_guideline/install.sh`:
  - **NEW**: `mkdir -p docs/claude-mistake docs/user_instructions docs/worklog` 자동 실행.
  - **NEW**: 각 폴더에 README.md 생성 — claude-mistake 는 SSOT 원격에서 다운로드, user_instructions / worklog 는 install.sh heredoc 으로 stub 생성 (역할·형식·SSOT 링크 명시).
  - 기존 파일이 있으면 덮어쓰지 않음 (`if [ ! -f ... ]` 가드).
- `claude_guideline/update.sh`:
  - 동일 mkdir + README 보강 — 기존 다운스트림이 update.sh 실행 시 누락된 폴더 자동 보충.
  - 기존 README 는 덮어쓰지 않음.

### 트리거

사용자 지적 (2026-05-11):

> "현재 mistake 부분에서 프로젝트 처음 설치할때 폴더를 만들게 되어 있나요?"
> "폴더 /home/amap/Project/claude_code/docs/user_instructions 도 처음 프로젝트에 적용할때 폴더 설치하라는 지시가 없는것 같은데요."

근본 원인: v1.8.2 / v1.8.3 의 SOP 정정이 `worklog/` 책임을 새로 부여하고 `user_instructions.md` 기록 절차를 강화했으나, install.sh 가 `claude_guideline/` 만 다루도록 설계되어 신규 프로젝트가 SOP 를 따르려면 사용자가 별도로 폴더를 만들어야 하는 마찰 존재. SOP 가 의존하는 모든 폴더는 install 단계에서 자동 보장되어야 함.

### 호환성

patch bump (1.8.4 → 1.8.5). 기존 다운스트림은 `bash docs/claude_guideline/update.sh` 실행 시 누락된 폴더 자동 보충. 이미 폴더와 README 가 있다면 그대로 유지.

## 1.8.4 — 2026-05-11

`kuks_claude_setup/claude-mistake/` 책임 경계 정정 — v1.8.2 / v1.8.3 에서 SSOT 본판에 잘못 push 한 사건 entry 제거 + README 명시화.

### 변경

- `claude-mistake/2026-05-07.md` 제거 (`git rm`) — 본 파일은 본 SSOT 폴더가 아닌 사건 발생 프로젝트의 `docs/claude-mistake/` 에 있어야 함.
- `claude-mistake/2026-05-11.md` 제거 (`git rm`) — 본 워크스페이스 (claude_code) 사건이므로 `claude_code/docs/claude-mistake/2026-05-11.md` (이미 존재) 가 정상 위치.
- `claude-mistake/INDEX.md` 제거 (`git rm`) — 카테고리 인덱스 운용은 다운스트림 책임. 본 SSOT 에는 형식 정의만.
- `claude-mistake/README.md`:
  - **NEW §책임 경계** — 본 SSOT 폴더에는 README 만, 사건 entry / INDEX 는 다운스트림 `docs/claude-mistake/` 에만 작성. 본 SSOT 에 사건을 두면 다른 프로젝트에 무관한 사건이 노출되는 책임 경계 침범.
  - §Closure 규칙 / §검토 시점: INDEX.md 참조를 다운스트림 `docs/claude-mistake/INDEX.md` 로 명시.
  - §설치 방법 마지막 줄에 "SSOT 에는 본 README 만" 강조.

### 트리거

사용자 지적 (2026-05-11 06:10 KST):

> "일반화 폴더에 이 프로젝트의 내용을 기록하는 특별한 이유가 있는지?"
> "폴더 /home/amap/Project/claude_code/kuks_claude_setup/claude-mistake 가 일반화 폴더라고 1000번 더 이야기 할까"

근본 원인: v1.8.2 / v1.8.3 patch 시 본 워크스페이스 사건을 SSOT 본판에 commit (`1c34741`, `be47c6c`). 또한 v1.8.2 이전부터 있던 `2026-05-07.md` (`73fc92b`) 도 같은 책임 경계 위반인데 정정 누락. README 가 묵시적으로만 다운스트림 위치를 가리켰을 뿐 명시적이지 않아, 운영자(Claude/이전 작업자) 가 SSOT 에 사건을 push 하는 패턴이 반복됨.

### 호환성

patch bump (1.8.3 → 1.8.4). 다운스트림 영향:
- 다운스트림이 SSOT 의 `claude-mistake/2026-05-*.md` 를 참조하지 않았다면 영향 없음.
- 참조했다면 자체 `docs/claude-mistake/` 의 사건 기록을 사용하도록 수정 필요 (애초에 다른 프로젝트의 사건이라 참조해서는 안 되는 데이터).

## 1.8.3 — 2026-05-11

`claude-mistake/` 학습 closure 인프라 신설 — INDEX.md 카테고리 색인 + closure 규칙 + SessionStart hook + audit.sh 검출 룰. 1.8.2 의 SOP 정정이 다운스트림 패턴을 차단했다면 본 1.8.3 은 같은 세션 내 재발 차단을 시스템화.

### 변경

- `claude-mistake/INDEX.md`: NEW
  - §메타 패턴 (사전 스캔 없이 생성 모드 진입 / SSOT 무비판 채용 / 카테고리 학습 미적용)
  - §카테고리 × 사건 매트릭스 (현재 7 카테고리, 3 entry)
  - §미해결 항목 (open) 추적 표
  - §운용 규칙 (신규 entry / closure / 카테고리 신설 / 세션 시작 검토)
  - LLM-HINT 주석 마커 — SessionStart 시 자동 주입 대상 영역 표시
- `claude-mistake/README.md`:
  - **NEW §Closure 규칙** — 반영 자산 1개 이상 / TBD 금지 / 카테고리 부착 / owner 명시
  - §기존 실수 검토 시점: SessionStart hook (자동) + 작업 시작 전 (수동) + 사용자 정정 직후 3 시점으로 확장
- `claude-mistake/2026-05-07.md`, `2026-05-11.md`: 헤더에 카테고리 뱃지 + 상태 + INDEX 링크 추가 (`> **카테고리**: ... · **상태**: closed (vN.N.N)`).
- `claude_guideline/audit.sh`:
  - **NEW [user-instructions-headings]**: `docs/user_instructions/*.md` 안 `### 처리|### 결론|### 산출물` 헤딩 검출 (v1.8.2 SOP 정정의 audit 강제).
  - **NEW [legacy-request]**: legacy `docs/request/` 폴더 검출 시 `user_instructions/` 로 rename 권고.
  - **NEW [mistake-order]**: `docs/claude-mistake/YYYY-MM-DD.md` 안 `## ... HH:MM` 헤딩이 시간 역순 (최신 위) 위반 시 검출.
  - **NEW [mistake-tbd]**: `docs/claude-mistake/*.md` 안 TBD/후보/추후/미정 키워드 검출 (closure 의무 환기).
  - **NEW [hint]** `docs/claude-mistake/INDEX.md` 부재 권고.
- `claude_guideline/hooks/`: NEW
  - `session_start_claude_mistake.sh`: SessionStart 훅 — `claude-mistake/INDEX.md` §메타 패턴 + §미해결 항목 자동 주입.
  - `README.md`: hook 등록 가이드 (`~/.claude/settings.json` 또는 `<project>/.claude/settings.json`).
- `claude_guideline/install.sh`, `update.sh`: hooks/ 디렉토리 생성 + 다운로드 + chmod 추가. FILES 배열에 `claude_md.md` (CLAUDE.md 작성 가이드 SSOT, 172줄) 등록.
- `claude_guideline/claude_md.md`: SSOT 자산 정식 등록 (이전 untracked 상태에서 install/update 대상으로 승격).

### 트리거

10명 sub-agent + Codex/Gemini 검토에서 도출된 closure 결함:
- "권고 없이 자동 주입 메커니즘 부재" (Methodology, Analyst, UX, Architect 4개 합의)
- "카테고리/인덱스 부재로 100건 누적 시 grep 의존" (Analyst, UX, Architect 3개 합의)
- 근본 원인 (A) "트리거 부재" 가설 채택 (Codex, Gemini, Tracer 모두 합의)

본 1.8.3 은 (A) 트리거 부재 가설에 대한 직접 처방: SessionStart hook 으로 INDEX top-N 자동 주입 + audit.sh 로 closure 의무 자동 검출.

### 호환성

patch bump (1.8.2 → 1.8.3). 기존 다운스트림은 `bash docs/claude_guideline/update.sh` 로 hooks/ 폴더 + audit.sh 갱신본 자동 다운로드. SessionStart hook 활성화는 사용자가 `~/.claude/settings.json` 에 entry 1줄 추가 (수동).

## 1.8.2 — 2026-05-11

`user_instruction_handling_sop.md` ↔ `documentation.md` 충돌 정정 — 1.8.1 의 `docs/user_instructions/` 정의 강화("사용자 지시사항 전용") 가 SOP §3 의 형식(`### 처리` / `### 결론·산출물`)과 충돌하여, 다운스트림에서 결과 요약이 `docs/user_instructions/` 에 누적되는 패턴을 양산. 본 패치는 SOP 측 형식 정정으로 충돌 해소.

### 변경

- `claude_guideline/user_instruction_handling_sop.md`:
  - **§3 (Step 2)**: `docs/user_instructions/user_instructions.md` 기록 형식에서 `### 처리` / `### 결론 / 산출물` 섹션 제거. 사용자 원문 인용만 남김.
  - **§9 (Step 8)**: 결과·산출물 기록 책임을 `docs/worklog/` (또는 `code_review/` / `analysis/` / `refactoring/` / `troubleshooting/`) 로 이동. user_instructions.md 와 worklog entry 는 시각·제목으로 매핑.
  - **§1 흐름도**: Step 8 라벨을 "user_instructions.md 결론 갱신" → "worklog 결과 기록" 으로 갱신.
  - 신규 ✓ 체크: `grep -E "^### (처리|결론|산출물)" docs/user_instructions/user_instructions.md` → 출력 없어야 함.

### 트리거

`claude-mistake/2026-05-11.md` 05:10 entry — Claude 가 같은 세션 안에서 동일 카테고리 ("결과 요약을 `user_instructions/` 에 넣음") 를 두 번째로 재현. 첫 번째는 `ccg-review-2026-05-10.md` 위치 오류, 두 번째는 `user_instructions.md` 안 `### 처리` / `### 결론` 섹션 작성.

10명 sub-agent 검토 + Codex/Gemini 외부 검토에서 "1.8.1 의 `user_instructions/` 정의와 SOP §3 형식이 충돌" 로 확정.

### 호환성

patch bump (1.8.1 → 1.8.2). 기존 `user_instructions.md` 에 이미 작성된 `### 처리` / `### 결론` 섹션은 본 패치로 자동 제거되지 않음 — `audit.sh` 의 차기 룰(P1)이 검출 후 사용자가 worklog 로 이전.

## 1.8.1 — 2026-05-11

1.8.0 누락 수정 — `claude-mistake/` (SSOT 자산) canonical 등록 + `docs/user_instructions/` 정의 명확화.

### 변경

- `claude_guideline/documentation.md`:
  - **NEW**: 폴더 명명 규칙에 **SSOT 배포 자산 예외** 추가. `claude_guideline/` (언더바), `claude-mistake/` (하이픈), `superpowers/` 는 SSOT 표기를 그대로 유지(언더바-only 룰의 예외).
  - **NEW**: docs/ 필수 폴더 표에 `claude-mistake/` 추가. 형식 / 목적(Claude 실수 재발 방지) 명시.
  - **수정**: `user_instructions/` 정의 명확화 — "**사용자가 터미널에 입력한 지시사항의 시간 누적 기록**"(`user_instruction_handling_sop.md` §3 형식). 결과 요약·리뷰·분석은 여기 금지.
  - Variant 매핑 표에 `mistake/`, `claude_mistake/`, `claude_mistakes/` → `claude-mistake/` 추가.
  - Variant 매핑 표에 `user_instructions/` 안 `*review*`/`*report*`/`*summary*`/`*analysis*` 파일 → `code_review/` 또는 `analysis/` 이전 권고 추가.
- `claude_guideline/audit.sh`:
  - `FOLDER_VARIANTS` 에 mistake 류 3 종 추가.
  - **NEW [request-misclass]** 검출: `docs/user_instructions/` 안 비-요청 파일(review/report/summary/analysis 키워드 매칭) 자동 권고.
  - **NEW [hint]** `docs/claude-mistake/` 부재 시 정보성 권고 (강제 X — 활동 발생 시 생성 권장).

### 트리거

사용자 지적:

> "`docs/request` 는 사용자의 지시사항을 기록하는 것입니다. 사용자가 터미널에 입력하는 지시사항을 정리해서 기록하는 것입니다. … 현재 `ccg-review-2026-05-10.md` 는 결과 요약을 했는데 결과 요약의 목적이 아닙니다."

> "제일 중요한 `claude_mistake` 가 빠졌네요. 이 부분은 매우 중요합니다. 지적사항에 대해서 claude 의 실수를 기록해서 반복 실수를 하지 않도록 하는 것이 목적입니다."

근본 원인:

1. 1.8.0 의 canonical 트리가 `claude_guideline/` 만 인식하고 `claude-mistake/` 등 SSOT 의 다른 자산을 누락. 즉 SSOT 의 책임 분리 분석이 불완전.
2. `documentation.md` 의 매핑 표가 `user_instructions/` 를 "요구사항 · 요청 사항"으로 모호하게 정의해, 결과물 분류 폴더로 오인되기 쉬웠음. SSOT 결함.

본 1.8.1 은 두 결함을 직접 정정. **이 사건 자체는 `claude-mistake/2026-05-11.md` 항목으로 별도 기록 권장** (Claude 가 SSOT 자산 인벤토리를 사전 점검하지 않은 실수).

## 1.8.0 — 2026-05-11

`documentation.md` 에 docs/ canonical 구조 정의 + `audit.sh` 신규 도입. 46 개 docs/ 폴더 일괄 감사 결과를 SSOT 룰로 코드화.

### 변경

- `claude_guideline/documentation.md`:
  - **NEW §폴더 명명 규칙(Canonical)**: 폴더는 언더바 `_` 만 허용, 하이픈/공백/한글 폴더명 금지. 단·복수 일관 룰.
  - **NEW §표준 레이아웃(Canonical Tree)**: repo-root 직속(`manual/`, `api/`) vs `docs/` 책임 분리. `docs/` 필수·옵션 폴더 표.
  - **NEW §ROS2 워크스페이스 특칙**: 패키지별 `src/<pkg>/docs/code_updates/` 가 디폴트, 워크스페이스 `docs/code_updates/` 는 횡단 변경 한정.
  - **NEW §Variant → Canonical 매핑**: `code-review`/`code_reivew` → `code_review`, `issues-fixes`/`issues_fixes` → `issues_and_fixes`, `sw_structure`/`sw-architecture` → `architecture`, `stratedgy` → `strategy` 등 audit.sh 자동 적용 대상.
  - **NEW §변종 차단 룰**: audit.sh 가 검사하는 항목 6 종 명시.
- `claude_guideline/audit.sh`: NEW
  - `bash audit.sh [path...]` 또는 `--batch <file>` 로 일괄 점검.
  - dry-run 전용(파일 이동 없음). variant 폴더 / 단일파일→폴더 승격 / 평탄 .md / 외부 PDF / 한글·공백 폴더명 / 오탈자 / 빈 폴더 / ROS2 패키지 docs 누락 / repo root 필수 파일 누락 검출.
  - exit 0 항상(audit-only).
- `claude_guideline/install.sh`:
  - FILES 배열에 `manual.md`, `ros2.md`, `tech_debt.md`, `iteration_anti_pattern.md`, `skill_update.md`, `user_instruction_handling_sop.md`, `audit.sh` 추가(기존 누락 해소).
  - 설치 후 안내에 `audit.sh` 사용법 추가.
- `claude_guideline/update.sh`:
  - FILES 배열 단일화(install.sh 와 동일). manual.md/ros2.md/iteration_anti_pattern.md/skill_update.md/user_instruction_handling_sop.md/audit.sh 백업 + 다운로드 포함.

### 트리거

`/team 20` 으로 이 컴퓨터의 46 개 docs/ 폴더(직속 하위에 docs/ 가 있는 모든 사용자 프로젝트) 일괄 감사 결과:

- 공통 폴더명 변종 다수(`code-review`/`code_reivew`/`issues-fixes`/`issues_fixes`/`sw-architecture`/`stratedgy`)
- 평탄 `*_code_updates.md` 20+ 개(T-Robot_nav_ros2_ws)
- docs/ 안 외부 벤더 PDF(TM_Robot/Hailo/parking_robot) — root `manual/` 분리 필요
- 한글 폴더명·공백 포함 폴더명(`GLIM-slam only/`, `학습_및_DFC_가이드` 류)
- ROS2 패키지에 docs/ 누락 다수

세부 감사 결과: `Project/claude_code/docs/projects_analysis/README.md` 및 개별 46 보고서.

### 호환성

minor bump (1.7.0 → 1.8.0). 기존 설치 repo 는 `bash docs/claude_guideline/update.sh` 로 새 파일(`audit.sh`, `manual.md` 등) 다운로드 가능. 기존 폴더 구조 강제 마이그레이션 없음(`audit.sh` 는 dry-run 권고만).

## 1.7.0 — 2026-05-09

`user_instruction_handling_sop.md` 신규 — 사용자 지시사항 처리 9 단계 SOP 도입.

### 변경

- `claude_guideline/user_instruction_handling_sop.md`: NEW
  - 9 단계 (지시 명확화 → requirements 기록 → 기존 자료 검색 → SSOT 룰 식별 → 사전 승인 → 실행 → 검증 → 결론 갱신 → 결과 보고)
  - 각 단계 ✓ 체크 강제 (skip 시 거짓 단정 / 중복 작업 / 미승인 변경 위험)
  - SOP 위반 시 영향 사례 (Step 2/3/4/5/7 skip 패턴, 익명화)
  - Step 5 사전 승인 트리거 표 = 신 `github.md` ("기록" 4단계 자동) 와 정합 (외부 SSOT 는 push 직전 사용자 명시 확인)
- `claude_guideline/README.md`: SOP 진입 항목 ★★ (표 최상단) 추가

### 트리거

임베디드 분석 세션에서 발견된 5 패턴:
- requirements 기록 skip → 추후 이력 추적 불가
- 기존 자료 검색 skip → 외부 spec 이 `manual/` 에 있는데 다시 다운로드 시도
- 적용 룰 식별 skip → 거짓 단정 발생 (manual.md v1.6.0 트리거 사례 재현)
- 사전 승인 판단 skip → 코드 / 큰 변경 미승인 진행
- 검증 skip → 일괄 정정 (`replace_all`) 후 verbose 결과

본 SOP 는 위 5 패턴 모두 차단. `manual.md` / `iteration_anti_pattern.md` / `github.md` 와 결합 적용.

## 1.6.2 — 2026-05-08

`manual.md` §3 강화 — 역방향 비약 경고 + DataSheet vs User Manual 분리 추가.

### 변경

- `claude_guideline/manual.md`:
  - **NEW §3.1 역방향 비약 경고**: datasheet → 운영점 해석 시 다음 비약 금지
    - "TYP = 권장값" 비약 (datasheet 명시 없으면 단정 X)
    - "Min/Max 안 = 무조건 OK" 비약 (footnote 측정 조건 충족 필요)
    - "SDK 매크로 수정값 = TYP 일치 = 합리적" 비약 (commit 증거 필요)
  - **NEW §3.2 DataSheet vs User Manual / Family Manual 분리**: pinout/전기 spec vs register-level/SR/DMA 토폴로지. 분석 대상에 따라 추가 PDF 필요. `manual/` 에 두 종류 모두 보관 권장.

### 트리거

20명 매뉴얼 근거 감사팀 (HFPDC ADC 프로젝트, 10 문서 × 2 워커) 의 발견:
- "iLLD 매크로 수정 = datasheet TYP 와 일치 = 합리적" 단정에서 "TYP=권장" 역방향 비약 식별 (m-a, m-b)
- DMA channelId / EVADC SR / GTM ADCTRIG mux 검증이 DataSheet 만으로 불가, User Manual/Family Manual 추가 필요 (w03-a, w03-b, w04-a, w04-b, w05-a, w05-b)
- 측정 조건 (postcalibration, ENRMS, ripple, footnote 2/3) 미인용 시 INL/DNL/TUE 단정 ⓦ 격하 권고 (m-a, m-b, w06-b)

본 패치로 manual.md 가 위 패턴 모두 명시적으로 경고. 다른 프로젝트도 동일 비약 회피 가능.

## 1.6.1 — 2026-05-08

`manual.md` + `skills/manual-first.md` 일반화 — 1.6.0 에서 특정 프로젝트 (HFPDC) 의 칩 / SDK 고유명 (예: AURIX TC38x, fADCI, IfxEvadc 등) 이 SSOT 본문에 노출되어 있던 문제를 정정. SSOT 는 프로젝트 중립이어야 한다.

### 변경

- `claude_guideline/manual.md`:
  - §3 source 분리 예시: 벤더 고유명 → "벤더 SDK / 드라이버 매크로", "`<PERIPHERAL>_<PARAM>_MAX`" 형태 일반 표현
  - §11 다운로드 절차 grep 예시: 칩 고유 파라미터명 → `<parameter_name>` 형태
  - §12 위반 사례: HFPDC 고유명 (AURIX, TC38x, fADCI, IfxEvadc) 모두 제거 → "어느 벤더 SDK 의 `<PARAMETER>_MAX` 매크로" 형태로 패턴만 보존. 상세 사례는 "프로젝트별 case study 파일" 로 outsource
- `skills/manual-first.md`:
  - 키워드 list 에서 칩 고유 파라미터 (`fADCI`, `fSPB`) 제거, 일반 spec 카테고리 (`INL`, `DNL`, `ENRMS`, 외부 표준 ISO/IEEE/UL/UN, 단위 등) 로 대체
  - 도입 사례 섹션 추상화 (HFPDC 명 제거)
- 기존 SSOT 5 섹션 (보관 위치 / 인용 / 추정금지 / 라이선스 / 누락처리) + 신규 6 섹션 (체크리스트 / 등급 / 다운로드 절차 / 변경 절차) 모두 보존, 본 패치는 표현 일반화만

### 트리거

1.6.0 push 직후 사용자 정정: "일반화를 해야지 특정 프로젝트용이면 안됨". SSOT 의 재사용성 보장을 위해 즉시 일반화 패치.

## 1.6.0 — 2026-05-08

`manual.md` 강화 + `skills/manual-first.md` 신규 등록 — datasheet 미참조 거짓 단정 누적 방지.

### `claude_guideline/manual.md` 강화 (42 줄 → 117 줄)

- **NEW §3 source 분리**: `iLLD/SDK 매크로 ≠ silicon datasheet spec` — 본 룰의 핵심 원칙
- **NEW §7 작업 전 체크리스트** (Pre-Work)
- **NEW §8 작업 중 체크리스트** (In-Progress)
- **NEW §9 작업 후 체크리스트** (Post-Work)
- **NEW §10 검증 등급** (✓ 직접 / ⓦ 보고만 / ⚠ 추론) 강제 표기
- **NEW §11 Datasheet 다운로드 표준 절차** (curl + pdftotext + grep)
- **NEW §12 본 룰 위반 시 영향 (실제 사례)** — HFPDC 2026-05-08 ADC 분석 사례
- 기존 SSOT 5 섹션 (보관 위치 / 인용 규칙 / 추정 금지·실측 검증 / 라이선스 / 누락 처리) 모두 보존 + 인용 형식 강제 (`[문서명 v버전, Table N, page P](경로)`)

### `skills/manual-first.md` 신규

- 키워드 (datasheet, 데이터시트, spec, 사양, INL, DNL, AEC-Q100, Operation Conditions, Electrical Characteristics, MHz, fADCI, fSPB, 위반, 초과, non-compliance, violation) 자동 트리거
- 핵심 3 줄 요약 + 작업 전/중/후 체크리스트 + 다운로드 절차 + 도입 사례
- SSOT 룰 ([`manual.md`](manual.md)) 진입점 역할

### 트리거 사건

HFPDC ADC 흐름도 분석 세션 (2026-05-08) — lead 가 iLLD `IFXEVADC_ANALOG_FREQUENCY_MAX = 20MHz` 매크로를 silicon datasheet spec 으로 비약 → "fADCI 33MHz가 datasheet 위반" 거짓 단정 → AEC-Q100 위반 / INL·DNL 무보증 등 downstream 거짓 결론 누적 → 검증팀 8명 launch 의 부분 전제 오염 → 다중 정정 라운드 (v2 → v2.2 → v2.3) 발생, 토큰 / 시간 낭비. 사용자가 datasheet PDF 직접 다운로드 후 검증: fADCI = 16/40/53.33 MHz Min/Typ/Max @ 5V VDDM (TC38x DataSheet v1.2, Table 3-21, page 316) → 33MHz = TYP 안쪽 정상. 본 룰 강화 + 스킬 등록으로 재발 방지.

## 1.5.0 — 2026-05-07

- `iteration_anti_pattern.md` 신규 추가 — Iteration 반복 수정 방지 원칙
  - 핵심 원칙: 1 회 정공법 우선 (2 회 이상 부분 수정 시 전체 재작성 전환)
  - 4 규칙: 기존 자료 우선 조사 / 모호한 단어 추측 금지 / 정정 시 임의 추가분 전체 감사 / 단일 파일도 구조 사전 승인
  - Iteration Loop 탈출 규칙 (2 회 반복 시 작성 중지 + 단어 재정의 질문 + 전체 재작성)
  - 본 규칙은 `coding.md` 및 `workflow.md` 를 강화하며 충돌 시 본 규칙 우선
- `README.md`: 진입점 표에 `iteration_anti_pattern.md` 행 추가
- 트리거 사건: ONE_LINERS.md 5 회 반복 수정 — `claude-mistake/2026-05-07.md` 참조

## 1.4.1 — 2026-05-07

표현 수정 — `skills.md` 를 `skill_update.md` 로 rename. "스킬 목록" 으로 오해할 여지를 줄이고 "스킬 갱신·등록 절차" 의미를 명시화. 내용은 동일.

- `skills.md` → `skill_update.md`
- `README.md`, `templates/CLAUDE.md.template` 의 링크 갱신

## 1.4.0 — 2026-05-07

신규 워크스페이스 자산(스킬 / hook / 가이드라인 / 템플릿)이 SSOT 스킬 레포에 누락되지 않도록 등록 절차를 메타 규칙으로 표준화.

### 추가된 파일

- `skills.md` 신규 추가 — 스킬 / 자동화 자산 SSOT 등록 규칙 (적용 대상 5 종, 등록 절차 6 단계, 워크스페이스↔SSOT 우선순위, 비공개 자산 처리, deprecate 정책)

### 보강된 파일

- `README.md`: 진입점 표에 `skills.md` 행 추가
- `templates/CLAUDE.md.template`: 메타 규칙 진입 링크에 `skills.md` 행 추가

### 신규 정책 요약

- 워크스페이스에서 만든 신규 스킬 / hook / 가이드라인 보강 / sub-agent / 도메인 템플릿은 SSOT 레포(`kuks_claude_setup`)에 등록한다.
- 등록 전 워크스페이스 검증 필수, 비공개 / 환경 의존 부분은 placeholder 또는 `local/` 처리.
- SSOT 가 단일 근원이며 워크스페이스 측 직접 수정 후 SSOT 갱신을 잊는 패턴 금지.

## 1.3.0 — 2026-05-05

ROS2 + 임베디드 + 모듈 CLAUDE.md override 계층을 가진 워크스페이스에서 운영하면서 발견된 규칙 보강. FITO AMR ROS2 워크스페이스 배포에서 검증된 변경분 contributions.

### 추가된 파일

- `ros2.md` 신규 추가 — ROS2 + 임베디드 결합 환경의 도메인 SSOT (빌드 / src 원본 / COLCON_IGNORE / vendored read-only / 시리얼 함정 / 패키지 종류별 주의)
- `manual.md` 신규 추가 — 외부 벤더 매뉴얼·데이터시트 보관·인용·검증 규칙 (추정 금지, 실측 검증, NDA / 라이선스 처리)
- `local/README.md` 신규 추가 — 프로젝트별 비공개 override 폴더 패턴 (하드웨어 IP / 사설 네트워크 / read-only 경로)

### 보강된 파일

- `workflow.md`:
  - 시작 7 항목 / 종료 8 항목 체크리스트로 확장
  - 임베디드 도메인의 펌웨어 다운로드(플래시) 절차 추가 — 포트 점유 확인 → 부트모드 → 플래시 → 실패 시 진단 우선순위
  - 보고 형식을 "매 답변 강제" 에서 "분기 시점에만" 으로 완화 (사전 승인 트리거 / workaround / "기록" / 범위 외 변경)
- `tech_debt.md`:
  - 실시간 / 임베디드 시스템에서 정공법이 특히 중요한 이유 명시
  - 하드웨어 quirk 우회 강화 조항 (벤더 펌웨어 errata / 외부 SDK / 외부 의존성 알려진 버그)
  - TODO 형식 표준화: `// TODO(YYYY-MM-DD): <할 일> [참조]` + 30 일 정리 룰
- `coding.md`:
  - **상수 분리 원칙** 신규 — 의미가 다른 두 값이 우연히 같을 때 한 상수로 합치지 않기 (silent bug 방지)
  - 사전 승인 트리거 5 항목 명시 (패키지 신규 / 외부 인터페이스 변경 / 빌드 시스템 / 하드웨어 인터페이스 / 데이터 스키마)
  - 사전 승인 없이 진행 가능한 변경 명시 (단일 파일 버그 / 파라미터 추가 / 내부 리팩터)
  - 코딩 스타일 섹션 추가 — `.clang-format` 등 저장소 설정 우선, 모듈 CLAUDE.md 가 워크스페이스 가이드보다 우선
  - 보고 양식을 "매 답변" 에서 "변경 분기에서만" 으로 완화
- `github.md`:
  - "기록" 명령에서 push 자동 실행 분리 — push 는 별도 명시 확인 후 수행
  - Read-only 외부 vendored 저장소 가드 섹션 신규 (외부 SDK / 시스템 라이브러리 / COLCON_IGNORE)
  - scope 별 commit 분할 예시 + 자동 staging(`git add -A`/`.`) 금지 명시
  - Push 전 확인에 사설 IP/MAC/endpoint, vendored 원본 저장소 오염 방지 추가
- `documentation.md`:
  - 모듈 CLAUDE.md 가 워크스페이스 가이드를 복제하지 않는다는 SSOT 규칙 명시
  - 도메인 식별자(토픽 / 노드 / 명령 / 레지스터 / 핀맵) 원문 유지 명시
- `README.md`: 진입점 표에 `ros2.md`, `manual.md`, `local/`, `CHANGELOG.md` 행 추가

### 신규 정책 요약

- 모듈 CLAUDE.md override 계층 — 모듈 CLAUDE.md 의 모듈 고유 규칙(핀맵·상수·하드웨어 명령)이 워크스페이스 가이드라인보다 우선
- "기록" → 자동 push 분리
- 보고 형식을 "매 답변 강제" → "분기 시점에만" 으로 완화

## 1.2.0 — 2026-05-01

- `tech_debt.md` 신규 추가 — 기술 부채 방지 원칙 (정공법 우선)
  - 핵심 원칙: 시간이 더 걸리더라도 근본 원인 해결, workaround 금지
  - 우회 사용 시 3가지 조건 (비용/리스크 제시 + 사용자 승인 + 정리 일정 기록) 모두 만족 필수
  - 시간 트레이드오프 보고 의무
  - 임시·진단 코드 정리 / TODO 코멘트 정책 / ADR Open Question 30일 재평가 정책
  - `coding.md` "회피 대안 절대 금지" 와 충돌 시 본 규칙 우선
- `README.md`: 진입점 표에 `tech_debt.md` 행 추가

## 1.1.0 — 2026-04-30

- `github.md`: "커밋·푸쉬는 작업 단위로 분리" 섹션 추가
  - 작업 단위 = 커밋 단위 = push 단위 원칙
  - staged 범위 검증 절차 (`git status --short`, `git diff --cached --name-only`)

## 1.0.0 — 2026-04-30

- 초기 릴리스
- `claude_guideline/` 5 개 파일 추가: `README`, `github`, `coding`, `workflow`, `documentation`
- `install.sh`, `update.sh`, `VERSION`, `CHANGELOG.md` 추가
- `templates/CLAUDE.md.template` 추가 (프로젝트별 CLAUDE.md 골격)

## 정책

- **major** (X.0.0): 기존 규칙과 호환 안 됨, 수동 마이그레이션 필요
- **minor** (X.Y.0): 규칙 추가, 호환됨
- **patch** (X.Y.Z): 오탈자, 표현 수정

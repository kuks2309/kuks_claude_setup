# 코드 작업 규칙

코드 수정·신규 작성 시의 단일 근원 SSOT. 사용자 지시 범위 / 사전 승인 트리거 / 코딩 스타일 / 보고 형식 정의.

## 작업 범위

- 사용자가 요청하지 않은 모델 / 아키텍처 / 구조 변경 금지.
- 요청 범위를 벗어난 코딩 금지.
- 지시사항을 회피하려는 대안 제시 금지 — 단, 지시 먼저 수행한 후 1줄 대안 제안은 허용.
- 영역별 우선순위:
  - 우회 / workaround → [tech_debt.md](tech_debt.md)
  - 반복 부분 수정 → [iteration_anti_pattern.md](iteration_anti_pattern.md)
  - 외부 자료 인용 → [manual.md](manual.md)

## 코드 수정 규칙

- 필요 최소 단위로 수정. 의도와 무관한 리팩토링·이름변경·포맷 변경 금지.
- 명명 규칙 (snake_case / camelCase / PascalCase) 은 해당 파일·모듈의 기존 컨벤션을 따른다.
- 매직 넘버 / 매직 스트링은 상수 분리 (의미 명확화).
- 외부 인용 (datasheet / spec / 매뉴얼) 은 [manual.md](manual.md) 룰 적용 — file:line 또는 page 인용 의무.

## 사전 승인 트리거

다음 변경은 **사용자 명시 승인 후** 진행한다:

| 트리거 | 사유 |
|--------|------|
| 새 패키지 / 모듈 / 폴더 생성 | 프로젝트 구조 변경 |
| 외부 인터페이스 변경 (`.proto`, `.msg`, `.srv`, OpenAPI) | downstream 영향 |
| 빌드 / 의존성 변경 (`CMakeLists.txt`, `package.xml`, `pyproject.toml`) | 빌드 그래프 영향 |
| 코드 (`Source/` 또는 동등 코드 디렉토리) 수정 | 사용자 명시 승인 필수 |
| 정공법이 사용자 지시 범위 초과 | [tech_debt.md](tech_debt.md) §범위 초과 |
| `.gitignore` 우회 / 빌드 산출물 commit | [github.md](github.md) §외부 vendored 보호 |

## 사전 승인 없이 진행 가능

- 단일 파일 내 버그 수정 / 로그 개선 / 주석 보강
- 파라미터 추가 (기본값 보존, 외부 인터페이스 미변경)
- 내부 함수 리팩터 (외부 시그니처 미변경)
- **단**: 의도가 모호한 단일 파일 작업은 [iteration_anti_pattern.md](iteration_anti_pattern.md) §구조 사전 승인 우선.

## 단일 파일 작업 분기

| 파일 종류 | 의도 명확 | 의도 모호 |
|---|---|---|
| 코드 파일 (`.c`, `.cpp`, `.py`, `.h`) | 진행 후 결과 보고 | 1~3줄 구조 요약 후 승인 |
| 문서 파일 (`.md`, `.rst`, `.txt`) | 진행 후 결과 보고 | 1~3줄 구조 요약 후 승인 |
| 스크립트 (`.sh`, alias, 환경 설정) | 진행 + 기존 자료 grep 1회 의무 | 1~3줄 구조 요약 후 승인 |
| 외부 인터페이스 / 빌드 / 의존성 | 사전 승인 필요 | 사전 승인 필요 |

## 코딩 스타일

- 기존 컨벤션 우선 — 새 컨벤션 도입 시 사용자 명시 승인.
- formatter / linter 설정이 있으면 그것을 따른다.
- TODO / FIXME 는 [tech_debt.md](tech_debt.md) §TODO 코멘트 정책 참조.

## 보고 형식

다음 시점에만 사유·영향·확인을 명시 ([workflow.md](workflow.md) §보고 형식 와 동일):

1. 사전 승인 트리거 변경 착수 전
2. 기존 로직 변경 시 (사유 + 영향 범위)
3. 우회 / workaround 결정 전 ([tech_debt.md](tech_debt.md) §우회 3 조건)
4. 정공법으로 추가 시간 예상 시 ([tech_debt.md](tech_debt.md) §시간 트레이드오프)

일상 단순 작업 (파라미터 추가, 로그 보강 등) 은 결과만 1~2줄 보고.

## 변경 절차

본 룰은 SSOT. 변경 시 사용자 승인 필수.

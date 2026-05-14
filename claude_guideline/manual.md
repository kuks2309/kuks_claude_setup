# 외부 매뉴얼 / 데이터시트 인용 (Manual-First)

외부 벤더의 매뉴얼·데이터시트·프로토콜 명세를 **어디에 보관**하고, **어떻게 인용**하며, **어떻게 검증**할지 정하는 SSOT. 본 룰 위반 시 거짓 단정 누적 → 다중 정정 라운드 → 토큰 낭비 / 신뢰 손상.

## 트리거 — 자동 인용 (Passive Cite)

다음 키워드가 사용자 지시·코드·문서에 등장하면 **본 룰을 자동 인용** 한다. 사용자 명시 지시 없이 추가 작업 (다운로드 / 파일 생성 / commit 등) 은 수행하지 않는다 ([skill_update.md](skill_update.md) §자동화 정책).

| 카테고리 | 키워드 |
|---|---|
| 영문 | datasheet, manual, spec, Operation Conditions, Electrical Characteristics, INL, DNL, AEC-Q100, non-compliance, violation |
| 한글 | 데이터시트, 매뉴얼, 사양, 위반, 초과, 무보증 |

## 보관 위치

다운스트림 프로젝트에서 매뉴얼·데이터시트 PDF / 사양서는 다음 한 곳에 저장:

| 위치 | 적용 |
|------|------|
| `manual/` | 워크스페이스 공통 자료 |
| `docs/manual/` | 문서화 중심 프로젝트 |
| `<package>/manual/` | 패키지 고유 자료 |

`.gitignore` 우회·인터넷 재다운로드보다 **로컬 manual/ 우선** — 재현성·오프라인 작업·인용 정합.

## 인용 의무

외부 자료를 참조하는 모든 단정·결정에 다음 두 가지 중 하나 첨부:

- `file:line` (텍스트 자료)
- `<filename>.pdf:p.<page>` (PDF / 데이터시트)

출처 없는 spec 단정 / 임의 추정 금지.

## 검증 절차

1. 본 매뉴얼·데이터시트가 silicon 차원의 1차 source 인지 확인 (벤더 SDK 매크로 / 드라이버 기본값은 silicon spec 비약 가능성).
2. 강한 단정어 ("위반" / "초과" / "non-compliance" / "fail") 사용 전 primary source 인용 확인.
3. TYP / MIN / MAX 구분 — TYP 값은 권장 운용점이 아닌 typical 측정치이며, 역방향 비약 금지 (예: "TYP=권장" 단정).

## 미인용 / 비약 시 대응

- ✓ 표시 / 단정 / "spec 위반" 등을 인용 없이 작성한 경우 → ⚠ 격하 후 인용 추가 후 ✓ 복원.
- 인용 가능한 1차 source 부재 시 → "벤더 SDK 기본값 추정" 등으로 명시 후 사용자에게 보고.

## 변경 절차

본 룰은 SSOT. 변경 시 사용자 승인 필수.

# 사용자 지시 기록 (User Instruction Recording)

사용자 지시 원문을 시간 누적 기록하여 **의도 부채 (Intent Debt)** 를 0 으로 유지하는 SSOT (Single Source of Truth / 단일 근원).

## 트리거

사용자 지시 도착 즉시. 작업 시작 전 기록. 완료 후 일괄 기록 금지.

## 기록 위치

다운스트림 프로젝트의 `docs/user_instructions/user_instructions.md`.

**본 파일은 사용자 원문 전용.** 처리 결과·결론·산출물은 본 파일에 두지 않으며 다른 폴더가 책임진다.

| 산출물 유형 | 기록 위치 |
|------------|----------|
| 일반 작업 로그 | `docs/worklog/YYYY-MM-DD.md` |
| 코드 리뷰 / 평가 | `docs/code_review/<주제>.md` |
| 분석 / 리서치 | `docs/analysis/<주제>.md` |
| 트러블슈팅 | `docs/troubleshooting/<주제>.md` |

## 형식

````markdown
## YYYY-MM-DD HH:MM KST — <짧은 제목>

> "<사용자 원문 인용>"

---
````

## 룰

- **KST (Korea Standard Time / 한국 표준시) 시각** + **시간 역순** (최신 위, prepend)
- **사용자 원문만 인용** — 요약·해석·재구성 금지
- 동일 요구의 단순 재확인은 생략 가능
- 비밀번호 / NDA (Non-Disclosure Agreement / 비공개 합의) / 자격증명은 마스킹

## 금지 헤딩

본 entry 안에 다음 헤딩 사용 금지 — 다른 폴더 책임:

- `### 처리`
- `### 결론`
- `### 산출물`

## 자체 점검

```bash
# 시간 역순 확인
grep "^## " docs/user_instructions/user_instructions.md | head -3

# 금지 헤딩 부재 확인 (출력 없어야 함)
grep -E "^### (처리|결론|산출물)" docs/user_instructions/user_instructions.md
```

## 근거 — 의도 부채

소프트웨어 부채 3 종 중 **의도 부채만 회복 불가능**.

| 부채 | 회복 가능성 | 근거 |
|------|------------|------|
| 기술 부채 | 가능 | 코드 리팩토링 |
| 인지 부채 | 가능 | 재학습 |
| **의도 부채** | **불가능** | 원문 망실 시 추측 외 복원 수단 부재 |

기록 부재 → 사용자 의도가 Claude 추측으로 대체 → 후속 작업이 잘못된 의도 위에 누적 → 회수 비용 기하급수 증가.

## 변경 절차

본 룰은 SSOT. 변경 시 사용자 승인 필수.

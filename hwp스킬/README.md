# hwp스킬 — HWPX 문서 생성·편집 + 렌더 검증

아래 한글(HWP/HWPX) 문서를 프로그래밍 방식으로 생성·편집하고, PDF 렌더로 시각 검증하는 스킬 자산 모음.

## 구성

| 항목 | 내용 | 상태 |
| --- | --- | --- |
| [`hwpx/`](hwpx/) | **설치형 통합 번들** (★ 사용 진입점). 원본 스킬 + 렌더 시각 검증 루프 통합판. `~/.claude/skills/hwpx` 로 폴더 복사만으로 설치 | 현행 |
| [`supplement/`](supplement/) | Windows + 한컴오피스(pyhwpx COM) 렌더 검증 보완 패키지. `hwpx/` 번들의 references/render-verify.md 부록으로 흡수됨 | 보존 (Windows 원조 경로) |
| `gonggong_hwpxskills-main.zip` | 원본 스킬 아카이브 (출처 보존용) | 보존 |

## 설치 (hwpx/ 번들)

```bash
cp -r hwpx ~/.claude/skills/hwpx
bash ~/.claude/skills/hwpx/scripts/setup_env.sh   # Linux 렌더 환경 (루트 불필요, 멱등)
pip install --user python-hwpx                     # ObjectFinder (텍스트 전수 조사)
```

## 핵심 워크플로

```
양식 복사 → 텍스트 전수 조사 → ZIP-level 치환 → 미사용 플레이스홀더 문단 삭제
  → fix_linesegarray → fix_namespaces
  → ★ 렌더 시각 검증 루프 (render_verify.py → PDF→PNG → 눈으로 검토 → 이상 시 반복)
  → 통과 후 완료
```

렌더 시각 검증 루프는 생성·편집 결과를 실제 렌더로 확인해 서식·글자 깨짐·디자인
결함을 잡는 필수 단계다 (구조 검증만으로는 렌더에서만 드러나는 결함을 놓친다).
세부는 [`hwpx/references/render-verify.md`](hwpx/references/render-verify.md).

## 의존 환경

- **Linux** (기본 경로): 포터블 LibreOffice 25.8+ + [H2Orestart](https://github.com/ebandal/H2Orestart) 확장(HWPX import, Java/JRE 필요), poppler-utils(`pdftoppm`/`pdftotext`) 또는 pypdfium2, Nanum 폰트(fontconfig 별칭 포함) — 전부 `hwpx/scripts/setup_env.sh` 가 루트 없이 구성 (poppler 만 시스템 패키지 권장)
- **Windows** (정밀 검증 경로): 한컴오피스 + `pip install pyhwpx pywin32` — `supplement/` 및 번들 render-verify.md 부록 참조
- LibreOffice 렌더는 한컴 한글과 근사치다: 글자 깨짐·치환 오류·서식·디자인 검증에 유효하나, 원본 폰트 부재 시 페이지 경계가 실제 한글과 다를 수 있다. 최종 인쇄 픽셀 검증은 Windows 경로 사용.

# gonggong_hwpxskills — 보완(supplement)

원본 `gonggong_hwpxskills-main.zip` 스킬에 **실전에서 검증한 "렌더 시각 검증 루프"와 한글 렌더 함정 모음**을 추가한 보완 패키지다. 원본을 대체하지 않고 보강한다.

## 왜 필요한가
원본 스킬은 HWPX(Hangul Word Processor XML) 편집(ZIP 텍스트 치환·linesegarray 제거·namespace 정규화)까지는 잘 다루지만, **편집 결과를 실제 한글 렌더로 눈으로 확인하는 단계**가 없다. 구조(XML/ZIP) 검증만으로 "완료"를 선언하면 색·정렬·줄바꿈·페이지 넘침 등 **렌더에서만 드러나는 결함**을 놓친다. 이 보완은 그 마지막 고리를 닫는다.

## 구성
| 파일 | 내용 |
|---|---|
| `references/render-verify.md` | 편집 후 **PDF 출력 → PNG 변환 → 이미지 확인** 파이프라인 (자체 수행) |
| `references/hwp-render-gotchas.md` | 한글 렌더 함정 5종 (새 스타일 margin 무시, lineBreak 무시, 표 쪽나눔, 내어쓰기, 자동화 hang) |
| `scripts/render_to_pdf.py` | pyhwpx로 HWPX→PDF (보안 모달 우회: 백그라운드+visible+register_module) |
| `scripts/pdf_to_png.py` | pypdfium2로 PDF→PNG (poppler 불요) |

## 통합 방법
원본 스킬 `SKILL.md`의 워크플로에 **"5. 렌더 시각 검증"** 단계를 추가하고 위 참조 문서를 링크한다:
> 텍스트 치환 → fix_linesegarray → fix_namespaces → **render_to_pdf → pdf_to_png → 이미지 확인** → (이상 시 반복) → 완료.

## 의존성
```
pip install pyhwpx pywin32 pypdfium2
```
- `pyhwpx`: 한글(Windows, 한컴오피스 설치) COM 자동화. 보안 모듈 자동 등록.
- `pypdfium2`: 번들 렌더러(외부 바이너리 불요)로 PDF→이미지.

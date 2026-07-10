# 렌더 시각 검증 (HWPX 편집 후 필수)

> **원칙: 완료 선언 = 렌더 시각 검증 이후.** 구조(XML/ZIP) 검증만으로 "완료" 금지. 문서 포맷은 레이아웃 캐시·글자속성·표 속성이 렌더를 좌우하므로, 실제 한글 출력을 눈으로 확인해야 색·정렬·줄바꿈·페이지 넘침 결함을 잡을 수 있다.

## 파이프라인
```
편집(ZIP 치환) → fix_linesegarray → fix_namespaces
   → render_to_pdf.py (한글 → PDF)
   → pdf_to_png.py   (PDF → PNG)
   → 이미지 확인 (색/정렬/줄바꿈/페이지수/내용)
   → 이상 있으면 편집으로 복귀 (반복)
```

## 1) PDF 출력 — 반드시 백그라운드 + visible=True
```python
from pyhwpx import Hwp
hwp = Hwp(new=True, visible=True, register_module=True)
hwp.open(src_hwpx)
hwp.save_as(pdf_path, "PDF")
hwp.quit()
```
- **headless(visible=False)·포그라운드 실행은 보안 승인/PDF 저장 모달로 hang**(수 분 타임아웃). 반드시 **백그라운드 프로세스 + visible=True**로 실행.
- `register_module=True`가 파일 접근 보안 대화상자를 억제한다. `RegisterModule` 경고가 떠도 **활성 데스크톱 세션**이면 렌더는 성공한다.
- 비대화형(서비스) 세션엔 인터랙티브 데스크톱이 없어 실패할 수 있다 → 사용자 세션에서 실행.

## 2) PDF → PNG (poppler 불요)
```python
import pypdfium2 as pdfium
pdf = pdfium.PdfDocument(pdf_path)
print("pages:", len(pdf))
pdf[i].render(scale=1.6).to_pil().save(f"p{i+1}.png")   # scale 1.6 ≈ 115dpi
```
- `pdftoppm`(poppler) 없이 번들 렌더러로 변환. LibreOffice·한글 없이도 PNG 확보.

## 3) 페이지별 텍스트 추출 (오버플로/누락 진단)
```python
t = pdf[i].get_textpage().get_text_range()
# 예: 특정 회사/푸터 문자열이 있는지로 페이지 경계·오버플로 탐지
```

## 확인 항목 체크리스트
- [ ] 글자색 (의도한 색인가 / placeholder 색 상속 안 했는가)
- [ ] 이탤릭/굵기 (의도대로인가)
- [ ] 정렬 (LEFT/JUSTIFY — 좁은 셀은 JUSTIFY가 단어 사이 공백을 벌림)
- [ ] 줄바꿈 (겹침 없는가 / 의도한 줄바꿈이 실제 반영됐는가)
- [ ] 페이지 수 (예기치 않은 오버플로로 페이지가 늘지 않았는가)
- [ ] 내용 정합 (치환이 올바른 위치에 들어갔는가)

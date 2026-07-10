#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HWPX(또는 HWP) → PDF 렌더 (pyhwpx / 한글 COM)

렌더 시각 검증 파이프라인의 1단계. 편집한 HWPX를 실제 한글로 열어 PDF로 저장한다.

중요:
  - 반드시 **백그라운드 프로세스 + visible=True**로 실행할 것.
    headless(visible=False)/포그라운드는 보안 승인·PDF 저장 모달로 hang(타임아웃)한다.
  - register_module=True 가 파일 접근 보안 대화상자를 억제한다.
    'RegisterModule ...' 경고가 떠도 활성 데스크톱 세션이면 렌더는 성공한다.
  - Windows + 한컴오피스(한글) 설치 필요.

설치:
  pip install pyhwpx pywin32

사용:
  python render_to_pdf.py <input.hwpx> [output.pdf]
  (output 생략 시 입력과 같은 경로에 .pdf)
"""
import os
import sys
import traceback


def render(src, pdf=None):
    src = os.path.normpath(os.path.abspath(src))
    if pdf is None:
        pdf = os.path.splitext(src)[0] + ".pdf"
    pdf = os.path.normpath(os.path.abspath(pdf))
    if os.path.exists(pdf):
        os.remove(pdf)

    from pyhwpx import Hwp
    hwp = Hwp(new=True, visible=True, register_module=True)
    try:
        hwp.open(src)
        hwp.save_as(pdf, "PDF")
    finally:
        try:
            hwp.quit()
        except Exception:
            pass

    ok = os.path.exists(pdf)
    print("RENDER_DONE" if ok else "RENDER_FAILED",
          "exists=", ok, "size=", (os.path.getsize(pdf) if ok else 0), "path=", pdf)
    return pdf if ok else None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python render_to_pdf.py <input.hwpx> [output.pdf]")
        sys.exit(1)
    try:
        render(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    except Exception:
        traceback.print_exc()
        sys.exit(2)

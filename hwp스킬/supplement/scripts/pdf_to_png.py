#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF → PNG (pypdfium2, 번들 렌더러 — poppler/pdftoppm 불요)

렌더 시각 검증 파이프라인의 2단계. render_to_pdf.py 로 만든 PDF의 페이지를
PNG 이미지로 변환해 눈으로 확인(색/정렬/줄바꿈/페이지수/내용)할 수 있게 한다.

설치:
  pip install pypdfium2

사용:
  python pdf_to_png.py <input.pdf> [outdir] [pages] [scale]
    pages : "all"(기본) 또는 "0,3,5" 또는 "2-6" (0-based)
    scale : 렌더 배율(기본 1.6 ≈ 115dpi)
"""
import os
import sys


def parse_pages(spec, n):
    if not spec or spec == "all":
        return list(range(n))
    out = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out += list(range(int(a), int(b) + 1))
        elif part:
            out.append(int(part))
    return [i for i in out if 0 <= i < n]


def convert(pdf_path, outdir=None, pages="all", scale=1.6):
    import pypdfium2 as pdfium
    pdf_path = os.path.abspath(pdf_path)
    outdir = os.path.abspath(outdir or os.path.dirname(pdf_path) or ".")
    os.makedirs(outdir, exist_ok=True)
    base = os.path.splitext(os.path.basename(pdf_path))[0]

    pdf = pdfium.PdfDocument(pdf_path)
    n = len(pdf)
    idxs = parse_pages(pages, n)
    print("pages:", n, "| rendering:", idxs)
    saved = []
    for i in idxs:
        out = os.path.join(outdir, f"{base}_p{i + 1:02d}.png")
        pdf[i].render(scale=float(scale)).to_pil().save(out)
        saved.append(out)
        print("saved", out)
    return saved


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_png.py <input.pdf> [outdir] [pages] [scale]")
        sys.exit(1)
    convert(
        sys.argv[1],
        sys.argv[2] if len(sys.argv) > 2 else None,
        sys.argv[3] if len(sys.argv) > 3 else "all",
        sys.argv[4] if len(sys.argv) > 4 else 1.6,
    )

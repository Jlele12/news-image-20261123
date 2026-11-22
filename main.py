#!/usr/bin/env python3
"""make.fun news-image-20261123 entry program.

Copies the pre-rendered entry image to /output/entry.png (the grader's
output directory; MAKEFUN_OUTPUT_DIR stands in for it locally).
Node 22 main.ts or Python 3.13 main.py, standard library only.
"""
import os
import shutil

src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
print("wrote", os.path.join(out_dir, "entry.png"))

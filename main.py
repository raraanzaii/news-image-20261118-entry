#!/usr/bin/env python3
"""Entry program for make.fun competition news-image-20261118.

The entry image (entry.png, a front page summing up the world news of
Wednesday 18 November 2026) is stored in this repository beside this
file.  This program copies it, byte for byte, to the output location:

  * the grader runs it with a writable /output directory;
  * local runs set MAKEFUN_OUTPUT_DIR to choose the directory instead.

A pure byte copy is deterministic: the program runs twice and both
runs write exactly the same bytes.  Standard library only, no network.
"""

import os
import shutil
import sys

IMAGE_NAME = "entry.png"


def source_path():
    """Absolute path of the committed image, next to this program."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, IMAGE_NAME)


def output_path():
    """Where the image must land, honouring the harness convention."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, IMAGE_NAME)


def main():
    src = source_path()
    dst = output_path()
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    # copyfile copies content only (no metadata), so the output bytes
    # are exactly the committed image bytes on every run.
    shutil.copyfile(src, dst)
    # Read both files back and refuse to leave a short or altered copy
    # behind: a truncated write would fail the gate silently otherwise.
    with open(src, "rb") as f:
        want = f.read()
    with open(dst, "rb") as f:
        got = f.read()
    if got != want:
        raise SystemExit("copy verification failed: output differs")
    return 0


if __name__ == "__main__":
    sys.exit(main())

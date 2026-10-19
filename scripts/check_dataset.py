#!/usr/bin/env python3
"""Offline layout checker for a user-downloaded MVTec AD dataset (doesn't download files)."""
from pathlib import Path
import argparse
import sys

EXPECTED = (
    "bottle", "cable", "capsule", "carpet", "grid", "hazelnut", "leather",
    "metal_nut", "pill", "screw", "tile", "toothbrush", "transistor",
    "wood", "zipper",
)

def verify(root: Path):
    if not root.is_dir():
        return [f"Dataset folder not found: {root}"]
    problems = []
    for name in EXPECTED:
        category = root / name
        if not category.is_dir():
            problems.append(f"Missing category: {name}")
            continue
        for directory in ("train/good", "test/good", "ground_truth"):
            if not (category / directory).is_dir():
                problems.append(f"Missing folder: {name}/{directory}")
    return problems

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_dir", type=Path, nargs="?", default=Path("datasets/mvtec_ad"))
    args = parser.parse_args()
    issues = verify(args.dataset_dir)
    if issues:
        print("Dataset layout incomplete or not extracted correctly:")
        for problem in issues:
            print("  -", problem)
        print("See datasets/README.md for download and extraction instructions.")
        sys.exit(1)
    print(f"PASS: 15 MVTec AD category directories and primary subfolders found at {args.dataset_dir}")
    print("Note: file content, count and mask consistency are not validated by this quick check.")

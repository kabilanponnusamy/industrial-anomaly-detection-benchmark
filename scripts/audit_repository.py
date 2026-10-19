#!/usr/bin/env python3
"""Strict publication manifest, privacy pattern checks and notebook-output checks."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# This is the exact set of project files approved for publication.
APPROVED = {
    ".gitignore",
    "README.md",
    "requirements.txt",
    "datasets/README.md",
    "notebooks/anomaly_detection_benchmark.ipynb",
    "docs/technical-review.md",
    "docs/observed-results.md",
    "scripts/audit_repository.py",
    "scripts/check_dataset.py",
    "scripts/publish_github.ps1",
    "tests/test_notebook_structure.py",
    "tests/test_dataset_layout.py",
}
PATTERNS = {
    "email": re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"),
    "eight-digit identifier": re.compile(r"(?<!\d)\d{8}(?!\d)"),
    "token or API credential": re.compile(r"(?:ghp_|gho_|ghu_|ghs_|ghr_|github_pat_)[A-Za-z0-9_]{15,}|sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}"),
    "embedded private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "user-specific absolute path": re.compile(r"(?:[A-Z]:\\Users\\|/Users/|/home/[^\s/]+/)", re.I),
}


def main():
    problems = []
    for name in sorted(APPROVED):
        path = ROOT / name
        if not path.is_file():
            problems.append(f"Missing approved file: {name}")
            continue
        if path.stat().st_size > 1_000_000:
            problems.append(f"Unexpected large file: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        # Pattern literals in the auditor itself are not secrets.
        if name != "scripts/audit_repository.py":
            for label, pattern in PATTERNS.items():
                if name == ".gitignore" and label == "token or API credential":
                    continue
                matches = pattern.findall(text)
                if label == "email":
                    matches = [m for m in matches if not m.endswith("@users.noreply.github.com")]
                if matches:
                    problems.append(f"Possible {label}: {name}")

    notebook = ROOT / "notebooks/anomaly_detection_benchmark.ipynb"
    if notebook.is_file():
        try:
            nb = json.loads(notebook.read_text(encoding="utf-8"))
            for i, cell in enumerate(nb["cells"]):
                if cell.get("cell_type") == "code" and (cell.get("outputs") or cell.get("execution_count") is not None):
                    problems.append(f"Notebook has retained outputs: cell {i}")
                if cell.get("attachments"):
                    problems.append(f"Notebook embedded attachments: cell {i}")
        except (ValueError, KeyError) as exc:
            problems.append(f"Invalid notebook: {exc}")

    # Important: .gitignore alone does not protect against accidentally staged files.
    if "--staged" in sys.argv:
        proc = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT"], cwd=ROOT,
                              capture_output=True, text=True, check=True)
        staged = set(proc.stdout.splitlines())
        for file in sorted(staged - APPROVED):
            problems.append(f"UNAPPROVED STAGED FILE: {file}")
        if not staged:
            problems.append("No files staged for publication")

    if problems:
        for problem in problems:
            print("FAIL:", problem)
        return 1
    print("PASS: approved files have no matches to configured ID, email, key, path or token patterns.")
    print("PASS: notebook contains no saved execution outputs or attachments.")
    if "--staged" in sys.argv:
        print("PASS: staged Git file inventory is within the approved publication manifest.")
    print("NOTE: automated scanning cannot guarantee that all personal information is absent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

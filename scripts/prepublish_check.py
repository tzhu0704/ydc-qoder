#!/usr/bin/env python3
"""Fail closed on common secrets and private paths before publishing this repository."""

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EXCLUDED_PARTS = {".git", "__pycache__", ".venv", "venv", "dist", "build"}
PRIVATE_NAME = re.compile(r"(^\.env(?:\..+)?$|\.(?:pem|key|p12|pfx)$|(?:credentials|secrets).*\.json$)", re.I)
PATTERNS = {
    "absolute home path": re.compile(r"/(?:Users|home)/[^/\s`]+/"),
    "private vault reference": re.compile(r"\b" + "llm" + "wiki" + r"\b|\b" + "search" + "_ydc" + r"\b", re.I),
    "private key block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "credential assignment": re.compile(
        r"(?i)\b(?:YDC_API_KEY|YOUSEARCH_API_KEY|api[_-]?key|access[_-]?token|client[_-]?secret)"
        r"\s*[=:]\s*['\"]?(?!<|\{|\$|\.|\s|none\b|false\b|true\b)[A-Za-z0-9_./+\-=]{16,}"
    ),
    "bearer credential": re.compile(r"(?i)\bBearer\s+(?!<|\$|\{)[A-Za-z0-9_\-\.]{16,}"),
}


def files_to_check():
    if (ROOT / ".git").exists():
        proc = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                              cwd=ROOT, capture_output=True, check=True)
        return [ROOT / p.decode() for p in proc.stdout.split(b"\0") if p]
    return [p for p in ROOT.rglob("*") if p.is_file() and not set(p.relative_to(ROOT).parts) & EXCLUDED_PARTS]


def main():
    findings = []
    for path in files_to_check():
        relative = path.relative_to(ROOT)
        if path.is_symlink():
            findings.append((str(relative), "symlink: inspect target manually"))
            continue
        if PRIVATE_NAME.search(path.name):
            findings.append((str(relative), "private filename"))
            continue
        if not path.exists():
            continue
        data = path.read_bytes()
        if b"\0" in data[:4096]:
            findings.append((str(relative), "binary file: inspect manually"))
            continue
        text = data.decode("utf-8", errors="replace")
        for name, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append((f"{relative}:{line}", name))
    if findings:
        for location, reason in findings:
            print(f"REVIEW {location}: {reason}")  # Do not print matched secret values.
        return 1
    print("PASS: no high-confidence secrets, private paths, or private filenames detected")
    print("Note: this is a heuristic scan; manually review the staged diff and repository history.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

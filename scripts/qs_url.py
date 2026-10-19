#!/usr/bin/env python3
"""Write a QuickStatements 3.0 batch URL next to each .qs file.

Usage: python3 scripts/qs_url.py batches/<base>.qs [more.qs ...]

For every <name>.qs this writes <name>.qs.url holding one line per batch:
https://qs-dev.toolforge.org/batch/new?v1=<percent-encoded commands>

Batches longer than MAX_URL_LENGTH are split into several URLs, at CREATE
lines where the file has them, so that no new item is cut in half. Open the
URLs in order.

Refuses files that still contain placeholders such as Q<ZA-Prot> or lines
without TAB separators, since QuickStatements would reject or misread them.
"""

import re
import sys
import urllib.parse
from pathlib import Path

QS_BASE_URL = "https://qs-dev.toolforge.org/batch/new?v1="
PLACEHOLDER_RE = re.compile(r"Q<[^>]*>")
# Browsers and Toolforge's proxy start failing somewhere above this length.
MAX_URL_LENGTH = 8000


def commands(path):
    return [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def problems(lines):
    out, placeholders = [], {}
    for n, line in enumerate(lines, 1):
        for p in PLACEHOLDER_RE.findall(line):
            placeholders.setdefault(p, []).append(n)
        if line != "CREATE" and "\t" not in line:
            out.append(f"line {n}: no TAB separator")
    for p, ns in placeholders.items():
        out.append(f"placeholder {p} on {len(ns)} line(s), first line {ns[0]}")
    return out


def batch_url(lines):
    return QS_BASE_URL + urllib.parse.quote("\n".join(lines), safe="")


def blocks(lines):
    """Split into CREATE blocks, or single lines if there is no CREATE."""
    if "CREATE" not in lines:
        return [[l] for l in lines]
    out = []
    for line in lines:
        if line == "CREATE" or not out:
            out.append([])
        out[-1].append(line)
    return out


def chunks(lines):
    out = [[]]
    for block in blocks(lines):
        if out[-1] and len(batch_url(out[-1] + block)) > MAX_URL_LENGTH:
            out.append([])
        out[-1] += block
    return out


def main(paths):
    failed = False
    for arg in paths:
        path = Path(arg)
        lines = commands(path)
        if errors := problems(lines):
            failed = True
            print(f"{path}: not written")
            for e in errors:
                print(f"  {e}")
            continue
        urls = [batch_url(c) for c in chunks(lines)]
        out = path.with_name(path.name + ".url")
        out.write_text("\n".join(urls) + "\n", encoding="utf-8")
        print(f"{out}: {len(lines)} commands in {len(urls)} URL(s)")
        if any(len(u) > MAX_URL_LENGTH for u in urls):
            print(f"  warning: a single item exceeds {MAX_URL_LENGTH} characters; paste the .qs file instead")
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1:]))

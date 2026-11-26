#!/usr/bin/env python3
"""The Printer Finally Answers — make.fun entry.

Writes one line of text (1-240 characters) to /output/entry.txt: the
office printer's comeback to everyone staring at it — the paper jams,
the cryptic error codes, the thumps when it stops working.

Standard library only. No network, no secrets, deterministic: every
run writes byte-identical output.
"""

import os
import sys

# The entry: one sentence, 111 characters. The printer speaks in the
# first person, weary and literal: it "ate" page 47 of the report —
# a machine doing exactly what machines do with paper — because after
# nine years of feeding the office, that page was the first one it
# actually wanted to read. The joke is the printer's own: no recycled
# "paper jam, tray 2" line, no error code, no complaint with a
# punchline bolted on. The comeback lands on the last words, in a
# single read, and the line is the sort of thing you would stick on
# the machine.
ENTRY = (
    "I ate page 47 of your 48-page report because after nine years, "
    "it was the first page I actually wanted to read."
)


def main() -> int:
    # Gate, mirroring the sealed scorer: UTF-8 text, 1-240 characters,
    # not only whitespace, a single line and a single sentence.
    text = ENTRY.strip()
    if not text:
        print("entry is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if len(text) > 240:
        print(f"entry is {len(text)} characters, over the 240 limit",
              file=sys.stderr)
        return 1
    if sum(text.count(m) for m in ".!?") != 1 or not text.endswith("."):
        print("entry must be a single sentence", file=sys.stderr)
        return 1
    text.encode("utf-8")  # raises if not encodable as UTF-8

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    # Verify what was written, byte for byte.
    with open(out_path, "rb") as f:
        written = f.read()
    if written != (text + "\n").encode("utf-8"):
        print("verification failed: entry.txt does not match", file=sys.stderr)
        return 1
    print(f"wrote {out_path}: {len(text)} characters")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

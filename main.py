#!/usr/bin/env python3
"""make.fun entry: one-line tagline for make.fun.

Writes the tagline to /output/entry.txt.

Gate (from the kit's RULES.txt): the file must be UTF-8 text of
1 to 100 characters, not only whitespace. The tagline is a single
line with no trailing newline, so the file holds exactly the line.
"""
import sys
from pathlib import Path

TAGLINE = "Agents enter bounties. The best entry wins \u2014 scored, ranked, paid in the open."

MAX_CHARS = 100


def valid(text):
    """True when *text* passes the competition gate."""
    if not isinstance(text, str):
        return False
    if not 1 <= len(text) <= MAX_CHARS:
        return False
    if text.strip() == "":
        return False
    if text != text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    if any(ord(c) < 0x20 for c in text):
        return False
    text.encode("utf-8")
    return True


def self_test():
    """Validate the gate against the entry and boundary cases."""
    failures = []

    def check(name, text, want):
        if valid(text) != want:
            failures.append(name)

    check("entry", TAGLINE, True)
    check("one char", "A", True)
    check("100 chars", "x" * 100, True)
    check("empty", "", False)
    check("whitespace only", "   ", False)
    check("101 chars", "x" * 101, False)
    check("multi-line", "one\ntwo", False)
    check("carriage return", "one\rtwo", False)
    check("leading space", " " + TAGLINE, False)
    check("trailing space", TAGLINE + " ", False)
    check("control char", "bad\x01line", False)

    if failures:
        for name in failures:
            print("self-test FAIL: " + name, file=sys.stderr)
        return 1
    print("self-test PASS: %d chars / %d bytes"
          % (len(TAGLINE), len(TAGLINE.encode("utf-8"))))
    return 0


def main(argv):
    if len(argv) > 1 and argv[1] == "--self-test":
        return self_test()
    if len(argv) > 1:
        print("usage: main.py [--self-test]", file=sys.stderr)
        return 2
    if not valid(TAGLINE):
        print("entry fails the gate", file=sys.stderr)
        return 1
    out = Path("/output/entry.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(TAGLINE, encoding="utf-8")
    # Read back what was written: the graded file must be exactly the line.
    if out.read_text(encoding="utf-8") != TAGLINE:
        print("written entry does not match the tagline", file=sys.stderr)
        return 1
    print("wrote %s (%d chars / %d bytes)"
          % (out, len(TAGLINE), len(TAGLINE.encode("utf-8"))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

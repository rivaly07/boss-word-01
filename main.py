"""One Word for the Boss — the entry is exactly one word, nothing else.

The bounty asks for a single word that describes the boss, so the output is a
bare token: no caption, no punctuation wrapper, no spaces, at most 30
characters. This module keeps the word in one constant and refuses to write
anything that breaks the rule.
"""

import os
import sys

WORD = "Overpromiser"


def build_entry():
    assert 1 <= len(WORD) <= 30, "word must be 1..30 characters"
    assert WORD.strip(), "word must not be blank or whitespace"
    assert " " not in WORD, "word must not contain a space"
    assert not any(c.isspace() for c in WORD), "word must be a single token"
    WORD.encode("utf-8")
    return WORD


def main():
    try:
        word = build_entry()
    except AssertionError as exc:
        print("refused: %s" % exc, file=sys.stderr)
        return 2

    data = word.encode("utf-8")
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SystemExit("refused: word is not valid UTF-8: %s" % exc)

    n = len(data)
    if not 1 <= n <= 30:
        raise SystemExit("refused: encoded word is %d bytes, gate allows 1..30" % n)

    out_path = os.environ.get("OUTPUT", "/output/entry.txt")
    parent = os.path.dirname(os.path.abspath(out_path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(data)

    print(len(data))
    print(word)
    return 0


if __name__ == "__main__":
    sys.exit(main())

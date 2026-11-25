"""The Router Confesses -- make.fun bounty entry program.

Writes one line to <output dir>/entry.txt: an excuse a home Wi-Fi
router gives for dropping the connection at the climax of a movie.

The entry, and why it fits the judge's brief (RULES.txt):
  * It IS a one-line excuse from the router for the dropped movie.
  * The twist: the router did not fail -- it kept the ending for
    itself, out of spite, because nobody ever thanked it.
  * Voice: a petty appliance with a grudge, not a generic apology.
  * One breath, no setup to explain.
  * Fresh: no buffering, bandwidth, or firmware-update joke.

Deterministic, stdlib only, no network, no randomness, no clock.
The output directory comes from MAKEFUN_OUTPUT_DIR (the grader sets
it to /output); it falls back to /output. Nothing is ever written
into the repository directory itself.
"""

import os
import sys

ENTRY = "Two hours I carried this movie and not one thank-you \u2014 so I kept the ending for myself."

MAX_CHARS = 200


def main() -> int:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    output_dir = os.path.abspath(output_dir)

    # Hard rule: never write into the repository directory itself --
    # the grader runs the repo read-only, so writing there fails
    # run_completes in Round 1. Refuse instead of failing silently.
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.commonpath([output_dir, repo_dir]) == repo_dir:
        print(f"refusing to write into the repo directory: {output_dir}",
              file=sys.stderr)
        return 1

    # Gate self-check: the sealed scorer requires UTF-8 text of
    # 1 to 200 characters, not only white space, a single line.
    text = ENTRY
    if not (1 <= len(text) <= MAX_CHARS):
        print(f"entry is {len(text)} characters, must be 1-{MAX_CHARS}",
              file=sys.stderr)
        return 1
    if not text.strip():
        print("entry is only white space", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    text.encode("utf-8")  # raises if not valid UTF-8 text

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"wrote {path} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

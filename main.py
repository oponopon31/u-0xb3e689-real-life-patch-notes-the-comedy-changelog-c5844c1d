"""Real-Life Patch Notes: The Comedy Changelog.

Writes a single patch-note line (at most 160 characters) to entry.txt.

Candidate lines, judged pairwise on patch-note format, everyday truth,
and whether the punch lands at the end:

1. "v1.9.3: fixed a bug where socks entered the dryer in pairs and exited
   as a single sock with no memory of its partner."
   Format: clean version + "fixed a bug where". Truth: everyone has lost
   a sock to the dryer. Punch: "no memory of its partner" lands last
   and personifies the survivor. Beats the others.

2. "v2.1.4: fixed a bug where the phone battery drained 40% faster the
   moment you actually needed it."
   Format: clean. Truth: universal. Punch: weak -- "the moment you
   actually needed it" is expected, no surprise twist. Loses to (1).

3. "v1.3.7: resolved an issue where sneezing in bright sunlight triggered
   a second, entirely unnecessary sneeze."
   Format: fine. Truth: real (photic sneeze reflex) but niche -- not
   everyone sneezes at sunlight. Punch: "entirely unnecessary" is mild.
   Loses to (1) on universality.

4. "v4.0.2: fixed a bug where autocorrect replaced a correct word with a
   worse one and then refused to admit it was wrong."
   Format: clean. Truth: universal. Punch: "refused to admit it was
   wrong" is funny, but the setup is long and the blame lands on a
   feature people already joke about constantly. Loses narrowly to (1).

5. "v2.7.1: fixed a bug where a five-minute nap snoozed itself into a
   full night's sleep and a missed morning."
   Format: clean. Truth: relatable. Punch: "missed morning" is a
   consequence, not a joke. Loses to (1).

Winner: candidate 1 -- the dryer sock. It has the tightest format, the
most universal everyday truth, and the punch ("no memory of its
partner") lands on the final word.
"""

import hashlib
import os
import re
import sys

LINE = (
    "v1.9.3: fixed a bug where socks entered the dryer in pairs and "
    "exited as a single sock with no memory of its partner."
)


def output_dir() -> str:
    """Resolve where entry.txt goes: env var, /output, else cwd."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output") and os.access("/output", os.W_OK):
        return "/output"
    return os.getcwd()


def validate(line: str) -> None:
    """Exactly one line, 1-160 chars, no blank, no control chars."""
    if not line or line != line.strip():
        raise ValueError("line must be non-empty with no surrounding whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must contain no newline characters")
    if len(line) > 160:
        raise ValueError(f"line is {len(line)} chars, over the 160 limit")
    if not re.match(r"^v\d+\.\d+\.\d+: ", line):
        raise ValueError("line must open with a release-note version tag (vX.Y.Z: )")
    for ch in line:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            raise ValueError(f"control character U+{ord(ch):04X} in line")


def main() -> int:
    validate(LINE)
    data = (LINE + "\n").encode("utf-8")
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as fh:
        fh.write(data)
    # Re-read and assert the exact bytes match what we intended.
    with open(path, "rb") as fh:
        written = fh.read()
    assert written == data, "entry.txt bytes do not match the chosen line"
    digest = hashlib.sha256(written).hexdigest()
    print(f"chars: {len(LINE)}")
    print(f"bytes: {len(written)}")
    print(f"sha256: {digest}")
    print(f"wrote: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

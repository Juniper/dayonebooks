#!/usr/bin/env python3
import sys
import re
from pathlib import Path

# List of "bad" invisible characters that Pandoc/LaTeX often choke on
BAD_CHARS = [
    "\u200b",  # ZERO WIDTH SPACE
    "\u200c",  # ZERO WIDTH NON-JOINER
    "\u200d",  # ZERO WIDTH JOINER
    "\u2060",  # WORD JOINER
    "\ufeff",  # ZERO WIDTH NO-BREAK SPACE (BOM)
]

# Map of problematic Unicode characters to safe replacements
REPLACEMENTS = {
    "\u2010": "-",  # HYPHEN
    "\u2011": "-",  # NON-BREAKING HYPHEN
    "\u2012": "-",  # FIGURE DASH
    "\u2013": "-",  # EN DASH
    "\u2014": "-",  # EM DASH
    "\u2015": "-",  # HORIZONTAL BAR
    "\u2212": "-",  # MINUS SIGN
}

# Regex for general control characters (U+0000–U+001F, U+007F), except \t \n \r
CONTROL_CHAR_REGEX = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")

def sanitize(text: str) -> str:
    # Remove invisible "bad" chars explicitly
    for ch in BAD_CHARS:
        text = text.replace(ch, "")

    # Replace problematic Unicode dashes/minus with ASCII "-"
    for bad, good in REPLACEMENTS.items():
        text = text.replace(bad, good)

    # Remove other control characters
    text = CONTROL_CHAR_REGEX.sub("", text)

    return text

def main():
    if len(sys.argv) < 2:
        print("Usage: sanitize_md.py <file.md>")
        sys.exit(1)

    infile = Path(sys.argv[1])
    outfile = infile.with_stem(infile.stem)

    text = infile.read_text(encoding="utf-8")
    cleaned = sanitize(text)
    outfile.write_text(cleaned, encoding="utf-8")

    print(f"✅ Cleaned file written to {outfile}")

if __name__ == "__main__":
    main()
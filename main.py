"""Never Say It Out Loud — entry program.

Reads the one-line confession from entry.txt next to this file and writes
it to /output/entry.txt, the artifact the sealed gate scorer reads.
"""

from pathlib import Path

MAX_CHARS = 200


def is_printable_text(line: str) -> bool:
    """Reject control characters the gate would treat as non-text."""
    return all(ord(ch) >= 0x20 or ch in "\t" for ch in line)


def load_line(path: Path) -> str:
    """Read and validate the single entry line."""
    text = path.read_text(encoding="utf-8")
    line = text.strip()
    if not line:
        raise ValueError("entry.txt is empty")
    if not is_printable_text(line):
        raise ValueError("entry contains control characters")
    if len(line) > MAX_CHARS:
        raise ValueError(f"entry is {len(line)} chars, over the 200 limit")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    return line


def write_output(line: str) -> Path:
    """Write the line to the grader's artifact path."""
    out_dir = Path("/output")
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / "entry.txt"
        target.write_text(line, encoding="utf-8")
    except OSError:
        fallback = Path(__file__).with_name("output")
        fallback.mkdir(parents=True, exist_ok=True)
        target = fallback / "entry.txt"
        target.write_text(line, encoding="utf-8")
    written = target.read_text(encoding="utf-8")
    if written != line:
        raise ValueError("round-trip check failed: written text differs")
    return target


def main() -> None:
    entry_path = Path(__file__).with_name("entry.txt")
    line = load_line(entry_path)
    target = write_output(line)
    print(f"Wrote {len(line)} chars to {target}")
    print(line)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEST_ROOT = ROOT / "config" / "ftbquests" / "quests"

DESCRIPTION_RE = re.compile(r"(?P<indent>^[ \t]*)description:\s*\[(?P<body>.*?)\]", re.MULTILINE | re.DOTALL)
STRING_RE = re.compile(r'"((?:\\.|[^"\\])*)"')
TITLE_RE = re.compile(r'(?P<prefix>\btitle:\s*)"(?P<text>(?:\\.|[^"\\])*)"')
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")

MAX_PARAGRAPH_CHARS = 150


def decode(raw: str) -> str:
    return json.loads(f'"{raw}"')


def encode(text: str) -> str:
    return json.dumps(text, ensure_ascii=False)


def safe_text(text: str) -> str:
    # FTB Quests treats '&' as a legacy formatting prefix. Natural-language
    # ampersands therefore render as "Invalid formatting" unless escaped.
    return text.replace(" & ", " and ")


def split_paragraph(text: str) -> list[str]:
    text = safe_text(text.strip())
    if not text:
        return []
    if len(text) <= MAX_PARAGRAPH_CHARS:
        return [text]

    sentences = [part.strip() for part in SENTENCE_SPLIT_RE.split(text) if part.strip()]
    if len(sentences) <= 1:
        return [text]

    paragraphs: list[str] = []
    current = ""
    for sentence in sentences:
        candidate = sentence if not current else f"{current} {sentence}"
        if current and len(candidate) > MAX_PARAGRAPH_CHARS:
            paragraphs.append(current)
            current = sentence
        else:
            current = candidate
    if current:
        paragraphs.append(current)
    return paragraphs


def format_description(match: re.Match[str]) -> str:
    indent = match.group("indent")
    raw_values = STRING_RE.findall(match.group("body"))
    values = [decode(raw) for raw in raw_values]

    # Treat existing empty strings as paragraph separators, then also split
    # oversized prose at sentence boundaries so compact quest windows stay readable.
    paragraphs: list[str] = []
    for value in values:
        if not value.strip():
            continue
        paragraphs.extend(split_paragraph(value))

    if not paragraphs:
        return match.group(0)

    entry_indent = indent + "\t"
    rendered: list[str] = [f"{indent}description: ["]
    for index, paragraph in enumerate(paragraphs):
        if index:
            rendered.append(f'{entry_indent}""')
        rendered.append(f"{entry_indent}{encode(paragraph)}")
    rendered.append(f"{indent}]")
    return "\n".join(rendered)


def format_content(content: str) -> str:
    content = DESCRIPTION_RE.sub(format_description, content)

    def format_title(match: re.Match[str]) -> str:
        text = safe_text(decode(match.group("text")))
        return f'{match.group("prefix")}{encode(text)}'

    return TITLE_RE.sub(format_title, content)


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize FTB Quests display text for readability and safe formatting.")
    parser.add_argument("--write", action="store_true", help="Rewrite quest files in place instead of only checking them.")
    args = parser.parse_args()

    changed: list[Path] = []
    for path in sorted(QUEST_ROOT.rglob("*.snbt")):
        original = path.read_text(encoding="utf-8")
        formatted = format_content(original)
        if formatted == original:
            continue
        changed.append(path)
        if args.write:
            path.write_text(formatted, encoding="utf-8")

    if args.write:
        if changed:
            for path in changed:
                print(f"formatted {path.relative_to(ROOT)}")
        else:
            print("Quest text already formatted.")
        return 0

    if changed:
        for path in changed:
            print(f"ERROR: quest text needs formatting: {path.relative_to(ROOT)}")
        print("Run: python tools/format_quest_text.py --write")
        return 1

    print("Quest text formatting OK: readable paragraph breaks and safe display text are normalized.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

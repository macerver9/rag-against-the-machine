import re


def is_table_separator(line: str) -> bool:
    """Check whether a line is a Markdown table separator."""

    pattern = r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$"

    return bool(re.match(pattern, line))


def get_code_fence(line: str) -> str | None:
    """Return the code fence marker if the line opens a fenced block."""

    match = re.match(r"^\s*(`{3,}|~{3,})", line)

    if match:
        return match.group(1)

    return None


def is_code_fence_end(line: str, marker: str) -> bool:
    """Check whether a line closes a fenced code block."""

    pattern = rf"^\s*{re.escape(marker[0])}{{{len(marker)},}}\s*$"

    return bool(re.match(pattern, line))


def get_heading_level(line: str) -> int | None:
    """Return the heading level if the line is a Markdown heading."""

    match = re.match(r"^ {0,3}(#{1,6})(?:[ \t]+|$)", line)

    if match:
        return len(match.group(1))

    return None


def get_line_offsets(lines: list[str]) -> list[int]:
    """Return the starting character position of each line."""

    offsets: list[int] = []
    offset = 0

    for line in lines:
        offsets.append(offset)
        offset += len(line)

    return offsets


def get_setext_heading_level(line: str) -> int | None:
    """Return the heading level if the line is a Setext under line."""

    match = re.match(r"^ {0,3}(=+|-+)[ \t]*$", line)

    if match:
        return 1 if "=" in match.group(1) else 2

    return None
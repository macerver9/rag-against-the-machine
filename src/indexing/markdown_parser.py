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


def find_markdown_tables(content: str) -> list[tuple[int, int]]:
    """Find Markdown tables and return their character positions."""

    lines = content.splitlines(keepends=True)
    tables: list[tuple[int, int]] = []

    offset = 0
    offsets: list[int] = []

    for line in lines:
        offsets.append(offset)
        offset += len(line)

    i = 0

    in_code_block = False
    code_marker = ""

    while i < len(lines):
        if in_code_block:
            if is_code_fence_end(lines[i], code_marker):
                in_code_block = False
                code_marker = ""

            i += 1
            continue

        marker = get_code_fence(lines[i])

        if marker is not None:
            in_code_block = True
            code_marker = marker

            i += 1
            continue

        if (
            i + 1 < len(lines)
            and "|" in lines[i]
            and is_table_separator(lines[i + 1])
        ):
            start = offsets[i]
            i += 2

            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                i += 1

            end = offsets[i - 1] + len(lines[i - 1])
            tables.append((start, end))
            continue

        i += 1

    return tables
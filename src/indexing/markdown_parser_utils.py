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

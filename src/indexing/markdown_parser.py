import re


def is_table_separator(line: str) -> bool:
    """Check whether a line is a Markdown table separator."""

    pattern = r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$"

    return bool(re.match(pattern, line))


def find_markdown_tables(content: str) -> list[tuple[int, int]]:
    """Find Markdown tables and return their character positions."""
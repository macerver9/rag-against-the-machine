from src.indexing.chunk import MarkdownBlock
from src.indexing.markdown_parser_utils import (
    get_code_fence,
    is_code_fence_end,
    is_table_separator,
    get_line_offsets,
    get_heading_level,
    get_setext_heading_level
)


def find_markdown_tables(content: str) -> list[MarkdownBlock]:
    """Find Markdown tables and return their character positions."""

    lines = content.splitlines(keepends=True)
    tables: list[MarkdownBlock] = []

    offsets = get_line_offsets(lines)

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
            tables.append(
                MarkdownBlock(
                    type="table",
                    start=start,
                    end=end,
                )
            )
            continue

        i += 1

    return tables


def find_markdown_headings(content: str) -> list[MarkdownBlock]:
    """Find Markdown headings and return their character positions"""

    lines = content.splitlines(keepends=True)
    offsets = get_line_offsets(lines)

    headings: list[MarkdownBlock] = []

    in_code_block = False
    code_marker = ""

    i = 0

    while i < len(lines):
        line = lines[i]

        if in_code_block:
            if is_code_fence_end(line, code_marker):
                in_code_block = False
                code_marker = ""

            i += 1
            continue

        marker = get_code_fence(line)

        if marker is not None:
            in_code_block = True
            code_marker = marker
            i += 1
            continue

        level = get_heading_level(line)

        if level is not None:

            start = offsets[i]
            end = start + len(line)

            headings.append(
                MarkdownBlock(
                    type="heading",
                    start=start,
                    end=end,
                    level=level
                )
            )

            i += 1
            continue

        if i + 1 < len(lines):
            next_line = lines[i + 1]
            level = get_setext_heading_level(next_line)

            if line.strip() and level is not None:
                start = offsets[i]
                end = offsets[i + 1] + len(next_line)

                headings.append(
                    MarkdownBlock(
                        type="heading",
                        start=start,
                        end=end,
                        level=level,
                    )
                )

                i += 2
                continue

        i += 1

    return headings



def find_markdown_paragraphs(content: str) -> list[MarkdownBlock]:
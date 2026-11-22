
from src.indexing.chunk import MarkdownBlock
from src.indexing.markdown_parser_utils import (
    get_code_fence,
    is_code_fence_end,
    get_heading_level,
    get_line_offsets,
    get_setext_heading_level,
)


def parse_markdown(content: str) -> list[MarkdownBlock]:
    """Parse Markdown content into ordered structural blocks."""

    lines = content.splitlines(keepends=True)
    offsets = get_line_offsets(lines)

    blocks: list[MarkdownBlock] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        marker = get_code_fence(line)
        level_atx = get_heading_level(line)

        if marker is not None:
            start = offsets[i]
            i += 1

            while i < len(lines) and not is_code_fence_end(lines[i], marker):
                i += 1

            if i < len(lines):
                i += 1

            end = offsets[i] if i < len(lines) else len(content)

            blocks.append(
                MarkdownBlock(
                    type="code",
                    start=start,
                    end=end,
                )
            )
            continue

        if level_atx is not None:
            blocks.append(
                MarkdownBlock(
                    type="heading",
                    start=offsets[i],
                    end=offsets[i] + len(line),
                    level=level_atx,
                )
            )
            i += 1
            continue

        level_setext = None

        if i + 1 < len(lines) and line.strip():
            level_setext = get_setext_heading_level(lines[i + 1])

        if level_setext is not None:
            blocks.append(
                MarkdownBlock(
                    type="heading",
                    start=offsets[i],
                    end=offsets[i + 1] + len(lines[i + 1]),
                    level=level_setext,
                )
            )
            i += 2
            continue

        start = i

        while i < len(lines):
            marker = get_code_fence(lines[i])
            heading = get_heading_level(lines[i])

            setext = None
            if i + 1 < len(lines) and lines[i].strip():
                setext = get_setext_heading_level(lines[i + 1])

            if marker is not None or heading is not None or setext is not None:
                break

            i += 1

        end = offsets[i] if i < len(lines) else len(content)

        blocks.append(
            MarkdownBlock(
                type="content",
                start=offsets[start],
                end=end,
            )
        )

    return blocks

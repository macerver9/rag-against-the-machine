from src.indexing.chunk import MarkdownBlock
from src.indexing.markdown_parser_utils import (
    get_code_fence,
    is_code_fence_end,
    get_heading_level,
    get_line_offsets,
    get_setext_heading_level,
)


def parser_markdown(content: str) -> list[MarkdownBlock]:
    """Parse Markdown content into ordered structural blocks."""

    lines = content.splitlines(keepends=True)
    offsets = get_line_offsets(lines)

    blocks: list[MarkdownBlock] = []

    i = 0

    while i < len(lines):
        line = lines[i]



        i += 1
    
    return blocks
from src.indexing.chunk import Chunk
from src.indexing.markdown_parser import parse_markdown


def update_heading_context(
    headings: list[tuple[int, str]],
    level: int,
    heading: str,
) -> None:
    """Update the heading hierarchy with a new heading."""

    while headings and headings[-1][0] >= level:
        headings.pop()

    headings.append((level, heading))


def find_split_position(
        text: str,
        start: int,
        char_limit: int,
) -> int:
    """FInd the best position to split a text block."""

    end = min(start + char_limit, len(text))

    if end == len(text):
        return end

    separators = ["\n\n", "\n", " "]

    for separator in separators:
        position = text.rfind(separator, start, end)

        if position > start:
            return position + len(separator)

    return end


def split_long_block(
        text: str,
        char_limit: int,
) -> list[str]:
    """Returns chunks thats match the size limit"""
    parts: list[str] = []
    start = 0

    while start < len(text):
        end = find_split_position(text, start, char_limit)

        if end == start:
            break

        if end > start:
            parts.append(text[start:end])

        start = end

    assert "".join(parts) == text
    assert all(len(part) <= char_limit for part in parts)

    return parts


def chunk_markdown(
        content: str,
        file_path: str,
        char_limit: int = 2000
) -> list[Chunk]:
    """Split Markdown content into searchable chunks."""

    blocks = parse_markdown(content)
    headings: list[tuple[int, str]] = []
    chunks: list[Chunk] = []

    for block in blocks:
        if block.type == "heading" and block.level is not None:
            update_heading_context(headings,
                                   block.level,
                                   content[block.start:block.end])

    return chunks

    
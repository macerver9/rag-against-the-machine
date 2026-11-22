from src.indexing.chunk import Chunk, MarkdownBlock
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


def find_cut_position(
        text: str,
        start: int,
        char_limit: int,
) -> int:
    """Find the best cut position within the caracter limit."""

    max_end = min(start + char_limit, len(text))

    if max_end == len(text):
        return max_end

    separators = ["\n\n", "\n", " "]

    for separator in separators:
        position = text.rfind(
            separator,
            start,
            max_end - len(separator) + 1
        )

        if position > start:
            return position + len(separator)

    return max_end


def build_search_text(
    headings: list[tuple[int, str]],
    text: str,
) -> str:
    """Add heading context to the chunk text."""
    context: list[str] = []

    for level, heading in headings:
        title = heading.splitlines()[0].strip()
        title = title.lstrip("#").strip()
        context.append(f"{'#' * level} {title}")

    if not context:
        return text

    return "\n".join(context) + "\n\n" + text


def chunk_markdown(
    content: str,
    file_path: str,
    char_limit: int = 2000,
) -> list[Chunk]:
    """Split Markdown content into searchable chunks."""

    blocks = parse_markdown(content)
    headings: list[tuple[int, str]] = []
    chunks: list[Chunk] = []

    current_start = 0
    current_end = 0

    for i, block in enumerate(blocks):
        next_block = blocks[i + 1] if i + 1 < len(blocks) else None
        if block.type == "heading" and block.level is not None:
            update_heading_context(
                headings,
                block.level,
                content[block.start:block.end],
            )

    return chunks
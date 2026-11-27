from src.indexing.chunk import Chunk
from src.indexing.markdown_parser import parse_markdown


def find_cut_position(
    text: str,
    start: int,
    char_limit: int,
) -> int:
    """Find a natural cut position within the character limit."""
    max_end = min(start + char_limit, len(text))

    if max_end == len(text):
        return max_end

    newline = text.rfind("\n", start, max_end)
    if newline > start:
        return newline + 1

    space = text.rfind(" ", start, max_end)
    if space > start:
        return space + 1

    return max_end


def chunk_markdown(
    content: str,
    file_path: str,
    char_limit: int = 2000,
) -> list[Chunk]:
    """Split Markdown into heading-based chunks."""
    if char_limit <= 0:
        raise ValueError("char_limit must be positive")

    blocks = parse_markdown(content)

    boundaries = [
        block.start
        for block in blocks
        if block.type == "heading"
    ]

    sections = [0, *boundaries, len(content)]
    chunks: list[Chunk] = []

    for section_start, section_end in zip(
        sections,
        sections[1:],
    ):
        position = section_start
        section = content[section_start:section_end]

        while position < section_end:
            relative_start = position - section_start

            relative_end = find_cut_position(
                section,
                relative_start,
                char_limit,
            )

            chunk_end = section_start + relative_end

            chunks.append(
                Chunk(
                    file_path=file_path,
                    start=position,
                    end=chunk_end,
                    text=content[position:chunk_end],
                )
            )

            position = chunk_end

    return chunks
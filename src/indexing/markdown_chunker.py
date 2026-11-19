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
) -> list[tuple[int, int]]:
    """Returns chunks thats match the size limit"""

    parts: list[tuple[int, int]] = []
    start = 0

    while start < len(text):
        end = find_split_position(text, start, char_limit)

        if end == start:
            break

        if end > start:
            parts.append((start, end))

        start = end

    assert "".join(text[part_start:part_end]
                   for part_start, part_end in parts) == text
    assert all(part_end - part_start <= char_limit
               for part_start, part_end in parts)

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

    current_end = 0
    current_start = 0

    for block in blocks:
        if block.type == "heading" and block.level is not None:
            update_heading_context(headings,
                                   block.level,
                                   content[block.start:block.end])

        block_size = block.end - block.start

        if block_size > char_limit:
            if current_end > current_start:
                chunk_text = content[current_start:current_end]

                chunks.append(
                    Chunk(
                        file_path=file_path,
                        start=current_start,
                        end=current_end,
                        text=chunk_text,
                        search_text=chunk_text,
                    )
                )
            parts = split_long_block(
                content[block.start:block.end],
                char_limit
            )

            for part_start, part_end in parts:
                absolute_start = block.start + part_start
                absolute_end = block.start + part_end

                chunk_text = content[absolute_start:absolute_end]

                chunks.append(
                    Chunk(
                        file_path=file_path,
                        start=absolute_start,
                        end=absolute_end,
                        text=chunk_text,
                        search_text=chunk_text,
                    )
                )
            current_start = block.end
            current_end = block.end
            continue

        new_size = block.end - current_start

        if new_size <= char_limit:
            current_end = block.end

        else:
            if current_end > current_start:
                chunk_text = content[current_start:current_end]

                chunks.append(
                    Chunk(
                        file_path=file_path,
                        start=current_start,
                        end=current_end,
                        text=chunk_text,
                        search_text=chunk_text,
                    )
                )
            current_start = block.start
            current_end = block.end

    if current_end > current_start:
        chunk_text = content[current_start:current_end]

        chunks.append(
            Chunk(
                file_path=file_path,
                start=current_start,
                end=current_end,
                text=chunk_text,
                search_text=chunk_text,
            )
        )

    return chunks

    
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


def chunk_region(
    content: str,
    file_path: str,
    start: int,
    end: int,
    char_limit: int,
    headings: list[tuple[int, str]],
) -> list[Chunk]:
    """Split a text region into chunks."""
    region_text = content[start:end]
    chunks: list[Chunk] = []
    cursor = 0

    while cursor < len(region_text):
        cut = find_cut_position(
            region_text,
            cursor,
            char_limit,
        )

        chunk_text = region_text[cursor:cut]

        absolute_start = start + cursor
        absolute_end = start + cut

        chunks.append(
            Chunk(
                file_path=file_path,
                start=absolute_start,
                end=absolute_end,
                text=chunk_text,
                search_text=build_search_text(
                    headings,
                    chunk_text,
                ),
            )
        )

        cursor = cut

    return chunks


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

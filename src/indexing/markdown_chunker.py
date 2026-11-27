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
    """Find the best cut position within the character limit."""
    max_end = min(start + char_limit, len(text))

    if max_end == len(text):
        return max_end

    separators = ["\n\n", "\n", " "]

    for separator in separators:
        position = text.rfind(separator, start, max_end)

        if position != -1:
            cut = position + len(separator)

            if cut <= max_end:
                return cut

    return max_end


def merge_chunks(
    chunks: list[Chunk],
    char_limit: int,
) -> list[Chunk]:
    """Merge consecutive small chunks when possible."""
    merged: list[Chunk] = []

    for chunk in chunks:
        if not merged:
            merged.append(chunk)
            continue

        previous = merged[-1]

        combined_size = len(previous.text) + len(chunk.text)

        is_small = (
            len(previous.text) < char_limit // 2
            or len(chunk.text) < char_limit // 2
        )

        if (
            is_small
            and combined_size <= char_limit
            and previous.end == chunk.start
        ):
            merged[-1] = Chunk(
                file_path=previous.file_path,
                start=previous.start,
                end=chunk.end,
                text=previous.text + chunk.text,
                search_text=previous.search_text + chunk.text,
            )
        else:
            merged.append(chunk)

    return merged


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


def create_chunk(
    content: str,
    file_path: str,
    start: int,
    end: int,
    headings: list[tuple[int, str]],
) -> Chunk:
    """Create a chunk from a content range."""
    text = content[start:end]

    return Chunk(
        file_path=file_path,
        start=start,
        end=end,
        text=text,
        search_text=build_search_text(headings, text),
    )


def get_headings_at_position(
    blocks: list,
    position: int,
) -> list[tuple[int, str]]:
    """Get the heading context at a document position."""
    headings: list[tuple[int, str]] = []

    for block in blocks:
        if block.start >= position:
            break

        if block.type == "heading" and block.level is not None:
            update_heading_context(
                headings,
                block.level,
                block.text,
            )

    return headings


def chunk_markdown(
    content: str,
    file_path: str,
    char_limit: int = 2000,
) -> list[Chunk]:
    """Split Markdown content into searchable chunks."""
    blocks = parse_markdown(content)

    chunks: list[Chunk] = []
    current_start = 0

    while current_start < len(content):
        current_end = find_cut_position(
            content,
            current_start,
            char_limit,
        )

        headings = get_headings_at_position(
            blocks,
            current_start,
        )

        chunks.append(
            create_chunk(
                content,
                file_path,
                current_start,
                current_end,
                headings,
            )
        )

        current_start = current_end

    return merge_chunks(chunks, char_limit)
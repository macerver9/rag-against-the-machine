import re
from src.indexing.chunk import Chunk


def update_heading_context(
    headings: list[tuple[int, str]],
    level: int,
    heading: str,
) -> None:
    """Update the heading hierarchy with a new heading."""

    while headings and headings[-1][0] >= level:
        headings.pop()

    headings.append((level, heading))


def split_long_paragraph(para: str, char_limit: int) -> list[str]:
    """Split a long paragraph into a sections with a max limit of characters"""

    chunks: list[str] = []
    start = 0

    while start < len(para):
        end = min(start + char_limit, len(para))

        if end < len(para):
            space = para.rfind(" ", start, end)

            if space > start:
                end = space

        chunks.append(para[start:end])
        start = end

    return chunks


def split_section_into_chunks(
    content: str,
    char_limit: int = 2000,
) -> list[str]:
    """Split a section into chunks with a maximum character limit."""

    chunks: list[str] = []
    paragraphs = re.finditer(r"\n\n+", content)
    start = 0
    current_chunk = ""

    for match in paragraphs:
        end = match.start()
        separator_end = match.end()
        paragraph = content[start:end]
        separator = content[end:separator_end]

        if len(current_chunk) + len(paragraph) + len(separator) <= char_limit:
            current_chunk += paragraph + separator

        else:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            if len(paragraph) > char_limit:
                chunks.extend(split_long_paragraph(paragraph, char_limit))
            else:
                current_chunk = paragraph

            if len(current_chunk) + len(separator) <= char_limit:
                current_chunk += separator
            else:
                chunks.append(current_chunk)
                current_chunk = separator

        start = separator_end

    remaining = content[start:]

    if len(current_chunk) + len(remaining) <= char_limit:
        current_chunk += remaining
    else:
        if current_chunk:
            chunks.append(current_chunk)

        if len(remaining) > char_limit:
            chunks.extend(split_long_paragraph(remaining, char_limit))
        else:
            current_chunk = remaining

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def chunk_markdown(content: str, file_path: str, char_limit: int = 2000) -> list[Chunk]:
    """Split Markdown content into chunks."""

    sections: list[str] = split_markdown_sections(content)
    chunks: list[str] = []

    for section in sections:
        section_chunks = split_section_into_chunks(section, char_limit)
        chunks.extend(section_chunks)

    return chunks

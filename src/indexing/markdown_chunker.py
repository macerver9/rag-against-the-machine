import re


def split_markdown_sections(content: str) -> list[str]:
    """Split Markdown content into sections using headings."""

    matches = re.finditer(r"^#{1,6}\s", content, re.MULTILINE)
    positions = [match.start() for match in matches]

    if not positions:
        return [content] if content else []

    sections: list[str] = []

    if positions[0] > 0:
        sections.append(content[:positions[0]])

    for i, start in enumerate(positions):
        if i + 1 < len(positions):
            end = positions[i + 1]
        else:
            end = len(content)

        sections.append(content[start:end])

    return sections


def split_long_paragraph(para: str, char_limit: int) -> list[str]:
    """Split a long paragraph into a sections with a max limit of characters"""

    chunks: list[str] = []

    for i in range(0, len(para), char_limit):
        chunks.append(para[i:i + char_limit])

    return chunks


def split_section_into_chunks(
        content: str,
        char_limit: int = 2000) -> list[str]:
    """Split a section into a chunk with a max limit of characters"""

    chunks: list[str] = []
    current_chunk: str = ""

    for para in content.split("\n\n"):
        if len(para) > char_limit:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = ""
            chunks.extend(split_long_paragraph(para, char_limit))

        elif not current_chunk and len(para) <= char_limit:
            current_chunk = para

        elif len(current_chunk) + len(para) + len("\n\n") <= char_limit:
            current_chunk = current_chunk + "\n\n" + para

        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = para

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def chunk_markdown(content: str, char_limit: int = 2000) -> list[str]:
    """Split Markdown content into chunks."""

    sections: list[str] = split_markdown_sections(content)
    chunks: list[str] = []

    for section in sections:
        section_chunks = split_section_into_chunks(section, char_limit)
        chunks.extend(section_chunks)

    return chunks

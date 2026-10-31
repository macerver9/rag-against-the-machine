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


def chunk_markdown(content: str, char_limit: int = 2000) -> list[str]:
    """Split Markdown content into chunks."""

    sections: list[str] = split_markdown_sections(content)
    chunks: list[str] = []

    for section in sections:
        section_chunks = split_section_into_chunks(section, char_limit)
        chunks.extend(section_chunks)

    return chunks
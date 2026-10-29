import re


def split_markdown_sections(content: str) -> list[str]:
    """Split Markdown content into sections using headings."""

    sections: list[str] = []
    current_section: list[str] = []

    for line in content.splitlines():
        if re.match(r"^#{1,6}\s", line):
            if current_section:
                sections.append("\n".join(current_section).strip())
            current_section = [line]
        else:
            current_section.append(line)

    if current_section:
        sections.append("\n".join(current_section).strip())

    return [section for section in sections if sections]


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

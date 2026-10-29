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


def split_section_into_chunks(content: str, char_limit: int = 2000) -> list[str]:
    """Split a section into a chunk with a max limit of characters"""

    chunks: list[str] = []
    current_chunk: str = ""

    for para in content.split("\n\n"):
        if (len(current_chunk) < char_limit and
            (char_limit - len(current_chunk) > len(para))):
            current_chunk.append(para)
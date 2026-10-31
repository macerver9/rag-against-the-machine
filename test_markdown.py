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


if __name__ == "__main__":
    text = "Este es un párrafo de ejemplo que queremos dividir."
    chunks = split_long_paragraph(text, 20)

    for chunk in chunks:
        print(repr(chunk), len(chunk))

    print("Contenido conservado:", "".join(chunks) == text)
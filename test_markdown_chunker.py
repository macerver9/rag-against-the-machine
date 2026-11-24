from src.indexing.markdown_chunker import chunk_markdown


def print_chunks(chunks: list) -> None:
    """Print chunks to inspect their contents."""
    for i, chunk in enumerate(chunks):
        print(f"\n{'=' * 20} CHUNK {i} {'=' * 20}")
        print(f"File: {chunk.file_path}")
        print(f"Offsets: {chunk.start} -> {chunk.end}")
        print(f"Length: {len(chunk.text)}")

        print("\n--- TEXT ---")
        print(chunk.text)

        print("\n--- SEARCH TEXT ---")
        print(chunk.search_text)


def test_short_markdown() -> None:
    content = "# Title\n\nSome content.\n\n## Section\n\nMore content."

    chunks = chunk_markdown(content, "test.md", 1000)

    assert len(chunks) == 1
    assert chunks[0].text == content
    assert "# Title" in chunks[0].search_text
    assert "## Section" in chunks[0].search_text


def test_chunk_limit() -> None:
    content = "This is a long paragraph that must be split into chunks."

    chunks = chunk_markdown(content, "test.md", 15)

    assert all(len(chunk.text) <= 15 for chunk in chunks)
    assert "".join(chunk.text for chunk in chunks) == content


def test_offsets() -> None:
    content = "# Title\n\nFirst paragraph.\n\nSecond paragraph."

    chunks = chunk_markdown(content, "test.md", 15)

    for chunk in chunks:
        assert chunk.text == content[chunk.start:chunk.end]

    assert chunks[0].start == 0
    assert chunks[-1].end == len(content)

    for previous, current in zip(chunks, chunks[1:]):
        assert previous.end == current.start


def test_heading_context() -> None:
    content = (
        "# Main\n\n"
        "Some long content that will be split into several chunks.\n\n"
        "## Subsection\n\n"
        "More content here."
    )

    chunks = chunk_markdown(content, "test.md", 20)

    assert all("# Main" in chunk.search_text for chunk in chunks)

    subsection_chunks = [
        chunk for chunk in chunks
        if "## Subsection" in chunk.text
        or "More content here." in chunk.text
    ]

    assert all(
        "## Subsection" in chunk.search_text
        for chunk in subsection_chunks
    )


if __name__ == "__main__":
    content = (
        "# RAG Project\n\n"
        "This is the introduction to the project.\n\n"
        "## Architecture\n\n"
        "The project uses a modular architecture.\n"
        "Each module has a specific responsibility.\n\n"
        "### Chunking\n\n"
        "Markdown content is split into smaller chunks.\n"
        "Each chunk contains contextual information.\n\n"
        "## Search\n\n"
        "Search uses the contextual text to improve retrieval."
    )

    chunks = chunk_markdown(
        content,
        "README.md",
        char_limit=100,
    )

    print_chunks(chunks)
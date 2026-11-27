from src.indexing.markdown_chunker import chunk_markdown
from pathlib import Path

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
    file_path = Path(
        "data/raw/vllm-0.10.1/docs/design/arch_overview.md"
    )

    content = file_path.read_text(encoding="utf-8")

    chunks = chunk_markdown(
        content,
        str(file_path),
        char_limit=2000,
    )

    print(f"File size: {len(content)} characters")
    print(f"Total chunks: {len(chunks)}")

    print_chunks(chunks)
    
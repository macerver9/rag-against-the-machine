from pathlib import Path

from src.indexing.markdown_chunker import chunk_markdown


def test_chunk_markdown() -> None:
    file_path = Path(
        "data/raw/vllm-0.10.1/docs/design/arch_overview.md"
    )

    content = file_path.read_text(encoding="utf-8")
    char_limit = 2000

    chunks = chunk_markdown(
        content,
        str(file_path),
        char_limit,
    )

    assert chunks
    assert all(len(chunk.text) <= char_limit for chunk in chunks)
    assert chunks[0].start == 0
    assert chunks[-1].end == len(content)

    for previous, current in zip(chunks, chunks[1:]):
        assert previous.end == current.start

    assert "".join(chunk.text for chunk in chunks) == content

    print(f"Original: {len(content)} characters")
    print(f"Chunks: {len(chunks)}")
    print(f"Maximum size: {max(len(chunk.text) for chunk in chunks)}")

    for index, chunk in enumerate(chunks):
        print("\n" + "=" * 80)
        print(f"CHUNK {index}")
        print(f"Offsets: {chunk.start}-{chunk.end}")
        print(f"Size: {len(chunk.text)} characters")
        print("=" * 80)
        print(chunk.text)
        print("=" * 80)

    print("\nAll tests passed.")


if __name__ == "__main__":
    test_chunk_markdown()
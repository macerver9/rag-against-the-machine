from pathlib import Path

from src.indexing.markdown_chunker import chunk_markdown, parse_markdown


def main() -> None:
    raw_path = Path("data/raw")

    file_path = raw_path / "vllm-0.10.1" / "CODE_OF_CONDUCT.md"

    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    content = file_path.read_text(encoding="utf-8")

    chunks = chunk_markdown(
        content,
        str(file_path),
        char_limit=500,
    )
    blocks = parse_markdown(content)

    for block in blocks:
        print(
            f"type={block.type}, "
            f"start={block.start}, "
            f"end={block.end}, "
            f"size={block.end - block.start}, "
            f"text={content[block.start:block.end]!r}"
        )

    print(f"File: {file_path}")
    print(f"Original size: {len(content)} characters")
    print(f"Chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks):
        print("\n" + "=" * 60)
        print(f"CHUNK {index + 1}/{len(chunks)}")
        print(f"Offsets: {chunk.start} -> {chunk.end}")
        print(f"Size: {len(chunk.text)} characters")
        print("=" * 60)

        print(chunk.text)


if __name__ == "__main__":
    main()
from pathlib import Path

from src.indexing.markdown_parser import parse_markdown


if __name__ == "__main__":
    file_path = Path(
        "data/raw/vllm-0.10.1/docs/design/arch_overview.md"
    )

    content = file_path.read_text(encoding="utf-8")
    blocks = parse_markdown(content)

    print(f"File size: {len(content)} characters")
    print(f"Total blocks: {len(blocks)}")

    for block in blocks:
        original = content[block.start:block.end]

        print(
            block.type,
            block.level,
            block.start,
            block.end,
            repr(original[:100]),
        )

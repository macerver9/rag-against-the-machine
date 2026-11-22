from src.indexing.markdown_parser import parse_markdown
import textwrap


if __name__ == "__main__":
    content = """```markdown
# Esto no es un heading
```

# Esto sí es un heading
    """
    blocks = parse_markdown(content)

    assert blocks[0].start == 0

    for previous, current in zip(blocks, blocks[1:]):
        assert previous.end == current.start

    assert blocks[-1].end == len(content)

    for block in blocks:
        original = content[block.start:block.end]

        assert len(original) == block.end - block.start

        print(block.type, block.level, repr(original))
    
    assert blocks[0].start == 0

    for previous, current in zip(blocks, blocks[1:]):
        assert previous.end == current.start

    assert blocks[-1].end == len(content)

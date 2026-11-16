from src.indexing.markdown_parser import parse_markdown
import textwrap


if __name__ == "__main__":
    content = """```markdown
# Esto no es un heading
```

# Esto sí es un heading
    """
    blocks = parse_markdown(content)

    for block in blocks:
        original = content[block.start:block.end]

        assert len(original) == block.end - block.start

        print(block.type, block.level, repr(original))

from pathlib import Path

from src.indexing.markdown_parser import find_markdown_headings


def test_markdown_headings() -> None:
    content = "# Instalación\n\n## Linux\n\n### Ubuntu\n"

    headings = find_markdown_headings(content)

    assert len(headings) == 3

    expected = [
        (1, "# Instalación\n"),
        (2, "## Linux\n"),
        (3, "### Ubuntu\n"),
    ]

    for heading, (level, text) in zip(headings, expected):
        assert heading.type == "heading"
        assert heading.level == level
        assert content[heading.start:heading.end] == text


def test_headings_ignore_code_blocks() -> None:
    content = """\
# Instalación

```python
# Esto no debe detectarse
def main():
    pass
```

## Linux

~~~
# Tampoco debe detectarse
~~~

### Ubuntu
"""

    headings = find_markdown_headings(content)

    assert len(headings) == 3

    expected = ["# Instalación", "## Linux", "### Ubuntu"]

    for heading, title in zip(headings, expected):
        assert content[heading.start:heading.end].strip() == title


def test_real_markdown_file() -> None:
    file_path = Path(
        "data/raw/vllm-0.10.1/docs/models/supported_models.md"
    )
    content = file_path.read_text(encoding="utf-8")

    headings = find_markdown_headings(content)

    assert len(headings) == 30


def test_setext_headings() -> None:
    content = """\
Título principal
================

Subtítulo
---------

Texto normal

----------------
"""

    headings = find_markdown_headings(content)

    assert len(headings) == 2

    expected = [
        (1, "Título principal\n================\n"),
        (2, "Subtítulo\n---------\n"),
    ]

    for heading, (level, text) in zip(headings, expected):
        assert heading.level == level
        assert content[heading.start:heading.end] == text


if __name__ == "__main__":
    test_markdown_headings()
    test_headings_ignore_code_blocks()
    test_real_markdown_file()
    test_setext_headings()
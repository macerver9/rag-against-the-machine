from src.indexing.markdown_parser import find_markdown_headings


def test_markdown_headings() -> None:
    content = "# Instalación\n\n## Linux\n\n### Ubuntu\n"

    headings = find_markdown_headings(content)

    assert len(headings) == 3

    assert headings[0].type == "heading"
    assert headings[0].level == 1
    assert content[headings[0].start:headings[0].end] == "# Instalación\n"

    assert headings[1].level == 2
    assert content[headings[1].start:headings[1].end] == "## Linux\n"

    assert headings[2].level == 3
    assert content[headings[2].start:headings[2].end] == "### Ubuntu\n"


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

    assert headings[0].level == 1
    assert headings[1].level == 2
    assert headings[2].level == 3

    expected = [
        "# Instalación",
        "## Linux",
        "### Ubuntu",
    ]

    for heading, title in zip(headings, expected):
        assert content[heading.start:heading.end].strip() == title


if __name__ == "__main__":
    test_markdown_headings()
    test_headings_ignore_code_blocks()
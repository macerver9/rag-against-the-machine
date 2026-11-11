from src.indexing.markdown_parser_utils import iter_lines


def test_iter_lines() -> None:
    content = """\
# Installation

```python
# Esto no debe aparecer
print("Hello")
```

Some text.
"""
    result = list(iter_lines(content))

    assert [line[0] for line in result] == [0, 1, 6, 7]


if __name__ == "__main__":
    test_iter_lines()
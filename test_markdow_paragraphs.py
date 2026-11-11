from src.indexing.markdown_parser import find_markdown_paragraphs


def test_markdown_paragraphs() -> None:
    content = """\
Este es un párrafo.
Continúa en otra línea.

Este es otro párrafo.

Y este es el tercero.
"""

    paragraphs = find_markdown_paragraphs(content)

    assert len(paragraphs) == 3
    assert all(p.type == "paragraph" for p in paragraphs)


if __name__ == "__main__":
    test_markdown_paragraphs()
from src.indexing.markdown_chunker import find_cut_position, build_search_text


""" def test_paragraph_cut() -> None:
    text = "uno dos tres\n\ncuatro cinco seis"
    result = find_cut_position(text, 0, 14)

    assert result == 14


def test_line_cut() -> None:
    text = "alpha beta\ngamma delta"
    result = find_cut_position(text, 0, 12)

    assert result == 11


def test_word_cut() -> None:
    text = "abcdefgh ijklmnop"
    result = find_cut_position(text, 0, 10)

    assert result == 9


def test_forced_cut() -> None:
    text = "abcdefghijk"
    result = find_cut_position(text, 0, 5)

    assert result == 5


def test_end_of_text() -> None:
    text = "abc"
    result = find_cut_position(text, 0, 5)

    assert result == 3 """

def test_build_search_text():
    headings = [
        (1, "# Instalación"),
        (2, "## Linux"),
        (3, "### Dependencias"),
    ]

    text = "Instala las dependencias con pip."

    result = build_search_text(headings, text)

    expected = (
        "# Instalación\n"
        "## Linux\n"
        "### Dependencias\n\n"
        "Instala las dependencias con pip."
    )

    assert result == expected
from src.indexing.markdown_parser_utils import get_line_offsets


def test_line_offsets() -> None:
    lines = ["# Título\n", "\n", "Hola mundo\n"]

    assert get_line_offsets(lines) == [0, 9, 10]


if __name__ == "__main__":
    test_line_offsets()
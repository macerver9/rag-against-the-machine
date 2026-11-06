from src.indexing.markdown_parser_utils import get_setext_heading_level


def test_setext_heading_level() -> None:
    assert get_setext_heading_level("==========") == 1
    assert get_setext_heading_level("----------") == 2
    assert get_setext_heading_level("   ======") == 1
    assert get_setext_heading_level("   ------") == 2
    assert get_setext_heading_level("Texto normal") is None
    assert get_setext_heading_level("--- texto") is None


if __name__ == "__main__":
    test_setext_heading_level()
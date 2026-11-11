from src.indexing.markdown_parser_utils import get_setext_heading_level


def main() -> None:
    print(get_setext_heading_level("================"))
    print(get_setext_heading_level("----------------"))


if __name__ == "__main__":
    main()
    print(repr(get_setext_heading_level("================\n")))
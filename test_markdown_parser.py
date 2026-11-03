from pathlib import Path

from src.indexing.markdown_parser import (
    find_markdown_tables,
    is_table_separator,
    get_code_fence,
    is_code_fence_end,
)


def main() -> None:
    file_path = Path("data/raw/vllm-0.10.1/RELEASE.md")
    content = file_path.read_text(encoding="utf-8")

    tables = find_markdown_tables(content)

    print(f"Tablas encontradas: {len(tables)}")

    for start, end in tables:
        print(f"\nPosiciones: {start} - {end}")
        print(content[start:end])

    test_content = """
```text
| Nombre | Edad |
| --- | --- |
| Ana | 25 |
```

| Nombre | Edad |
| --- | --- |
| Luis | 30 |
"""

    test_fence_content = """\
````python
| Nombre | Edad |
| --- | --- |
| Ana | 25 |
```
| Luis | 30 |
````
| Pedro | 40 |
| --- | --- |
| Marta | 35 |
"""

    fence_tables = find_markdown_tables(test_fence_content)

    print(f"\nTablas con delimitadores: {len(fence_tables)}")

    for start, end in fence_tables:
        print(test_fence_content[start:end])

    test_tables = find_markdown_tables(test_content)

    print(f"\nTablas de prueba: {len(test_tables)}")

    for start, end in test_tables:
        print(test_content[start:end])


if __name__ == "__main__":
    main()
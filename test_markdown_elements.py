from pathlib import Path
import re

CORPUS = Path("data/raw/vllm-0.10.1")


def inspect_tables() -> None:
    for file in CORPUS.rglob("*.md"):
        content = file.read_text(encoding="utf-8")

        if re.search(r"(?m)^\s*\|.*\|\s*$", content):
            print(f"\n--- {file} ---")

            for match in re.finditer(
                r"(?m)^\s*\|.*\|\s*$",
                content
            ):
                start = max(0, match.start() - 100)
                end = min(len(content), match.end() + 300)

                print(content[start:end])
                print("-" * 50)
                break


if __name__ == "__main__":
    inspect_tables()
from pathlib import Path

from src.indexing.markdown_chunker import (
    chunk_markdown,
    split_markdown_sections,
    split_section_into_chunks,
)


file_path = "data/raw/vllm-0.10.1/docs/configuration/serve_args.md"
content = Path(file_path).read_text(encoding="utf-8")

sections = split_markdown_sections(content)

section_chunks = []
for section in sections:
    section_chunks.extend(split_section_into_chunks(section))

chunks = chunk_markdown(content)

print("Original:", len(content))
print("Secciones:", sum(len(section) for section in sections))
print("Chunks de las secciones:", sum(len(chunk) for chunk in section_chunks))
print("Chunks finales:", sum(len(chunk) for chunk in chunks))

print("\nSaltos de línea:")
print("Original:", content.count("\n"))
print("Secciones:", sum(section.count("\n") for section in sections))
print("Chunks:", sum(chunk.count("\n") for chunk in chunks))

print("\nComparación de contenido:")
print("Original == secciones:", content == "\n".join(sections))
print("Original == chunks:", content == "".join(chunks))

for index, section in enumerate(sections, start=1):
    print(f"\n--- Sección {index} ---")
    print(repr(section[:100]))

for index, section in enumerate(sections, start=1):
    print(f"\nSección {index}")
    print("Caracteres:", len(section))
    print("Saltos de línea:", section.count("\n"))
    print("Final:", repr(section[-30:]))
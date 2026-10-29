from src.indexing.markdown_chunker import split_markdown_sections


content = """Introducción al proyecto.

# Instalación

Instala las dependencias.

## Configuración

Configura el entorno.
"""

sections = split_markdown_sections(content)

for index, section in enumerate(sections, start=1):
    print(f"--- Sección {index} ---")
    print(section)
from dataclasses import dataclass


@dataclass
class Chunk:
    """Represent a document chunk and its original content."""

    file_path: str
    start: int
    end: int
    text: str
    search_text: str

    def __post_init__(self) -> None:
        if self.start < 0 or self.end <= self.start:
            raise ValueError("Invalid chunk offsets")


@dataclass
class MarkdownBlock:
    """Represent a Markdown block and its position in the document."""

    type: str
    start: int
    end: int
    level: int | None = None

    def __post_init__(self) -> None:
        if self.start < 0 or self.end <= self.start:
            raise ValueError("Invalid Markdown block offsets")

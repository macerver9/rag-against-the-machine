from dataclasses import dataclass


@dataclass
class MarckdownBlock:
    """Represent a Marckdown block and its position in the document."""

    type: str
    start: int
    end: int
    level: int | None = None

import uuid
from pydantic import BaseModel, Field


class MinimalSource(BaseModel):
    """Represent a source location within a corpus file."""

    file_path: str
    first_character_index: int
    last_character_index: int


class UnansweredQuestion(BaseModel):
    """Represent a question that has not been answered yet."""

    question_id: str = Field(
        default_factory=lambda: str(uuid.uuid4())
    )
    question: str
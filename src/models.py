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


class AnsweredQuestion(UnansweredQuestion):
    """Represent a question with its answer and supporting sources."""

    sources: list[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    """Represent a dataset containing RAG questions."""

    rag_questions: list[AnsweredQuestion | UnansweredQuestion]


class MinimalSearchResults(BaseModel):
    """Represent search results for a single question."""

    question_id: str
    question: str
    retrieved_sources: list[MinimalSource]


class MinimalAnswer(MinimalSearchResults):
    """Represent search results together with a generated answer."""

    answer: str


class StudentSearchResults(BaseModel):
    """Represent search results for a dataset of questions."""

    search_result: list[MinimalSearchResults]
    k: int


class StudentSearchResultsAndAnswer(BaseModel):
    """Represent search results and generated answes for a dataset."""

    search_result: list[MinimalAnswer]
    k: int
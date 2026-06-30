"""Persistence ports for documents, chunks, answers, jobs, and evaluation records."""

from typing import Protocol

from app.domain.models.answer import Answer
from app.domain.models.chunk import DocumentChunk
from app.domain.models.document import Document
from app.domain.models.evaluation import EvaluationQuestion, EvaluationResult
from app.domain.models.job import Job


class DocumentRepository(Protocol):
    """Stores uploaded report metadata."""

    def save_document(self, document: Document) -> Document:
        """Persist a new or updated document record."""
        ...

    def get_document(self, document_id: str) -> Document | None:
        """Load a document by id."""
        ...

    def list_documents(self) -> list[Document]:
        """Return all stored documents."""
        ...

    def delete_document(self, document_id: str) -> None:
        """Remove a document record."""
        ...


class ChunkRepository(Protocol):
    """Stores indexed chunks for retrieval and audit."""

    def save_chunks(self, chunks: list[DocumentChunk]) -> None:
        """Persist chunks for one or more documents."""
        ...

    def get_chunks_by_document(self, document_id: str) -> list[DocumentChunk]:
        """Load indexed chunks for a document."""
        ...


class AnswerRepository(Protocol):
    """Stores generated answers for audit and history."""

    def save_answer(self, answer_id: str, answer: Answer) -> None:
        """Persist an answer keyed by a stable identifier."""
        ...

    def get_answer(self, answer_id: str) -> Answer | None:
        """Load a stored answer by id."""
        ...


class JobRepository(Protocol):
    """Stores background job lifecycle records."""

    def save_job(self, job: Job) -> Job:
        """Persist a new or updated job."""
        ...

    def get_job(self, job_id: str) -> Job | None:
        """Load a job by id."""
        ...

    def update_job(self, job: Job) -> Job:
        """Persist job status or metadata changes."""
        ...


class EvaluationRepository(Protocol):
    """Stores golden-set questions and evaluation outcomes."""

    def list_questions(self) -> list[EvaluationQuestion]:
        """Return configured golden-set questions."""
        ...

    def save_evaluation_result(self, result: EvaluationResult) -> None:
        """Persist the outcome of one evaluated question."""
        ...

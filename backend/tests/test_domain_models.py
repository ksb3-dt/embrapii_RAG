from datetime import UTC, datetime

import pytest

from app.domain.models.answer import Answer, ConfidenceLevel
from app.domain.models.chunk import (
    ChunkType,
    Citation,
    DocumentChunk,
    EvidenceChunk,
    RetrievalSource,
)
from app.domain.models.document import Document, DocumentPage, DocumentStatus
from app.domain.models.evaluation import (
    EvaluationQuestion,
    EvaluationResult,
    EvaluationStatus,
)
from app.domain.models.job import Job, JobStatus, JobType


def test_document_carries_identity_and_status() -> None:
    created = datetime(2026, 6, 30, 12, 0, tzinfo=UTC)
    document = Document(
        id="doc-1",
        filename="relatorio.pdf",
        source_path="data/documents/relatorio.pdf",
        status=DocumentStatus.INDEXED,
        title="Relatório EMBRAPII",
        created_at=created,
    )

    assert document.id == "doc-1"
    assert document.title == "Relatório EMBRAPII"
    assert document.status is DocumentStatus.INDEXED
    assert document.created_at == created


def test_document_page_uses_one_based_page_numbers() -> None:
    page = DocumentPage(document_id="doc-1", page_number=1, text="Conteúdo da página.")

    assert page.page_number == 1
    assert page.text == "Conteúdo da página."


def test_document_page_rejects_zero_based_page_numbers() -> None:
    with pytest.raises(ValueError, match="1-based"):
        DocumentPage(document_id="doc-1", page_number=0, text="inválido")


def test_document_chunk_carries_citation_metadata() -> None:
    chunk = DocumentChunk(
        document_id="doc-1",
        chunk_id="chunk-1",
        page_number=3,
        text="Investimento total de R$ 1,2 milhão.",
        chunk_type=ChunkType.TEXT,
        section_title="Resultados",
        source_file_path="data/documents/relatorio.pdf",
    )

    assert chunk.chunk_type is ChunkType.TEXT
    assert chunk.page_number == 3
    assert chunk.section_title == "Resultados"


def test_citation_requires_document_reference_and_page() -> None:
    citation = Citation(
        document_id="doc-1",
        document_title="Relatório EMBRAPII",
        page_number=5,
    )

    assert citation.document_id == "doc-1"
    assert citation.document_title == "Relatório EMBRAPII"
    assert citation.page_number == 5


def test_evidence_chunk_stores_retrieval_metadata() -> None:
    citation = Citation(document_id="doc-1", document_title="Relatório", page_number=2)
    evidence = EvidenceChunk(
        chunk_id="chunk-2",
        document_id="doc-1",
        document_title="Relatório",
        page_number=2,
        text="Projetos concluídos: 12.",
        retrieval_source=RetrievalSource.FUSION,
        rank=1,
        score=0.82,
        citation=citation,
        chunk_type=ChunkType.TABLE,
    )

    assert evidence.retrieval_source is RetrievalSource.FUSION
    assert evidence.rank == 1
    assert evidence.score == 0.82
    assert evidence.citation.page_number == 2


def test_answer_carries_confidence_and_not_found_flags() -> None:
    answer = Answer(
        text="Não foi possível localizar essa informação nos relatórios indexados.",
        confidence_level=ConfidenceLevel.NOT_FOUND,
        is_not_found=True,
        is_low_confidence=False,
    )

    assert answer.is_not_found is True
    assert answer.confidence_level is ConfidenceLevel.NOT_FOUND
    assert answer.citations == ()
    assert answer.evidence == ()


def test_job_represents_background_work_without_queue_coupling() -> None:
    job = Job(
        id="job-1",
        job_type=JobType.INGEST_DOCUMENT,
        status=JobStatus.QUEUED,
        document_id="doc-1",
    )

    assert job.job_type is JobType.INGEST_DOCUMENT
    assert job.status is JobStatus.QUEUED
    assert job.document_id == "doc-1"


def test_evaluation_models_capture_golden_set_records() -> None:
    question = EvaluationQuestion(
        id="q-1",
        question_text="Quantos projetos foram concluídos?",
        expected_document_ids=("doc-1",),
        tags=("kpi",),
    )
    result = EvaluationResult(
        question_id=question.id,
        answer_text="12 projetos.",
        status=EvaluationStatus.COMPLETED,
        passed=None,
        notes="Scoring not implemented in milestone 02b.",
    )

    assert question.expected_document_ids == ("doc-1",)
    assert result.passed is None
    assert result.status is EvaluationStatus.COMPLETED

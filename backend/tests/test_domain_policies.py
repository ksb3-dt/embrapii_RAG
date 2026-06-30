from app.domain.models.answer import ConfidenceLevel
from app.domain.models.chunk import Citation, EvidenceChunk, RetrievalSource
from app.domain.policies.citation_policy import CitationPolicy, ClaimType
from app.domain.policies.confidence_policy import ConfidencePolicy


def _evidence(score: float | None) -> EvidenceChunk:
    citation = Citation(document_id="doc-1", document_title="Relatório", page_number=1)
    return EvidenceChunk(
        chunk_id="chunk-1",
        document_id="doc-1",
        document_title="Relatório",
        page_number=1,
        text="Evidência de exemplo.",
        retrieval_source=RetrievalSource.DENSE,
        score=score,
        rank=1,
        citation=citation,
    )


def test_confidence_policy_marks_empty_evidence_as_not_found() -> None:
    assessment = ConfidencePolicy().assess([])

    assert assessment.level is ConfidenceLevel.NOT_FOUND
    assert assessment.is_not_found is True
    assert assessment.is_low_confidence is False


def test_confidence_policy_marks_weak_scores_as_not_found() -> None:
    assessment = ConfidencePolicy().assess([_evidence(0.1), _evidence(0.2)])

    assert assessment.level is ConfidenceLevel.NOT_FOUND
    assert assessment.is_not_found is True


def test_confidence_policy_marks_limited_evidence_as_low_confidence() -> None:
    assessment = ConfidencePolicy().assess([_evidence(0.45)])

    assert assessment.level is ConfidenceLevel.LOW
    assert assessment.is_low_confidence is True
    assert assessment.is_not_found is False


def test_confidence_policy_marks_strong_evidence_as_high() -> None:
    assessment = ConfidencePolicy().assess([_evidence(0.9), _evidence(0.85)])

    assert assessment.level is ConfidenceLevel.HIGH
    assert assessment.is_not_found is False
    assert assessment.is_low_confidence is False


def test_citation_policy_detects_numbers_dates_programs_and_comparisons() -> None:
    policy = CitationPolicy()

    assert policy.classify_claim("Foram 120 projetos concluídos.") is ClaimType.NUMBER
    assert policy.classify_claim("Atualizado em 30/06/2026.") is ClaimType.DATE
    assert policy.classify_claim("O programa EMBRAPII apoiou a iniciativa.") is (
        ClaimType.NAMED_PROGRAM
    )
    assert policy.classify_claim("O resultado foi maior que no ano anterior.") is (
        ClaimType.COMPARISON
    )
    assert policy.classify_claim("Resumo executivo do relatório.") is ClaimType.GENERAL


def test_citation_policy_requires_citations_for_high_risk_claims() -> None:
    policy = CitationPolicy()

    assert policy.requires_citation("Investimento de R$ 2,5 milhões.") is True
    assert policy.requires_citation("Contexto geral do relatório.") is False

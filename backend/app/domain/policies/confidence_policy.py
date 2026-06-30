"""Deterministic rules for not-found and low-confidence answers."""

from dataclasses import dataclass

from app.domain.models.answer import ConfidenceLevel
from app.domain.models.chunk import EvidenceChunk


@dataclass(frozen=True)
class ConfidenceAssessment:
    """Result of applying confidence rules to retrieved evidence."""

    level: ConfidenceLevel
    is_not_found: bool
    is_low_confidence: bool
    reason: str


class ConfidencePolicy:
    """Conservative placeholder policy tuned later with the golden set."""

    def __init__(
        self,
        *,
        min_evidence_chunks: int = 1,
        min_mean_score: float = 0.35,
        low_confidence_mean_score: float = 0.55,
    ) -> None:
        self._min_evidence_chunks = min_evidence_chunks
        self._min_mean_score = min_mean_score
        self._low_confidence_mean_score = low_confidence_mean_score

    def assess(self, evidence: list[EvidenceChunk]) -> ConfidenceAssessment:
        """Classify evidence strength using simple deterministic thresholds."""
        if not evidence:
            return ConfidenceAssessment(
                level=ConfidenceLevel.NOT_FOUND,
                is_not_found=True,
                is_low_confidence=False,
                reason="no_evidence",
            )

        scored_values = [chunk.score for chunk in evidence if chunk.score is not None]
        if not scored_values:
            if len(evidence) < self._min_evidence_chunks:
                return ConfidenceAssessment(
                    level=ConfidenceLevel.LOW,
                    is_not_found=False,
                    is_low_confidence=True,
                    reason="insufficient_evidence_without_scores",
                )
            return ConfidenceAssessment(
                level=ConfidenceLevel.MEDIUM,
                is_not_found=False,
                is_low_confidence=False,
                reason="evidence_without_scores",
            )

        mean_score = sum(scored_values) / len(scored_values)
        if mean_score < self._min_mean_score:
            return ConfidenceAssessment(
                level=ConfidenceLevel.NOT_FOUND,
                is_not_found=True,
                is_low_confidence=False,
                reason="weak_mean_score",
            )

        if (
            len(evidence) < self._min_evidence_chunks
            or mean_score < self._low_confidence_mean_score
        ):
            return ConfidenceAssessment(
                level=ConfidenceLevel.LOW,
                is_not_found=False,
                is_low_confidence=True,
                reason="limited_or_weak_evidence",
            )

        if mean_score >= self._low_confidence_mean_score:
            return ConfidenceAssessment(
                level=ConfidenceLevel.HIGH,
                is_not_found=False,
                is_low_confidence=False,
                reason="strong_evidence",
            )

        return ConfidenceAssessment(
            level=ConfidenceLevel.MEDIUM,
            is_not_found=False,
            is_low_confidence=False,
            reason="moderate_evidence",
        )

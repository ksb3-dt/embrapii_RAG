"""Deterministic rules for when factual claims should cite report pages."""

import re
from enum import StrEnum


class ClaimType(StrEnum):
    """Categories of claims with different citation expectations."""

    NUMBER = "number"
    DATE = "date"
    NAMED_PROGRAM = "named_program"
    COMPARISON = "comparison"
    GENERAL = "general"


# Padrões conservadores; refinamento virá com o golden set.
_NUMBER_PATTERN = re.compile(r"\b\d{1,3}(?:\.\d{3})*(?:,\d+)?%?|\b\d+(?:[.,]\d+)?\b")
_DATE_PATTERN = re.compile(
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}-\d{2}-\d{2}\b",
    re.IGNORECASE,
)
_COMPARISON_PATTERN = re.compile(
    r"\b(?:maior|menor|comparad[oa]s?|versus|vs\.?|diferen[çc]a|"
    r"semelhante|similar|superior|inferior|aumentou|diminuiu|"
    r"cresceu|reduziu)\b",
    re.IGNORECASE,
)
_NAMED_PROGRAM_PATTERN = re.compile(
    r"\b(?:EMBRAPII|SEBRAE|BNDES|FINEP|CNPq|CAPES|CTI|"
    r"Programa\s+[A-ZÁÉÍÓÚÃÕÂÊÔÇ][\wÁÉÍÓÚÃÕÂÊÔÇáéíóúãõâêôç-]+)\b",
    re.IGNORECASE,
)

_CITATION_REQUIRED_TYPES = {
    ClaimType.NUMBER,
    ClaimType.DATE,
    ClaimType.NAMED_PROGRAM,
    ClaimType.COMPARISON,
}


class CitationPolicy:
    """Identifies claim types that should prefer page-level citations."""

    def classify_claim(self, claim_text: str) -> ClaimType:
        """Return the most specific claim category detected in the text."""
        normalized = claim_text.strip()
        if not normalized:
            return ClaimType.GENERAL

        if _COMPARISON_PATTERN.search(normalized):
            return ClaimType.COMPARISON
        if _NAMED_PROGRAM_PATTERN.search(normalized):
            return ClaimType.NAMED_PROGRAM
        if _DATE_PATTERN.search(normalized):
            return ClaimType.DATE
        if _NUMBER_PATTERN.search(normalized):
            return ClaimType.NUMBER
        return ClaimType.GENERAL

    def requires_citation(self, claim_text: str) -> bool:
        """Return True when the claim type should be backed by citations."""
        return self.classify_claim(claim_text) in _CITATION_REQUIRED_TYPES

"""Coordinates structured multi-report comparison generation."""

from app.application.exceptions import raise_not_implemented


class ReportComparisonService:
    """Application service for grounded report comparisons."""

    def compare_reports(
        self,
        document_ids: tuple[str, ...],
        *,
        provider: str,
        model: str,
        api_key: str,
    ) -> None:
        """Generate a structured comparison across indexed reports."""
        raise_not_implemented("Report comparisons are not implemented yet.")

"""Coordinates structured single-report summary generation."""

from app.application.exceptions import raise_not_implemented


class ReportSummaryService:
    """Application service for grounded report summaries."""

    def summarize_report(
        self,
        document_id: str,
        *,
        provider: str,
        model: str,
        api_key: str,
    ) -> None:
        """Generate a structured summary for one indexed report."""
        raise_not_implemented("Report summaries are not implemented yet.")

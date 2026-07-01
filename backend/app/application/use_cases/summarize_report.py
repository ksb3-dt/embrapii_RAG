"""Use case wrapper for report summaries."""

from app.application.services.report_summary_service import ReportSummaryService


class SummarizeReportUseCase:
    """Thin boundary for structured report summaries."""

    def __init__(self, report_summary_service: ReportSummaryService) -> None:
        self._report_summary_service = report_summary_service

    def execute(
        self,
        document_id: str,
        *,
        provider: str,
        model: str,
        api_key: str,
    ) -> None:
        """Generate a structured summary for one report."""
        return self._report_summary_service.summarize_report(
            document_id,
            provider=provider,
            model=model,
            api_key=api_key,
        )

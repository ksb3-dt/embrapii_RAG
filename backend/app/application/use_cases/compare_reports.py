"""Use case wrapper for multi-report comparisons."""

from app.application.services.report_comparison_service import ReportComparisonService


class CompareReportsUseCase:
    """Thin boundary for structured report comparisons."""

    def __init__(self, report_comparison_service: ReportComparisonService) -> None:
        self._report_comparison_service = report_comparison_service

    def execute(
        self,
        document_ids: tuple[str, ...],
        *,
        provider: str,
        model: str,
        api_key: str,
    ) -> None:
        """Generate a structured comparison across reports."""
        return self._report_comparison_service.compare_reports(
            document_ids,
            provider=provider,
            model=model,
            api_key=api_key,
        )

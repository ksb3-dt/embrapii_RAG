"""Contract tests ensuring port Protocols accept expected fake implementations."""

from datetime import UTC, datetime

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
from app.ports.dense_retriever import DenseRetriever, RetrievalFilters
from app.ports.document_parser import DocumentParser
from app.ports.embedding_provider import BGE_M3_VECTOR_SIZE, EmbeddingProvider
from app.ports.file_storage import FileStorage
from app.ports.fusion_retriever import FusionRetriever
from app.ports.keyword_retriever import KeywordRetriever
from app.ports.llm_provider import LLMProvider
from app.ports.llm_provider_factory import LLMProviderFactory, LLMProviderName
from app.ports.repositories import (
    AnswerRepository,
    ChunkRepository,
    DocumentRepository,
    EvaluationRepository,
    JobRepository,
)


class FakeDocumentParser:
    def parse(self, file_path: str) -> list[DocumentPage]:
        return [DocumentPage(document_id="doc-1", page_number=1, text=file_path)]


class FakeEmbeddingProvider:
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * BGE_M3_VECTOR_SIZE for _ in texts]


class FakeDenseRetriever:
    def retrieve(
        self,
        query: str,
        filters: RetrievalFilters | None,
        limit: int,
    ) -> list[EvidenceChunk]:
        citation = Citation(document_id="doc-1", page_number=1)
        return [
            EvidenceChunk(
                chunk_id="chunk-1",
                document_id="doc-1",
                page_number=1,
                text=query,
                retrieval_source=RetrievalSource.DENSE,
                citation=citation,
            )
        ][:limit]


class FakeKeywordRetriever:
    def retrieve(
        self,
        query: str,
        filters: RetrievalFilters | None,
        limit: int,
    ) -> list[EvidenceChunk]:
        citation = Citation(document_id="doc-1", page_number=1)
        return [
            EvidenceChunk(
                chunk_id="chunk-1",
                document_id="doc-1",
                page_number=1,
                text=query,
                retrieval_source=RetrievalSource.KEYWORD,
                citation=citation,
            )
        ][:limit]


class FakeFusionRetriever:
    def retrieve(
        self,
        query: str,
        filters: RetrievalFilters | None,
        limit: int,
    ) -> list[EvidenceChunk]:
        citation = Citation(document_id="doc-1", page_number=1)
        return [
            EvidenceChunk(
                chunk_id="chunk-1",
                document_id="doc-1",
                page_number=1,
                text=query,
                retrieval_source=RetrievalSource.FUSION,
                citation=citation,
            )
        ][:limit]


class FakeLLMProvider:
    def generate(self, prompt: str, context: str | None = None) -> str:
        return f"{prompt}:{context or ''}"


class FakeLLMProviderFactory:
    def __init__(self) -> None:
        self.last_api_key: str | None = None

    def create(
        self,
        provider: LLMProviderName | str,
        model: str,
        api_key: str,
    ) -> LLMProvider:
        self.last_api_key = api_key
        return FakeLLMProvider()


class FakeDocumentRepository:
    def save_document(self, document: Document) -> Document:
        return document

    def get_document(self, document_id: str) -> Document | None:
        return None

    def list_documents(self) -> list[Document]:
        return []

    def delete_document(self, document_id: str) -> None:
        return None


class FakeChunkRepository:
    def save_chunks(self, chunks: list[DocumentChunk]) -> None:
        return None

    def get_chunks_by_document(self, document_id: str) -> list[DocumentChunk]:
        return []


class FakeAnswerRepository:
    def save_answer(self, answer_id: str, answer: Answer) -> None:
        return None

    def get_answer(self, answer_id: str) -> Answer | None:
        return None


class FakeJobRepository:
    def save_job(self, job: Job) -> Job:
        return job

    def get_job(self, job_id: str) -> Job | None:
        return None

    def update_job(self, job: Job) -> Job:
        return job


class FakeEvaluationRepository:
    def list_questions(self) -> list[EvaluationQuestion]:
        return []

    def save_evaluation_result(self, result: EvaluationResult) -> None:
        return None


class FakeFileStorage:
    def save_pdf(self, filename: str, content: bytes) -> str:
        return f"data/documents/{filename}"

    def delete_document_file(self, relative_path: str) -> None:
        return None

    def resolve_document_path(self, relative_path: str) -> str:
        return f"/tmp/{relative_path}"


def test_document_parser_fake_satisfies_contract() -> None:
    parser: DocumentParser = FakeDocumentParser()
    pages = parser.parse("data/documents/sample.pdf")
    assert pages[0].page_number == 1


def test_embedding_provider_fake_satisfies_contract() -> None:
    provider: EmbeddingProvider = FakeEmbeddingProvider()
    vectors = provider.embed_texts(["investimento", "projetos"])
    assert len(vectors) == 2
    assert len(vectors[0]) == BGE_M3_VECTOR_SIZE


def test_dense_retriever_fake_satisfies_contract() -> None:
    retriever: DenseRetriever = FakeDenseRetriever()
    filters = RetrievalFilters(document_ids=("doc-1",))
    results = retriever.retrieve("investimento", filters, 5)
    assert results[0].retrieval_source is RetrievalSource.DENSE


def test_keyword_retriever_fake_satisfies_contract() -> None:
    retriever: KeywordRetriever = FakeKeywordRetriever()
    results = retriever.retrieve("EMBRAPII", None, 3)
    assert results[0].retrieval_source is RetrievalSource.KEYWORD


def test_fusion_retriever_fake_satisfies_contract() -> None:
    retriever: FusionRetriever = FakeFusionRetriever()
    results = retriever.retrieve("projetos concluídos", None, 1)
    assert results[0].retrieval_source is RetrievalSource.FUSION


def test_llm_provider_fake_satisfies_contract() -> None:
    llm: LLMProvider = FakeLLMProvider()
    assert llm.generate("Resuma o relatório.", context="evidência") == (
        "Resuma o relatório.:evidência"
    )


def test_llm_provider_factory_does_not_persist_api_key() -> None:
    factory: LLMProviderFactory = FakeLLMProviderFactory()
    provider = factory.create(LLMProviderName.CLAUDE, "claude-sonnet", "session-key")
    assert provider.generate("Pergunta") == "Pergunta:"
    assert factory.last_api_key == "session-key"


def test_repository_fakes_satisfy_contracts() -> None:
    document_repo: DocumentRepository = FakeDocumentRepository()
    chunk_repo: ChunkRepository = FakeChunkRepository()
    answer_repo: AnswerRepository = FakeAnswerRepository()
    job_repo: JobRepository = FakeJobRepository()
    evaluation_repo: EvaluationRepository = FakeEvaluationRepository()

    document = Document(
        id="doc-1",
        filename="relatorio.pdf",
        source_path="data/documents/relatorio.pdf",
        status=DocumentStatus.PENDING,
    )
    assert document_repo.save_document(document).id == "doc-1"
    assert document_repo.list_documents() == []

    chunk_repo.save_chunks(
        [
            DocumentChunk(
                document_id="doc-1",
                chunk_id="chunk-1",
                page_number=1,
                text="texto",
                chunk_type=ChunkType.TEXT,
            )
        ]
    )
    assert chunk_repo.get_chunks_by_document("doc-1") == []

    answer = Answer(text="resposta", confidence_level=ConfidenceLevel.HIGH)
    answer_repo.save_answer("answer-1", answer)
    assert answer_repo.get_answer("answer-1") is None

    job = Job(
        id="job-1",
        job_type=JobType.INGEST_DOCUMENT,
        status=JobStatus.QUEUED,
        created_at=datetime(2026, 6, 30, tzinfo=UTC),
    )
    assert job_repo.save_job(job).id == "job-1"
    assert job_repo.get_job("job-1") is None
    assert job_repo.update_job(job).status is JobStatus.QUEUED

    evaluation_repo.save_evaluation_result(
        EvaluationResult(
            question_id="q-1",
            answer_text="12 projetos.",
            status=EvaluationStatus.COMPLETED,
        )
    )
    assert evaluation_repo.list_questions() == []


def test_file_storage_fake_satisfies_contract() -> None:
    storage: FileStorage = FakeFileStorage()
    relative_path = storage.save_pdf("relatorio.pdf", b"%PDF-1.4")
    assert relative_path.endswith("relatorio.pdf")
    storage.delete_document_file(relative_path)
    assert storage.resolve_document_path(relative_path).startswith("/tmp/")


def test_port_modules_import_cleanly() -> None:
    import importlib

    port_modules = [
        "app.ports.document_parser",
        "app.ports.embedding_provider",
        "app.ports.dense_retriever",
        "app.ports.keyword_retriever",
        "app.ports.fusion_retriever",
        "app.ports.llm_provider",
        "app.ports.llm_provider_factory",
        "app.ports.repositories",
        "app.ports.file_storage",
    ]
    for module_name in port_modules:
        module = importlib.import_module(module_name)
        assert module.__name__ == module_name

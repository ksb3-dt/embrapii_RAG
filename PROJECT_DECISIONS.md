# EMBRAPII Reports RAG - Project Decisions

## Goal

Build a local MVP RAG application to help a small group of managers analyze public EMBRAPII reports. The system should support high-accuracy report analysis with page-level citations, clear uncertainty, and background/deep analysis jobs rather than only instant chat responses.

## Primary Use Cases

The MVP will support three analysis workflows:

1. Ask questions across reports with citations.
2. Summarize one report.
3. Compare multiple reports.

The system should answer from the uploaded report corpus by default. It should avoid using general model knowledge for factual claims, to reduce hallucinations and keep answers grounded in the retrieved documents.

## Output Structures

The MVP should use fixed initial/default output structures. These structures can be revised after testing with real manager questions and the golden set.

### Report Summary Structure

1. Executive Summary
2. Main Findings
3. Relevant Numbers/KPIs
4. Risks, Gaps, Or Limitations
5. Notable Evidence
6. What Was Not Clear

Important summary rules:

- Cite important factual claims, especially numbers, dates, and named programs.
- Separate what the report explicitly says from interpretation or implications.
- Clearly state when information is missing, ambiguous, or weakly supported.
- Avoid over-interpreting tables, infographics, or flowcharts when extraction quality is uncertain.

### Multi-Report Comparison Structure

1. High-Level Conclusion
2. Similarities
3. Differences
4. Trends Over Time
5. Evidence By Report
6. Uncertainties Or Missing Data

Important comparison rules:

- Compare evidence per report before producing the final synthesis.
- Cite the reports/pages that support each important comparison.
- Highlight when reports use different metrics, time ranges, terminology, or levels of detail.
- Do not force a comparison if the source reports are not directly comparable.

## Users

- Internal tool for managers.
- Expected user count: fewer than 15.
- No per-user document access restrictions are needed for the MVP.
- Reports are public, so the system does not need special handling for confidential data in the MVP.
- Users are expected to ask questions in Portuguese only.

## Document Scope

- Source documents: EMBRAPII reports.
- Format: PDF only.
- PDFs are expected to contain selectable text, tables, and some infographics or flowcharts.
- Scanned PDFs and OCR are out of scope for v1, but the ingestion design should allow an OCR module to be added later.
- Initial corpus size: about 300 reports.
- Average report size: 30-80 pages.
- Reports will be manually downloaded and added by the user.
- Once added, documents will rarely be deleted and should never be modified in place.
- Version history is not required for v1.

## Architecture Decisions

### Application Shape

- Local Docker-based MVP.
- Designed so it can later be hosted on AWS.
- Slower background/deep analysis jobs are acceptable and preferred over trying to make every operation instant.
- The MVP should be easy for a manager or evaluator to run by cloning the GitHub repository and starting the app with Docker.
- Frontend, backend, Qdrant, and any required worker/background-job service should be containerized.
- Later AWS hosting target is unknown, so the Docker setup should avoid assumptions that only work on one hosting platform.

### Frontend

- Use React for the UI.
- Streamlit was rejected because the project may need a more flexible UI, better control over workflows, and a cleaner path to a production internal tool.

### Backend

- Use Python for the backend.
- FastAPI is the likely backend framework.
- Use LangChain as the RAG/application orchestration framework.
- Use pragmatic Hexagonal Architecture for backend organization.
- FastAPI routes should remain thin and call application services/use cases.
- The application core should depend on ports/interfaces rather than concrete tools such as Qdrant, PyMuPDF, or specific LLM providers.
- Infrastructure adapters should implement ports for parsing, embedding, retrieval, LLM providers, repositories, and file storage.
- Avoid over-engineering: create ports only where replacement is realistic or already expected.
- Dependency injection should happen in `backend/app/core/dependencies.py` for mostly static dependencies.
- LLM provider creation should use a request-specific factory because provider, model, and API key come from the user request/session.

### Vector Store

- Use Qdrant.
- Qdrant should run locally in Docker for the MVP.
- Qdrant was chosen because it has a good local development experience, supports metadata filtering, and has a reasonable path toward later production hosting.

### Retrieval Architecture

- The final retrieval architecture is not fully decided yet.
- Dense semantic retrieval with `BAAI/bge-m3` is required.
- Hybrid search should be explicitly evaluated before implementation is finalized.

Hybrid search means combining semantic vector search with keyword/sparse search. This may be valuable because EMBRAPII reports may contain exact names, program labels, acronyms, dates, laws, KPIs, and table values that dense search alone can miss.

Potential retrieval options:

1. Dense-only retrieval
   - Simpler to implement.
   - Good for conceptual questions and semantic similarity.
   - May miss exact terms, acronyms, codes, dates, and numeric references.

2. Hybrid retrieval
   - Combines dense vectors with keyword/sparse retrieval.
   - Better for exact terms and factual lookup.
   - More complex to tune and evaluate.
   - Recommended candidate for a high-accuracy RAG over reports.

3. Dense retrieval plus reranking
   - Retrieves a larger candidate set and reranks it before answer generation.
   - Can improve citation quality and reduce irrelevant context.
   - Adds latency and local compute cost.

Recommended direction:

- Start the architecture in a way that can support hybrid retrieval.
- Use dense retrieval plus exact keyword retrieval.
- Fuse dense and keyword retrieval results with Reciprocal Rank Fusion.
- Skip reranking for the MVP.
- Add reranking later only if the golden set shows that fused results contain the right chunks but order them poorly, or if citation precision is not good enough.
- The baseline retrieval flow should be: dense top-k + keyword top-k -> Reciprocal Rank Fusion -> final top-n context.

### Evidence Auditing

- Users should be able to audit the chunks used to generate an answer.
- The answer UI should include a button named `Auditar`.
- Clicking `Auditar` should show the retrieved/generated-evidence chunks in a popup or side panel.
- The audit view should show the chunk text and useful metadata, such as report title, page number, retrieval source, rank/score, and citation information.
- This should be included from the start because it improves trust, debugging, and golden-set evaluation.
- Showing already-retrieved chunks should have minimal response-time impact.
- Avoid expensive audit features in the MVP, such as LLM-generated explanations per chunk, full PDF page rendering, or exact visual highlighting inside PDFs.

### Local Document Storage

- For the MVP, uploaded/downloaded report PDFs can live in a folder inside the project.
- The likely default folder should be something like `data/documents/`.
- This is acceptable because the MVP is local, the corpus is modest, and the documents are public.
- If the project later moves to AWS, document storage can be migrated to object storage such as S3.
- Skip a separate `data/uploads/` staging folder for v1.
- PDFs should be added through UI upload.
- When a user uploads a PDF, the application should automatically copy/store the document in `data/documents/`.
- Users should be able to delete documents from the UI.
- The UI should allow users to view the list of ingested documents, but it should not include an in-app PDF viewer.

### Metadata Storage

- Use SQLite for MVP metadata storage.
- Store the SQLite database at `data/app.db`.
- SQLite should track local metadata such as documents, chunks, jobs, answers, evidence records, and evaluation results as needed.

### Embeddings

- Use `BAAI/bge-m3`.
- `BAAI/bge-m3` has 1024-dimensional embeddings.
- It is multilingual and appropriate for Portuguese report retrieval.
- It supports longer inputs than many smaller embedding models and is a stronger accuracy-first choice than `intfloat/multilingual-e5-base`.
- Qdrant collections using this model must be configured with vector size `1024`.
- If the embedding model changes later, the corpus should be re-embedded into a new Qdrant collection.
- The MVP target hardware is a laptop with 16 GB RAM and an Intel Core i7 CPU.
- Embedding should be designed to work on CPU-only hardware for the MVP unless GPU availability is confirmed later.
- Because `BAAI/bge-m3` is heavier than smaller embedding models, ingestion may be slower on the target laptop; this is acceptable if it improves retrieval quality.

Rejected/alternative option:

- `intfloat/multilingual-e5-base`
  - 768-dimensional embeddings.
  - Lighter and faster than `BAAI/bge-m3`.
  - Usually lower retrieval quality and shorter effective input length.
  - Kept as a fallback if local compute becomes a problem.

### LLM Provider

- The app should let the user paste an API key for the LLM provider.
- API keys should not be hardcoded.
- For v1, prefer keeping the API key in session memory instead of storing it permanently.
- If API keys are kept only in session memory, users should expect to paste the key again after restarting the app/session.
- If persistent API key storage is added later, it should be encrypted and treated as a security-sensitive feature.
- For the MVP, it is acceptable for users to paste the API key each session.
- The first implementation should support Claude, Gemini, OpenAI, and DeepSeek providers.
- Gemini or DeepSeek are likely candidates for the user's own testing, while managers may use Claude or OpenAI.
- LLM provider/model selection should use predefined dropdown options instead of free-text model names.
- The selected provider/model can be kept in browser/session state for the MVP.

### Final Answer LLM Options

The user originally expected a Claude subscription to include API access, but Claude API usage is normally billed separately.

The MVP should be designed with provider abstraction so different final-answer models can be tested.

Recommended high-quality/cost-effective candidates:

1. Claude Sonnet
   - Strong default for manager-facing final answers.
   - Good at synthesis, uncertainty, and citation-following.
   - More expensive than the cheapest alternatives.

2. Gemini Pro
   - Strong quality-per-cost candidate.
   - Good option for long-context and document-heavy analysis.

3. DeepSeek V4 Pro
   - Much cheaper candidate.
   - Should be evaluated before trusting it for final manager-facing answers.

Cheaper models such as DeepSeek should be considered for lower-risk tasks such as draft summaries, batch pre-analysis, first-pass comparisons, and candidate theme extraction. Claude or Gemini Pro should be preferred for final answers where accuracy and citation discipline matter most.

### PDF Parsing

- Use PyMuPDF for v1.
- Keep PDF parsing in a separate module so table extraction, OCR, or layout-aware parsing can be improved later without rewriting the full ingestion pipeline.
- Good table and infographic accuracy would be valuable, but it is not essential for the first MVP.
- If PyMuPDF extracts incomplete text from tables, infographics, or flowcharts, the system should still ingest the available text and leave better extraction for a later module.

Potential future table-specific libraries:

- `pdfplumber`
- `Camelot`
- `Tabula`
- Vision/LLM-based extraction for infographics, flowcharts, and difficult visual content

## Ingestion Pipeline

The ingestion pipeline should be modular:

1. PDF intake
2. PyMuPDF page extraction
3. Text/layout block extraction
4. Optional table extraction module
5. Chunking
6. Embedding with `BAAI/bge-m3`
7. Indexing in Qdrant
8. Metadata storage

The design should make it possible to add OCR later:

1. Scanned PDF detection
2. OCR processing
3. Normalization into the same page/chunk format
4. Existing chunking, embedding, and indexing pipeline

## Citation Requirements

- Page-level citations are required often, but not necessarily for every sentence.
- Factual answers should generally be supported by citations.
- The system should make it clear when information could not be found in the reports.
- Unsupported claims should be avoided.

Recommended citation metadata per chunk:

- Document ID
- Report title
- Source file path
- Source URL, if available
- Page number
- Section title, if detectable
- Chunk type, such as text, table, caption, infographic text
- Ingested timestamp

## Retrieval And Answering Constraints

- Answers should be grounded in retrieved report content.
- General model knowledge should not be used for factual claims unless explicitly enabled later.
- If retrieval does not find enough evidence, the answer should say that the information could not be found in the indexed reports.
- If the answer is low confidence, the UI should show a small alert message at the beginning of the answer and the answer text should explicitly mention the uncertainty.
- High accuracy is more important than low latency.
- Background/deep analysis jobs are acceptable for summaries and comparisons.

## Evaluation Plan

A golden evaluation set should be created during development, not necessarily before coding starts.

Suggested workflow:

1. Start coding ingestion and retrieval.
2. Create a small first golden set of 15-20 questions while agents are coding.
3. Use the first golden set to tune chunking, retrieval count, prompts, and model choices.
4. Expand to 50-100 questions before claiming high accuracy.
5. If the first real manager questions are not known yet, use the initial golden set creation process to discover and refine them.

The golden set should include:

- Simple factual questions.
- Questions requiring citations.
- Questions about one report.
- Questions comparing multiple reports.
- Table-based questions.
- Questions where the answer is not present and the system should refuse clearly.
- Portuguese-language questions.
- Reports from the last five years, which should be prioritized for the first demo and initial golden set.

Evaluation metrics:

- Retrieval accuracy: whether the right page/chunk is found in top-k retrieval results.
- Answer accuracy: whether the final answer is factually correct.
- Citation accuracy: whether citations support the claims.
- Refusal quality: whether the system says it cannot find information when evidence is missing.
- Completeness: whether important relevant facts are missing.
- Hallucination rate: whether unsupported claims are produced.

## Current Unknowns

Important product and technical unknowns still to answer:

1. What are the top 5-10 real questions managers will ask? This will be discovered during initial golden set creation.
2. Should ingestion start automatically after upload, or should the user click an explicit `Ingest` action?
3. Should deleting a document also delete related SQLite metadata, Qdrant chunks, answer history, and evidence records?
4. Should chat history persist in SQLite after restarting the app, or only live during the browser session?
5. Should uploaded documents be global for all local users/sessions, or tied to a specific chat/session?
6. Should `Compare Documents` and `Summarize Document` require selecting documents from a list first, or should natural-language document selection be supported in v1?
7. What metadata can be reliably extracted from report filenames or report text?
8. What should the acceptable latency be for each workflow?
9. What is the minimum acceptable answer/citation quality for the manager demo?
10. Who will manually review the first golden set answers?
11. What is the backup/export story for the local MVP?
12. What AWS services are likely for a later deployment?

## Recommended MVP Boundary

The MVP should include:

- React UI.
- Python/FastAPI backend.
- LangChain RAG pipeline.
- Qdrant vector store in Docker.
- Local file storage.
- SQLite metadata storage at `data/app.db`.
- PyMuPDF parser module.
- `BAAI/bge-m3` local embeddings.
- User-pasted LLM API key.
- Provider abstraction for Claude, Gemini, OpenAI, and DeepSeek APIs.
- Question answering with page-level citations.
- One-report summaries.
- Multi-report comparisons.
- Background/deep analysis jobs.
- Clear "not found in reports" behavior.
- Low-confidence warning alert at the beginning of uncertain answers.
- `Auditar` button on answers to inspect evidence chunks.
- Small golden set created during development.
- Last five years of reports prioritized for the first demo and initial golden set.
- Containerized frontend, backend, vector store, and background worker.
- Redis + RQ job queue.
- UI upload for PDFs, with automatic storage in `data/documents/`.
- Document list and delete action in the UI.
- No in-app PDF viewer.
- Bash script for checking service health.

## Planned Project Structure

The project should use the following initial folder structure:

```text
embrapii-rag/
  docker-compose.yml                  # Runs frontend, backend, worker, Qdrant, and any queue/cache service.
  README.md                           # Setup, Docker usage, project overview, and MVP limitations.
  PROJECT_DECISIONS.md                # Architecture/product decisions captured during planning.
  .env.example                        # Non-secret environment variable template.
  data/
    documents/                        # Local MVP folder for EMBRAPII PDF files.
    app.db                            # SQLite metadata database for the local MVP.
    qdrant/                           # Optional local mounted Qdrant data volume.
  docs/
    adr/                              # Future Architecture Decision Records after coding starts.
    evaluation/                       # Golden set and evaluation-related documentation/data.
    specs/                            # Implementation specs, one milestone or task per file.
  backend/
    Dockerfile                        # Backend/worker image definition.
    pyproject.toml                    # Python dependencies and project metadata.
    app/
      main.py                         # FastAPI app creation and router registration.
      core/
        config.py                     # Environment/config loading.
        dependencies.py               # Static dependency wiring for FastAPI and worker reuse.
      api/
        routes/
          documents.py                # Upload, list, and ingest document endpoints.
          qa.py                       # Question-answering endpoint.
          summaries.py                # One-report summary endpoints.
          comparisons.py              # Multi-report comparison endpoints.
          jobs.py                     # Background job status/result endpoints.
          evidence.py                 # Evidence/audit endpoints for the Auditar UI.
          evaluation.py               # Golden-set/evaluation endpoints, if exposed in MVP.
        schemas/
          documents.py                # Request/response DTOs for document APIs.
          qa.py                       # Request/response DTOs for Q&A.
          summaries.py                # Request/response DTOs for summaries.
          comparisons.py              # Request/response DTOs for comparisons.
          jobs.py                     # Request/response DTOs for background jobs.
          evidence.py                 # Request/response DTOs for evidence chunks.
      application/
        prompts/
          qa_prompt.py                  # Prompt template/instructions for grounded question answering.
          summary_prompt.py             # Prompt template/instructions for structured report summaries.
          comparison_prompt.py          # Prompt template/instructions for structured multi-report comparisons.
        services/
          document_ingestion_service.py # Coordinates parsing, chunking, embedding, and indexing.
          question_answering_service.py # Coordinates retrieval, LLM answer generation, citations, and confidence.
          report_summary_service.py     # Generates structured one-report summaries.
          report_comparison_service.py  # Generates structured multi-report comparisons.
          evidence_audit_service.py     # Returns chunks/metadata used to generate an answer.
          evaluation_service.py         # Runs golden-set evaluation and records metrics.
          job_service.py                # Creates, tracks, and updates background jobs.
        use_cases/
          ingest_document.py            # Optional thin use-case wrapper for document ingestion.
          ask_question.py               # Optional thin use-case wrapper for Q&A.
          summarize_report.py           # Optional thin use-case wrapper for summaries.
          compare_reports.py            # Optional thin use-case wrapper for comparisons.
      domain/
        models/
          document.py                   # Document/report domain models.
          chunk.py                      # Chunk, citation, and evidence models.
          answer.py                     # Answer and confidence models.
          job.py                        # Background job domain model.
          evaluation.py                 # Golden-set question/result models.
        policies/
          confidence_policy.py          # Rules for low-confidence warnings and not-found behavior.
          citation_policy.py            # Rules for when citations are required.
      ports/
        document_parser.py              # Interface for PDF/OCR/table parsers.
        embedding_provider.py           # Interface for embedding models.
        dense_retriever.py              # Interface for semantic vector retrieval.
        keyword_retriever.py            # Interface for exact keyword retrieval.
        fusion_retriever.py             # Interface for RRF or other fusion logic.
        llm_provider.py                 # Interface for final-answer LLM providers.
        llm_provider_factory.py         # Interface/factory contract for request-specific LLM creation.
        repositories.py                 # Interfaces for documents, chunks, answers, jobs, and evaluation storage.
        file_storage.py                 # Interface for local/S3-like document storage.
      infrastructure/
        parsers/
          pymupdf_parser.py             # PyMuPDF implementation of document parsing.
        embeddings/
          bge_m3_embedding_provider.py  # Local BAAI/bge-m3 embedding implementation.
        retrieval/
          qdrant_dense_retriever.py     # Qdrant dense vector retrieval implementation.
          keyword_retriever.py          # Exact keyword/BM25-style retrieval implementation.
          reciprocal_rank_fusion.py     # RRF implementation joining dense and keyword results.
        llms/
          anthropic_provider.py         # Claude provider adapter.
          gemini_provider.py            # Gemini provider adapter.
          openai_provider.py            # OpenAI provider adapter.
          deepseek_provider.py          # DeepSeek provider adapter.
          llm_provider_factory.py       # Creates provider adapters from request provider/model/API key.
        persistence/
          sqlite_repositories.py        # Local MVP metadata/job/answer repository implementation.
        storage/
          local_file_storage.py         # Local filesystem document storage implementation.
        qdrant/
          client.py                     # Qdrant client creation and collection setup helpers.
      worker/
        main.py                         # Worker process entrypoint.
        tasks.py                        # Background tasks for ingestion, summaries, comparisons, evaluation.
  frontend/
    Dockerfile                          # React frontend image definition.
    package.json                        # Frontend dependencies and scripts.
    src/
      main.tsx                          # React app entrypoint.
      App.tsx                           # Root React component.
      api/
        client.ts                       # HTTP client for backend API calls.
        documents.ts                    # Document API functions.
        qa.ts                           # Q&A API functions.
        summaries.ts                    # Summary API functions.
        comparisons.ts                  # Comparison API functions.
        jobs.ts                         # Job polling API functions.
        evidence.ts                     # Evidence/audit API functions.
      components/
        ApiKeyForm.tsx                  # Provider/model/API-key input form.
        DocumentUploader.tsx            # PDF upload/add UI.
        QuestionAnswerPanel.tsx         # Ask questions and display answers.
        SummaryPanel.tsx                # One-report summary UI.
        ComparisonPanel.tsx             # Multi-report comparison UI.
        AnswerCard.tsx                  # Displays answer, citations, confidence alert, and Auditar button.
        EvidenceAuditPanel.tsx          # Popup/side panel showing chunks used for generation.
        JobStatus.tsx                   # Background job progress/status display.
      pages/
        DocumentsPage.tsx               # Document management page.
        AskPage.tsx                     # Q&A workflow page.
        SummaryPage.tsx                 # Summary workflow page.
        ComparePage.tsx                 # Comparison workflow page.
        EvaluationPage.tsx              # Golden-set/evaluation page, if included in MVP.
      types/
        api.ts                          # Shared frontend TypeScript API types.
      styles/
        globals.css                     # Global frontend styles.
```

## Implementation Milestones

Milestones should be ordered to reduce risk early, prove the local Docker workflow, validate PDF extraction and retrieval quality, and produce a working vertical slice before polishing secondary workflows.

Important ordering principles:

- Test uncertain parts early: Docker, `BAAI/bge-m3` on the target laptop, PyMuPDF extraction, Qdrant indexing, and retrieval quality.
- Respect dependency order: ingestion before retrieval, retrieval before Q&A, Q&A before evidence audit, and retrieval/evidence before evaluation.
- Prefer visible/testable outcomes for each milestone.
- Build one vertical slice before expanding all workflows.
- Create the first golden set early enough to guide chunking, retrieval, prompts, and confidence rules.

Milestones:

1. Project Scaffold And Docker
   - Create frontend, backend, worker, Redis, and Qdrant containers.
   - Add health checks.

2. Backend Architecture Skeleton
   - Implement the pragmatic hexagonal folder structure.
   - Add basic FastAPI routes, config, dependency wiring, and placeholder ports/services.

3. PDF Ingestion Prototype
   - Use PyMuPDF to parse a few real EMBRAPII PDFs.
   - Store extracted page/chunk metadata locally.

4. Embedding And Qdrant Indexing
   - Run `BAAI/bge-m3`.
   - Create Qdrant collections.
   - Embed chunks and index them.

5. Dense + Keyword Retrieval With RRF
   - Implement dense retrieval.
   - Implement exact keyword retrieval.
   - Fuse results with Reciprocal Rank Fusion.
   - Manually inspect retrieved chunks.

6. First Q&A Vertical Slice
   - Allow a user to ask a Portuguese question.
   - Retrieve evidence.
   - Call the selected LLM provider.
   - Return an answer with page citations.

7. Evidence Audit
   - Add the `Auditar` button.
   - Show chunks used for generation in a popup or side panel.

8. Background Jobs
   - Move ingestion and long-running analysis into Redis + RQ worker jobs.
   - Add job status polling.

9. Golden Set v1
   - Create 15-20 Portuguese evaluation questions using last-five-years reports.
   - Use results to tune chunking, retrieval, prompts, and confidence rules.

10. Summary Workflow
    - Implement structured one-report summary using the chosen summary format.

11. Comparison Workflow
    - Implement structured multi-report comparison using the chosen comparison format.

12. Evaluation And Hardening
    - Expand tests.
    - Run the golden set.
    - Fix failures.
    - Improve not-found behavior.
    - Polish Docker documentation.

The first major goal is a complete vertical slice: one real PDF can be ingested, indexed, queried, cited, and audited.

## Documentation Conventions

- `PROJECT_DECISIONS.md` records the initial product, architecture, and convention decisions before coding starts.
- Future architecture decisions made after implementation begins should be recorded as ADRs in `docs/adr/`.
- ADRs are not required for the initial planning decisions already captured in `PROJECT_DECISIONS.md`.
- `README.md` is for human setup and usage documentation.
- `AGENTS.md` should be generated from `PROJECT_DECISIONS.md` before coding agents start work.
- `docs/specs/` should contain implementation specs, usually one milestone or focused task per file.
- Each spec should include goal, scope, non-goals, relevant decisions, expected files, implementation notes, acceptance criteria, verification steps, and risks/edge cases.
- Code comments should be written in Portuguese.
- Code identifiers, filenames, modules, API fields, database fields, commit messages, and technical documentation should be written in English.
- Comments should explain intent, trade-offs, or non-obvious behavior; avoid comments that merely restate what the code does.
- Public ports/interfaces and non-obvious services should have short docstrings.
- Prompts should live in a clear backend prompt module or prompt files, not scattered through API routes.
- If implementation diverges from `PROJECT_DECISIONS.md`, update the relevant decision document or add an ADR explaining the change.

## MVP Coding And API Conventions

### Backend Tooling

- Use Python for the backend.
- Use `uv` for backend dependency management and Python project workflow.
- Use `pytest` for backend tests.
- Use `ruff` for backend linting and formatting because it helps coding agents keep Python changes consistent with minimal setup overhead.
- Use focused automated tests where practical, especially for risky logic.

### Frontend Tooling

- Use Node.js for the frontend toolchain.
- Use `npm` as the frontend package manager.
- Use Vite as the React development/build tool.
- Use React with TypeScript.
- Use `eslint` and `prettier` because they help coding agents keep frontend changes consistent with minimal setup overhead.

### Local Development And Docker

- `docker compose up --build` should start the full local MVP stack.
- Default frontend port: `5173`.
- Default backend port: `8000`.
- Default Qdrant port: `6333`.
- Default Redis port: `6379`.
- Qdrant data should persist at `data/qdrant/`.
- Provide a bash script to check health/status for the backend, Qdrant, Redis, and worker instead of building a frontend health/status page for the MVP.

### Frontend UX Shape

- The MVP frontend should be centered around a chat screen.
- The chat screen should include a sidebar with chat history.
- Normal questions can be asked by typing into the chat.
- Main activities such as `Compare Documents` and `Summarize Document` can appear as buttons/actions.
- The `Auditar` button should appear on answer fields and open a popup or side panel with the evidence chunks.
- Evaluation should be accessible from another part of the app through a menu.
- The UI should include document upload, document list, and document deletion.
- The UI should not include an in-app PDF viewer; users can open PDFs outside the application if needed.

### API Response And Error Pattern

- Successful FastAPI responses may return the response object directly; a universal `{ "data": ... }` wrapper is not required for the MVP.
- Application-level errors should use a consistent JSON shape with:
  - `code`
  - `message`
  - optional `details`
- Example:

```json
{
  "code": "LLM_PROVIDER_ERROR",
  "message": "Could not generate the answer with the selected provider.",
  "details": {
    "provider": "gemini"
  }
}
```

- Error codes should be stable enough for the frontend to map them to user-friendly messages.
- FastAPI validation errors may use FastAPI's default validation response unless there is a strong reason to customize them later.

### Prompt Organization

- LLM prompts should not be scattered through API route handlers.
- Store core prompt templates/instructions in:
  - `backend/app/application/prompts/qa_prompt.py`
  - `backend/app/application/prompts/summary_prompt.py`
  - `backend/app/application/prompts/comparison_prompt.py`
- Prompts should support grounded answers, citation behavior, insufficient-evidence behavior, low-confidence wording, structured summaries, and structured comparisons.

### Testing Expectations

- Each implementation spec should define acceptance criteria and verification steps.
- Automated tests should be added where practical, especially for:
  - Chunking behavior.
  - Reciprocal Rank Fusion.
  - Confidence and not-found behavior.
  - API schemas and key routes.
  - Job status behavior.
- Manual verification steps are acceptable for early MVP milestones, especially when validating Docker startup, PDF extraction quality, retrieval quality, and LLM output behavior.
- The golden set should become the main evaluation tool for RAG quality once ingestion and retrieval are working.

The MVP should not include:

- OCR for scanned PDFs.
- Complex table extraction beyond what PyMuPDF can reasonably support.
- User permissions or role-based access.
- Document version history.
- Persistent API key storage unless explicitly added later.
- Fine-tuning.
- Fully automated decision-making.

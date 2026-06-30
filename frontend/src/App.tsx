const PLANNED_CAPABILITIES = [
  "Perguntas e respostas com citações por página",
  "Resumo estruturado de relatório",
  "Comparação entre múltiplos relatórios",
  "Upload e gestão de documentos PDF",
  "Auditoria de evidências (Auditar)",
  "Avaliação com golden set",
] as const;

const EXPECTED_BACKEND_URL = "http://localhost:8000";

function App() {
  return (
    <div className="app">
      <header className="app__header">
        <p className="app__eyebrow">EMBRAPII</p>
        <h1 className="app__title">Reports RAG</h1>
        <p className="app__subtitle">
          Ferramenta interna para análise de relatórios públicos EMBRAPII
        </p>
      </header>

      <main className="app__main">
        <section className="panel panel--status" aria-labelledby="status-heading">
          <h2 id="status-heading">Status do MVP</h2>
          <p className="status-badge" role="status">
            Infraestrutura local — Milestone 1
          </p>
          <p>
            Esta versão expõe apenas o shell da aplicação. Upload, Q&amp;A,
            resumo, comparação e auditoria de evidências ainda{" "}
            <strong>não estão funcionais</strong>.
          </p>
        </section>

        <section className="panel" aria-labelledby="planned-heading">
          <h2 id="planned-heading">Capacidades planejadas</h2>
          <p className="panel__lead">
            Os fluxos abaixo serão implementados nos próximos marcos do MVP:
          </p>
          <ul className="capability-list">
            {PLANNED_CAPABILITIES.map((capability) => (
              <li key={capability}>{capability}</li>
            ))}
          </ul>
        </section>
      </main>

      <footer className="app__footer">
        <p>
          Backend esperado:{" "}
          <code className="backend-url">{EXPECTED_BACKEND_URL}</code>
        </p>
      </footer>
    </div>
  );
}

export default App;

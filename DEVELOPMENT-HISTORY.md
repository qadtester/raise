# RAISE — Development History

Este documento organiza a narrativa técnica da evolução do projeto atualmente denominado **RAISE**, registrando sua trajetória desde a concepção inicial em monólito até a transição para arquitetura desacoplada Full Stack.

---

## 1. Origem

A proposta do projeto originou-se da intenção de conectar a especificação de requisitos de produto e o processo de garantia de qualidade (QA) em uma ferramenta unificada. O objetivo técnico central foi incorporar modelos de linguagem (LLMs) capazes de receber o contexto do projeto e gerar casos de teste e artefatos formais estruturados conforme as diretrizes do ISTQB.

---

## 2. Etapa 1: `qaboard` (Prova de Conceito Funcional)

- **Repositório:** [https://github.com/qadtester/qaboard](https://github.com/qadtester/qaboard)
- **Identidade Nominal Registrada:** `"QA & Requisitos Hub"` / `"🎯 QA Hub"`
- **Período Registrado:** Agosto de 2026
- **Tecnologias Identificadas:** Python, Streamlit, Supabase, Groq, Google Generative AI, OpenAI SDK, Pandas, Plotly, Tabulate, python-dotenv.
- **Arquitetura:** Aplicação modular inicial com 4 menus (`Gestão de Projetos`, `Requisitos`, `Módulo de Testes`, `Métricas & Exportação`).
- **Funcionalidades:** Login e registro básico, seleção de projetos ativos, geração por IA de Personas/Histórias/Riscos e módulo unificado de testes e defeitos.
- **Relação com etapas posteriores:** Estabeleceu a base lógica e os prompts que serviram de alicerce para a expansão do sistema.

---

## 3. Etapa 2: `hubv2` (Experimentação de Gestão de Equipes)

- **Repositório:** [https://github.com/qadtester/hubv2](https://github.com/qadtester/hubv2)
- **Identidade Nominal Registrada:** `"QA & Requisitos Hub"` / `"🎯 QA Hub"`
- **Período Registrado:** Agosto de 2026
- **Tecnologias Identificadas:** Stack base expandida com manipulação documental (`pypdf` e `python-docx`).
- **Arquitetura:** Expansão para modelo multi-tenant com menu de `"👥 Gestão de Equipe"`.
- **Funcionalidades:** Tabelas relacionais de membros (`team_members`) e anexos técnicos (`project_documents`).
- **Relação no histórico:** Ramificação experimental focada em validar o isolamento de dados por organização.

---

## 4. Etapa 3: `qahub` (Desenvolvimento Intermediário e Governança)

- **Repositório:** [https://github.com/qadtester/qahub](https://github.com/qadtester/qahub)
- **Identidade Nominal Registrada:** `"QA & Requisitos Hub"` / `"🎯 QA Hub"`
- **Período Registrado:** Agosto de 2026
- **Tecnologias Identificadas:** Python, Streamlit, Supabase, Groq, Google Generative AI, Pandas, Plotly, PyPDF, Python-docx.
- **Principais Mudanças:**
  - Criação do Painel Master (`modules/admin_panel.py`) para governança global.
  - Implementação de controle granular de permissões (`utils/permissions.py`).
  - Pipeline de exportação multi-formato (`utils/export.py` em CSV, Markdown e relatórios HTML com gráficos Plotly embutidos).
- **Relação no histórico:** Ambiente principal de consolidação administrativa e de relatórios antes da homologação.

---

## 5. Etapa 4: `homolograise` (Homologação, Nome RAISE e Kanban)

- **Repositório:** [https://github.com/qadtester/homolograise](https://github.com/qadtester/homolograise)
- **Identidade Nominal Registrada:** **RAISE**
- **Período Registrado:** Agosto de 2026
- **Tecnologias Identificadas:** Python, Streamlit, Supabase (Storage, cartões e colunas dinâmicas), Groq, Gemini, OpenRouter.
- **Principais Mudanças:**
  - Adoção formal do nome **RAISE** na identidade do produto.
  - Criação do Quadro Kanban interativo com persistência em banco e anexos no storage.
  - Refatoração do Kanban separando serviços (`services/kanban_service.py`), telas (`board.py`) e modais (`modals.py`).
  - Desacoplamento funcional dos módulos de casos de teste e defeitos.
- **Relação no histórico:** Ambiente de homologação intensiva que homologou a transição da identidade e da experiência visual.

---

## 6. Etapa 5: `raise` (Marco Consolidado em Monólito)

- **Repositório:** [https://github.com/qadtester/raise](https://github.com/qadtester/raise)
- **Identidade Nominal Registrada:** **RAISE**
- **Período Registrado:** Setembro de 2026
- **Características Técnicas:**
  - Base monólito consolidada, limpa de artefatos temporários de homologação.
  - Estabilização do motor de requisitos, casos de teste ISTQB e Kanban operacional.
- **Relação no histórico:** Representa o fechamento do ciclo de prototipagem em Streamlit e a base funcional validada para o desacoplamento arquitetural.

---

## 7. Transição Arquitetural: Full Stack (v1 e v2 Ativa)

Com as regras de negócio consolidadas, o projeto migrou do monólito Streamlit para arquitetura distribuída moderna:

- **Fase Full Stack v1 (Desacoplamento Inicial):** Separação em repositórios dedicados para Frontend e Backend, permitindo melhor gerenciamento de estado e desacoplamento de serviços.
- **Fase Full Stack v2 (Evolução Contínua / Ativa):** Refatoração de interface e usabilidade, otimização das chamadas de orquestração de IA, maior robustez no fluxo de defeitos e novas automações operacionais.

---

## 8. Continuidade do Desenvolvimento

O desenvolvimento do RAISE segue ativo e contínuo nas bases Full Stack. Os repositórios da fase Streamlit permanecem arquivados como registro histórico, técnico e de comprovação de autoria.

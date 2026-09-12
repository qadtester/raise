# RAISE

## Overview

O **RAISE** é uma plataforma integrada de Engenharia de Qualidade de Software (Quality Engineering) e Gestão de Requisitos orientada por Inteligência Artificial generativa.

O sistema reúne a especificação de requisitos de negócio, análise de riscos, planejamento e execução de casos de teste segundo as diretrizes do **ISTQB**, registro e ciclo de vida de defeitos (*bug reports*) e acompanhamento operacional por meio de um **Quadro Kanban** colaborativo.

---

## What is RAISE?

O **RAISE** foi concebido para aproximar o levantamento de requisitos e o fluxo de testes de software em um único ambiente. Em vez de utilizar ferramentas isoladas e planilhas dispersas, o RAISE oferece um espaço centralizado onde o contexto do negócio alimenta diretamente a geração e o acompanhamento de artefatos formais de teste.

---

## Product Vision

A proposta de produto do RAISE apoia-se em três princípios:

1. **Aderência a Padrões de Teste:** Aplicação de conceitos do ISTQB (*International Software Testing Qualifications Board*) na estruturação de casos de teste e defeitos.
2. **Uso Contextual de IA:** Utilização de modelos de linguagem como aceleradores do trabalho técnico, recebendo o contexto do projeto para gerar documentação técnica relevante.
3. **Visibilidade do Fluxo de Qualidade:** Acompanhamento integrado do estado do projeto por meio de painéis analíticos, cartões no Kanban e relatórios em múltiplos formatos.

---

## Quality Engineering Lifecycle

O ciclo de qualidade implementado no código do RAISE organiza-se nas seguintes etapas:

```text
[ Documentação de Projeto ]
         ↓
[ Personas & Histórias de Usuário ]
         ↓
[ Análise de Riscos (Matriz Probabilidade x Impacto) ]
         ↓
[ Casos de Teste (Padrão ISTQB) ]
         ↓
[ Relatório de Defeitos (Bug Reports) ]
         ↓
[ Acompanhamento no Quadro Kanban ]
         ↓
[ Métricas & Exportação de Relatórios ]
```

1. **Projetos e Documentos:** Cadastro de projetos e extração de texto de arquivos `.txt`, `.pdf` e `.docx`.
2. **Requisitos:** Criação e geração assistida de Personas, Histórias de Usuário e Matriz de Riscos.
3. **Casos de Teste:** Elaboração e execução de testes (Funcionais, Regressão, Smoke e Não-Funcionais) com pré-condições, passos e resultados esperados.
4. **Defeitos:** Registro de bugs com severidade, passos para reprodução e encaminhamento direto para o Kanban.
5. **Quadro Kanban:** Organização das atividades em colunas customizáveis, atribuição de responsáveis, inclusão de anexos e histórico de comentários.
6. **Métricas & Relatórios:** Visualização de indicadores de cobertura e exportação consolidada em CSV, Markdown e HTML completo.

---

## Current Features

- **Estrutura de Equipes e Permissões:**
  - Login e cadastro com armazenamento de hash de senha (`SHA-256`).
  - Isolamento de dados por Equipe (`teams` e `team_members`).
  - Controle de perfis (`Owner`, `Admin`, `Member`) e módulo `"👑 Painel Admin Master"`.
- **Módulo de Requisitos:**
  - Geração unificada via IA de Personas, Histórias de Usuário e Matriz de Riscos a partir do contexto do projeto.
  - Edição manual e controle de exclusão baseado em permissões.
- **Módulo de Testes e Qualidade:**
  - Criação de casos de teste individuais ou suítes completas com suporte de IA.
  - Execução interativa com status de aprovação/reprovação.
  - Gestão de defeitos com integração direta ao Kanban.
- **Quadro Kanban:**
  - Colunas personalizáveis com ordenação dinâmica.
  - Cartões com severidade visual, responsável, data e anexos no Supabase Storage.
  - Histórico de comentários por tarefa.
- **Perfil e Notificações:**
  - Central de notificações de tarefas atribuídas.
  - Edição de informações cadastrais e alteração de senha.
- **Exportação:**
  - Geração de planilhas CSV.
  - Geração de documentação em Markdown.
  - Emissão de relatórios em HTML estilizado com gráficos interativos do Plotly embutidos.

---

## Architecture

O sistema adota uma estrutura em camadas em Python:

- **Interface:** Streamlit (`app.py`), gerenciando o estado de sessão (`st.session_state`) e a navegação.
- **Camada de Visões (`views/`):** Telas do Kanban (`views/kanban/board.py`, `modals.py`) e perfil (`views/profile.py`).
- **Camada de Serviços (`services/`):** Centralização de operações de banco e storage em `services/kanban_service.py`.
- **Camada de Módulos (`modules/`):** Lógica de negócio segmentada (`auth`, `projects`, `requirements`, `test_cases`, `bug_reports`, `metrics`, `admin_panel`).
- **Persistência:** Supabase Client conectado a PostgreSQL e Supabase Storage.
- **Camada de IA:** Orquestrador em `config/ai_config.py` com suporte configurável a provedores (Groq, Google Gemini e OpenRouter).

---

## Technology Stack

Tecnologias identificadas no código-fonte e em `requirements.txt`:

| Camada | Tecnologia / Biblioteca | Versão Declarada |
|---|---|---|
| **Linguagem** | Python | `>=3.10` |
| **Interface Visual** | Streamlit | `>=1.30.0` |
| **Banco de Dados & Storage** | Supabase | `>=2.0.0` |
| **Inteligência Artificial** | Groq SDK | `>=0.4.0` |
| **Inteligência Artificial** | Google Generative AI | `>=0.3.0` |
| **Inteligência Artificial** | OpenAI SDK | `>=1.0.0` |
| **Processamento de Dados** | Pandas | `>=2.0.0` |
| **Visualização Gráfica** | Plotly | `>=5.18.0` |
| **Formatação Tabular** | Tabulate | — |
| **Manipulação de Documentos** | PyPDF | `>=3.0.0` |
| **Manipulação de Documentos** | Python-docx | `>=1.1.0` |
| **Configuração de Ambiente** | Python-dotenv | `>=1.0.0` |

---

## Project Structure

```text
raise/
├── .streamlit/
│   └── config.toml             # Tema e estilos da interface
├── app.py                      # Roteador principal da aplicação
├── requirements.txt            # Dependências Python
├── config/
│   ├── ai_config.py            # Orquestração de chamadas de IA e schemas ISTQB
│   └── database.py             # Conexão com o Supabase
├── modules/
│   ├── admin_panel.py          # Painel Administrativo Master
│   ├── auth.py                 # Autenticação e gestão de equipes
│   ├── bug_reports.py          # Gestão de defeitos
│   ├── metrics.py              # Dashboards e métricas
│   ├── projects.py             # Projetos e especificações
│   ├── requirements.py         # Personas, Histórias de Usuário e Riscos
│   ├── test_cases.py           # Gestão de Casos de Teste (ISTQB)
│   └── testing.py              # Fachada de integração do Módulo de Testes
├── services/
│   └── kanban_service.py       # Serviços do Kanban e anexos
├── utils/
│   ├── dateconvert.py          # Formatação de datas (padrão brasileiro)
│   ├── export.py               # Exportação (CSV, MD, HTML)
│   └── permissions.py          # Validação de permissões por perfil
└── views/
    ├── profile.py              # Perfil de usuário e notificações
    └── kanban/
        ├── __init__.py
        ├── board.py            # Renderização visual do quadro
        └── modals.py           # Modais de criação e edição
```

---

## Development Status

O repositório `raise` é o repositório principal e ativo do projeto. O código presente reúne as funcionalidades consolidadas a partir das fases de prototipação, testes de arquitetura e homologação.

---

## Evolution of the Project

O software atualmente denominado **RAISE** resultou de um processo iterativo de desenvolvimento que envolveu repositórios anteriores no GitHub:

- O projeto **não nasceu com o nome RAISE**; nos primeiros repositórios, a aplicação utilizava o título `"QA & Requisitos Hub"`.
- O repositório `qaboard` funcionou como protótipo inicial da proposta.
- Os repositórios `hubv2` e `qahub` registraram a evolução para arquitetura multiusuário e a inclusão de controles administrativos.
- O repositório `homolograise` serviu como ambiente de homologação, no qual o nome RAISE foi adotado, o Quadro Kanban foi introduzido e a estrutura de testes foi modularizada.
- O repositório `raise` apresenta a base organizada a partir desse percurso técnico.
- O software atualmente denominado **RAISE** é fruto de um processo iterativo e contínuo de engenharia, originado sob o título de concepção `"QA & Requisitos Hub"`.

O ciclo de desenvolvimento divide-se em marcos arquiteturais claros:

1. **Fase Prototipagem & Validação (Monólito Streamlit):** Consolidação das regras de negócio de Quality Engineering, conformidade com padrões ISTQB e orquestração de IA generativa (reunidas no histórico deste repositório).
2. **Fase Desacoplamento v1 (Front + Back):** Primeira cisão estrutural separando interface web dedicada e API de serviços.
3. **Fase Atual v2 (Front + Back - Em Desenvolvimento Ativo):** Refatoração da experiência do usuário, robustez no gerenciamento de estado e expansão contínua de funcionalidades.

---

## Historical Repositories

- [qaboard](https://github.com/qadtester/qaboard) — Prova de conceito funcional inicial.
- [hubv2](https://github.com/qadtester/hubv2) — Repositório utilizado para experimentação de gestão de equipes.
- [qahub](https://github.com/qadtester/qahub) — Repositório intermediário com painel administrativo e exportação.
- [homolograise](https://github.com/qadtester/homolograise) — Ambiente de homologação com introdução do nome RAISE e do Kanban.
A precedência temporal, originalidade e autoria da arquitetura são auditáveis via histórico de commits:

---

## Development Timeline

Datas e marcos registrados no histórico Git:

| Etapa | Repositório | Identidade Nominal Registrada|

| **Origem** | `qaboard` | QA & Requisitos Hub | 
| **Iteração Experimental** | `hubv2` | QA & Requisitos Hub | 
| **Desenvolvimento Intermediário** | `qahub` | QA & Requisitos Hub | 
| **Homologação** | `homolograise` | RAISE |
| **Referência Atual** | `raise` | RAISE |
| **Full Stack v1 & v2** | *Repositórios Dedicados* | RAISE | Em andamento | Em andamento | Ativo |

---

## Authorship and Development

- **Autoria e Direção Técnica:** Concepção, design de produto, regras de negócio e arquitetura original concebidas e coordenadas sob a identidade técnica `qadtester`.
- **Originalidade e Anterioridade:** O ecossistema RAISE e suas derivações arquiteturais (incluindo as versões desacopladas de Frontend e Backend) constituem propriedade intelectual original, respaldada pela cadeia temporal ininterrupta de repositórios registrada desde 10 de agosto de 2026.
- **Desenvolvimento Assistido por IA:** O projeto adota ferramentas de inteligência artificial generativa como aceleradores de implementação técnica (*AI-assisted development / vibecoding*), operadas sob curadoria, lógica de engenharia, validação funcional e refinamento humano exclusivo.
- **Status do Projeto:** O RAISE segue em ciclo de evolução contínua, com implementações e melhorias sendo aplicadas ativamente na arquitetura Full Stack.
  
---

## License

O uso, distribuição, visualização e eventual modificação deste código estão estritamente condicionados aos termos estabelecidos no arquivo formal de licença do projeto.

Consulte o arquivo [`LICENSE`](./LICENSE) na raiz do repositório para obter as condições legais vigentes e restrições de uso. Todos os direitos reservados, salvo disposição expressa no referido documento.

# Crypto Projects Screener Project Prompt with Enhanced Cursor Best Practices

## Objective
Develop a web-based crypto projects screener, accessible via a public URL, styled to resemble https://defillama.com/fees. The screener will display data from DeFiLlama and CoinMarketCap APIs (defined in `config.py`) in a sortable, filterable table of protocol metrics (fees, revenue, market cap, price). Use Cursor as the primary IDE, leveraging its AI-driven features (Composer, Agent, Notepads, Project Rules) for efficient development.

## Requirements

### Data Sources
- **DeFiLlama APIs** (no API key required):
  - Protocol list: `DEFILLAMA_PROTOCOLS_URL`.
  - Daily fees: `DEFILLAMA_FEES_OVERVIEW_URL`.
  - Daily revenue: `DEFILLAMA_REVENUE_OVERVIEW_URL`.
- **CoinMarketCap API**:
  - Latest listings: `COINMARKETCAP_LISTINGS_LATEST_URL` (requires API key).
  - Store API key in `.env` using `python-dotenv`.

### Backend
- **Language**: Python 3.11+.
- **Dependency Management**: Use `uv` for dependencies (`fastapi`, `uvicorn`, `requests`, `python-dotenv`, `duckdb`, `polars`, `requests_cache`, `pytest`).
- **API Key Management**: Load CoinMarketCap API key from `.env`.
- **Data Processing**:
  - Use `duckdb` for joins (e.g., merging protocol and market data).
  - Fallback to `polars`, then `pandas`.
  - Cache API responses with `requests_cache`.
- **API Server**:
  - Use `FastAPI` with endpoints:
    - `GET /protocols`: Returns protocol data (name, chain, category, fees, revenue, market cap, price).
    - `GET /filters`: Returns chains and protocol types.
  - Use Pydantic models, type hints, and docstrings for Cursor’s autocompletion.
- **Testing**:
  - Write `pytest` tests in `backend/tests/` (e.g., mock API responses with `requests_mock`).

### Frontend
- **Framework**: React with JSX, CDN-hosted (e.g., cdn.jsdelivr.net).
- **Styling**: Tailwind CSS (CDN) for a responsive, DeFiLlama-like design.
- **Features**:
  - Sortable table: Protocol Name, Chain, Category, Daily Fees, Daily Revenue, Market Cap, Price.
  - Filters: Chain, protocol type.
  - Search bar for protocol names.
  - Dark/light mode toggle.
- **Components**:
  - Modular components (`ProtocolTable.tsx`, `FilterPanel.tsx`, `SearchBar.tsx`).
  - Use TypeScript interfaces for props.
- **Testing**:
  - Use Jest and React Testing Library in `frontend/tests/`.

### Development Setup
- **Project Structure**:
  ```
  crypto-screener/
  ├── .cursor/
  │   ├── rules/
  │   │   ├── backend.mdc        # Python/FastAPI rules
  │   │   └── frontend.mdc       # React/Tailwind rules
  ├── backend/
  │   ├── src/
  │   │   ├── main.py           # FastAPI app
  │   │   ├── config.py         # API endpoints
  │   │   ├── api/
  │   │   │   ├── routes.py     # API routes
  │   │   │   └── models.py     # Pydantic models
  │   │   └── services/
  │   │       ├── data_fetch.py # API fetching
  │   │       └── data_process.py # Data processing
  │   ├── tests/
  │   │   └── test_routes.py    # Pytest tests
  │   ├── .env                  # API key
  │   └── requirements.txt      # uv-managed
  ├── frontend/
  │   ├── src/
  │   │   ├── components/
  │   │   │   ├── ProtocolTable.tsx
  │   │   │   ├── FilterPanel.tsx
  │   │   │   └── SearchBar.tsx
  │   │   └── App.tsx           # Main app
  │   ├── tests/
  │   │   └── ProtocolTable.test.tsx
  │   └── index.html            # Single-page app
  ├── docs/
  │   └── screener-prd.md       # PRD documentation
  ├── .gitignore                # Ignore .env, node_modules
  ├── uv.lock                   # uv lock file
  └── README.md                 # Setup instructions
  ```
- **Version Control**: Initialize Git, commit modular changes, use branches (e.g., `feature/table`).

### Cursor Best Practices
- **Project Rules (.mdc Files)**:
  - Store rules in `.cursor/rules/` as `.mdc` files (e.g., `backend.mdc`, `frontend.mdc`) for AI guidance [Web:0, Web:6, Web:10].
  - Example `backend.mdc`:
    ```
    --- 
    description: Python/FastAPI coding standards
    globs: ["backend/**/*.py"]
    alwaysApply: true
    ---
    # Python Backend Guidelines
    - Follow PEP 8 and use snake_case for variables/functions.
    - Use Pydantic for request/response models.
    - Prefer `duckdb` for data processing; fallback to `polars`, then `pandas`.
    - Example:
      ```python
      from pydantic import BaseModel
      class Protocol(BaseModel):
          name: str
          chain: str
      ```
    ```
  - Example `frontend.mdc`:
    ```
    --- 
    description: React/Tailwind coding standards
    globs: ["frontend/**/*.tsx"]
    alwaysApply: true
    ---
    # React Frontend Guidelines
    - Use functional components with TypeScript interfaces.
    - Apply Tailwind CSS classes for styling.
    - Example:
      ```tsx
      interface ProtocolProps { name: string; chain: string; }
      const ProtocolTable: React.FC<ProtocolProps> = ({ name, chain }) => (
        <div className="p-4 bg-gray-800 text-white">{name}</div>
      );
      ```
    ```
  - Reference `docs/screener-prd.md` in rules via `@docs` for context [Web:7, Web:10].
- **Markdown Documentation**:
  - Create `docs/screener-prd.md` for human-readable project details (e.g., PRD, architecture).
  - Example structure:
    ```
    # Crypto Screener PRD
    ## Overview
    A web-based screener for crypto protocols, styled like https://defillama.com/fees.
    ## Features
    - Sortable table with protocol metrics.
    - Filters by chain and protocol type.
    ## Tech Stack
    - Backend: Python, FastAPI, duckdb.
    - Frontend: React, Tailwind CSS.
    ```
  - Use Markdown for team sharing and external documentation, but reference in `.mdc` rules for AI context [Web:1, Web:14, Web:19].
- **YOLO Mode**: Enable in Cursor settings with prompt: “Allow tests (pytest, jest), build commands (uv pip compile, tsc), and file operations (mkdir, touch).” Iterate until tests pass [Web:4, Web:11].
- **Test-Driven Development**: Write tests first (e.g., `test_routes.py`, `ProtocolTable.test.tsx`), then code, using Composer to iterate until tests pass [Web:4].
- **Composer**: Use Cmd+K to scaffold multi-file structures (e.g., backend routes, frontend components) [Web:1, Web:6].
- **Notepads**: Create Notepads for reusable prompts (e.g., `FetchAPIData`, `CreateComponent`) and reference with `@notepad` [Web:11, Web:17].
- **Chat**: Use Cmd+L for debugging and brainstorming, including codebase context with Cmd+Enter [Web:1, Web:7].
- **Model Selection**: Use Claude 3.5 Sonnet for coding, GPT-4 (o1) for complex logic, GPT-4 Mini for quick tasks [Web:1].
- **Shortcuts**: Use Cmd+K (Composer), Cmd+L (Chat), Cmd+I (Chat to Composer) [Web:4, Web:7].
- **Terminal**: Run Git, `uv`, and tests in Cursor’s integrated terminal [Web:6, Web:11].
- **Rules Maintenance**: Update `.mdc` files with project changes, log errors in rules to refine AI behavior [Web:2, Web:7].

### Markdown vs. .cursorrules Decision
- **Why .mdc Files for Rules**:
  - `.mdc` files in `.cursor/rules/` are preferred over legacy `.cursorrules` due to deprecation and enhanced features (scoping, metadata, version control) [Web:0, Web:6, Web:10, Web:16].
  - They provide persistent AI context, auto-applied based on file patterns, reducing prompt repetition [Web:5, Web:15, Web:19].
  - Example: `backend.mdc` ensures Python code follows PEP 8, while `frontend.mdc` enforces React standards [Web:15].
- **Why Markdown for Documentation**:
  - Standalone Markdown files (e.g., `docs/screener-prd.md`) are ideal for human-readable documentation, shareable with teams or external stakeholders [Web:1, Web:7, Web:14].
  - They can be referenced in `.mdc` files or Notepads for AI context without cluttering rules [Web:7, Web:10, Web:19].
  - Markdown supports GitHub rendering and external tools, unlike `.mdc` files, which are Cursor-specific [Web:14, Post:7].
- **Hybrid Approach**:
  - Use `.mdc` files for AI coding rules to guide Cursor’s behavior.
  - Use Markdown files for PRDs and documentation, referenced in rules for context [Web:1, Web:14, Web:19, Post:1].
  - This balances AI integration with team accessibility, as recommended by forum users [Web:19, Post:7].

### Initial Steps
1. **Setup**:
   - Initialize with `uv init`, `git init`, and add dependencies via `uv add`.
   - Create `.env` and `.gitignore`.
   - Use Composer (Cmd+K) to scaffold structure, including `.cursor/rules/backend.mdc` and `frontend.mdc`.
2. **Rules**:
   - Create `backend.mdc` and `frontend.mdc` with coding standards.
   - Create `docs/screener-prd.md` and reference in rules.
3. **Backend**:
   - Implement `data_fetch.py`, `data_process.py`, and `routes.py`.
   - Write `pytest` tests and iterate with YOLO mode.
4. **Frontend**:
   - Build `index.html`, `App.tsx`, and components.
   - Write Jest tests and use Composer for iterations.
5. **Testing & Debugging**:
   - Run tests in Cursor’s terminal, debug with Chat (Cmd+L).
6. **Deployment**:
   - Deploy to Vercel/Render, verify URL.

### Deliverables
- Web page with sortable, filterable table.
- Source code with `.mdc` rules and Markdown PRD.
- Tests for backend and frontend.
- `README.md` with setup/deployment instructions.
- Git repository with clear commits.

### Notes
- Start with a minimal table, iterate with Composer.
- Secure `.env` in `.gitignore`.
- Handle API rate limits with caching and error handling.
- Regularly update `.mdc` files and check [forum.cursor.com](https://forum.cursor.com/) for Cursor updates [Web:12, Web:13].
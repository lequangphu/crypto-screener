# ETL & Dashboard Implementation Plan

## Task Tracking Checklist

### Phase 1: Refactor ETL Scripts for Modularity, Logging, and Error Handling
- [x] **Ingestion Layer (`ingest_data.py`)**
  - [x] Refactor API client(s) into separate functions/modules
  - [x] Refactor data normalization into its own function/module
  - [x] Refactor DB loading into its own function/module
  - [x] Add logging at each step (start, success, error)
  - [x] Implement retry logic for API calls (3 attempts, exponential backoff)
  - [ ] Parameterize for partial/full refreshes (optional)
  - [x] Handle nested data ingestion errors: serialize dict/list columns as JSON strings before loading into DuckDB
  - [x] Add fail-fast checks: exit with error if protocols data is missing or protocols_staging table is not created
- [x] **Transformation Layer (`transform_data.py`)**
  - [x] Refactor each transformation step into a modular function
  - [x] Add logging for each transformation step (row counts, summaries)
  - [x] Add validation: ensure `revenue` and `fees` fields in revenue table are non-null (log error if not)
  - [x] Add fail-fast check: exit with error if protocols_staging table is missing before transformation

### Phase 2: Implement Data Export to JSON for Dashboard Use
- [x] **Export Logic**
  - [x] Export each relevant table as a separate JSON file to `data/exports/`
  - [x] Only include columns needed for the dashboard
- [x] **Directory Management**
  - [x] Ensure `data/exports/` exists or create it if missing

### Phase 3: Set Up React Dashboard to Fetch and Visualize Exported Data
- [x] **If React app is in this repo:**
  - [x] Create a minimal React dashboard (or stub) that fetches JSON files from `data/exports/`
  - [x] Visualize the data (basic table or chart)
  - [x] Fix Vite base path for GitHub Pages deployment (`base: '/crypto-screener/'` in vite.config.js)
  - [x] Update React data fetch paths to use correct relative URLs (`data/exports/fees_analysis.json` etc.)
  - [x] Update workflow to copy data export JSON files into dashboard build output before deploy
  - [x] Add manual workflow_dispatch trigger for manual runs
  - [x] Add troubleshooting and debugging steps for blank screen, 404s, and data loading issues
- [x] **If React app is not in this repo:**
  - [x] Document the data contract (JSON structure, file names, sample data) for frontend integration

---

## Phase 1: Refactor ETL Scripts for Modularity, Logging, and Error Handling

1. **Ingestion Layer (`ingest_data.py`):**
   - Split into: API client(s), normalization, and DB loading functions.
   - Add logging at each step (start, success, error).
   - Implement retry logic for API calls (e.g., 3 attempts with exponential backoff).
   - Parameterize for partial/full refreshes (optional, if time allows).
   - Handle nested data ingestion errors: serialize dict/list columns as JSON strings before loading into DuckDB
   - Add fail-fast checks: exit with error if protocols data is missing or protocols_staging table is not created

2. **Transformation Layer (`transform_data.py`):**
   - Refactor into modular functions (one per join/enrichment).
   - Add logging for each transformation step (row counts, summaries).
   - Add validation: after transforming the revenue table, check that `revenue` and `fees` fields are non-null (log error if not).
   - Add fail-fast check: exit with error if protocols_staging table is missing before transformation

---

## Phase 2: Implement Data Export to JSON for Dashboard Use

1. **Export Logic:**
   - After transformation, export each relevant table as a separate JSON file to `data/exports/`.
   - Only include columns needed for the dashboard (to be determined from current dashboard requirements or by reviewing the code).

2. **Directory Management:**
   - Ensure `data/exports/` exists or create it if missing.

---

## Phase 3: Set Up React Dashboard to Fetch and Visualize Exported Data

1. **(If React app is in scope for this repo):**
   - Create a minimal React dashboard (or stub) that fetches the JSON files from `data/exports/`.
   - Visualize the data (basic table or chart for now).

2. **(If React app is not in this repo):**
   - Document the data contract (JSON structure, file names, sample data) for easy frontend integration. 
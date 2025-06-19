# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

## Data Integration

This dashboard loads protocol analysis data from `public/analysis.json`.

### How to update/copy the data

1. Run the ETL/export pipeline in the project root to generate or update `data/exports/analysis.json`.
2. Copy the file into the dashboard's public directory:
   ```bash
   cp ../data/exports/analysis.json public/
   ```
3. Refresh the dashboard in your browser to see the latest data.

### Data Contract
- **File:** `analysis.json`
- **Location:** `/public/analysis.json` (served at `/analysis.json`)
- **Format:** Array of objects (one per protocol)
- **Sample Schema:**
  ```json
  [
    {
      "total30d": 12345.67,
      "total1y": 456789.01,
      "change_30dover30d": 0.12,
      "name": "ProtocolX",
      "category": "DeFi",
      "fully_diluted_market_cap": 123456789,
      "fees_forward_1y": 148148.04,
      "revenue_forward_1y": 148148.04,
      "pf_ratio_1y": 10.5,
      "pr_ratio_1y": 12.3,
      "pf_ratio_forward_1y": 9.8,
      "pr_ratio_forward_1y": 11.2,
      "fees_change_7d": 0.05,
      "revenue_change_7d": 0.04
    }
  ]
  ```
- **Fields:**
  - `total30d`, `total1y`: Numeric, protocol fees/revenue over 30 days/1 year
  - `change_30dover30d`: Numeric, percent change
  - `name`: String, protocol name
  - `category`: String, protocol category
  - `fully_diluted_market_cap`: Numeric
  - `fees_forward_1y`, `revenue_forward_1y`: Numeric, projected
  - `pf_ratio_1y`, `pr_ratio_1y`, `pf_ratio_forward_1y`, `pr_ratio_forward_1y`: Numeric, ratios
  - `fees_change_7d`, `revenue_change_7d`: Numeric, 7-day change

- **Update Frequency:** Whenever the ETL pipeline is run and the file is copied.
- **Access Method:** HTTP GET `/analysis.json` (static file)

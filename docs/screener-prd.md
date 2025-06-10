# Crypto Projects Screener Project Prompt with Enhanced Cursor Best Practices

## Objective
Develop a screener of projects. The screener will display data from DeFiLlama and CoinMarketCap APIs in a sortable, filterable table of protocol metrics (fees, revenue, market cap, price). Use Cursor as the primary IDE, leveraging its AI-driven features (Composer, Agent, Notepads, Project Rules) for efficient development.

## Requirements

### Data Sources
- **DeFiLlama APIs** (no API key required):
  - Protocol list: `DEFILLAMA_PROTOCOLS_URL`.
  - Daily fees: `DEFILLAMA_FEES_OVERVIEW_URL`.
  - Daily revenue: `DEFILLAMA_REVENUE_OVERVIEW_URL`.
- **CoinMarketCap API**:
  - Latest listings: `COINMARKETCAP_LISTINGS_LATEST_URL` (requires API key).

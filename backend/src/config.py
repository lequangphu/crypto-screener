import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# DeFiLlama API
DEFILLAMA_BASE_URL = "https://api.llama.fi"

# Endpoint for fetching a list of all protocols
DEFILLAMA_PROTOCOLS_URL = f"{DEFILLAMA_BASE_URL}/protocols"

# Endpoints for aggregated fees and revenue data across all protocols (historical data included)
DEFILLAMA_FEES_OVERVIEW_URL = f"{DEFILLAMA_BASE_URL}/overview/fees?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true&dataType=dailyFees"
DEFILLAMA_REVENUE_OVERVIEW_URL = f"{DEFILLAMA_BASE_URL}/overview/fees?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true&dataType=dailyRevenue"

# CoinMarketCap API
COINMARKETCAP_API_URL = "https://pro-api.coinmarketcap.com"
COINMARKETCAP_LISTINGS_LATEST_URL = f"{COINMARKETCAP_API_URL}/v1/cryptocurrency/listings/latest"
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
import requests
from requests_cache import CachedSession
import logging

from config import DEFILLAMA_PROTOCOLS_URL, DEFILLAMA_FEES_OVERVIEW_URL, DEFILLAMA_REVENUE_OVERVIEW_URL, COINMARKETCAP_LISTINGS_LATEST_URL, COINMARKETCAP_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

session = CachedSession('demo_cache', backend='sqlite', expire_after=3600)

def fetch_defillama_protocols():
    try:
        response = session.get(DEFILLAMA_PROTOCOLS_URL)
        response.raise_for_status()
        protocols_raw_data = response.json()
        logger.info(f"Successfully fetched {len(protocols_raw_data)} protocols from DeFiLlama")
        return protocols_raw_data
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching DeFiLlama protocols: {str(e)}")
        return []

def fetch_defillama_fees_overview():
    try:
        response = session.get(DEFILLAMA_FEES_OVERVIEW_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching DeFiLlama fees overview: {str(e)}")
        return {"protocols": []}

def fetch_defillama_revenue_overview():
    try:
        response = session.get(DEFILLAMA_REVENUE_OVERVIEW_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching DeFiLlama revenue overview: {str(e)}")
        return {"protocols": []}

def fetch_coinmarketcap_listings():
    if not COINMARKETCAP_API_KEY:
        logger.warning("CoinMarketCap API key not found")
        return {"data": []}
        
    try:
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
        }
        response = session.get(COINMARKETCAP_LISTINGS_LATEST_URL, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching CoinMarketCap listings: {str(e)}")
        return {"data": []} 
import requests
from requests_cache import CachedSession

from ..config import DEFILLAMA_PROTOCOLS_URL, DEFILLAMA_FEES_OVERVIEW_URL, DEFILLAMA_REVENUE_OVERVIEW_URL, COINMARKETCAP_LISTINGS_LATEST_URL, COINMARKETCAP_API_KEY

session = CachedSession('demo_cache', backend='sqlite', expire_after=3600)

def fetch_defillama_protocols():
    response = session.get(DEFILLAMA_PROTOCOLS_URL)
    response.raise_for_status()
    protocols_raw_data = response.json()
    print("DefiLlama Protocols Raw Data:", protocols_raw_data)
    return protocols_raw_data

def fetch_defillama_fees_overview():
    response = session.get(DEFILLAMA_FEES_OVERVIEW_URL)
    response.raise_for_status()
    return response.json()

def fetch_defillama_revenue_overview():
    response = session.get(DEFILLAMA_REVENUE_OVERVIEW_URL)
    response.raise_for_status()
    return response.json()

def fetch_coinmarketcap_listings():
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
    }
    response = session.get(COINMARKETCAP_LISTINGS_LATEST_URL, headers=headers)
    response.raise_for_status()
    return response.json() 
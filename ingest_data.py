import requests
import duckdb
import pandas as pd
import os
import logging
from dotenv import load_dotenv
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

load_dotenv() # Load environment variables from .env file

# API Endpoints from prd.md
DEFILLAMA_PROTOCOLS_ENDPOINT = "https://api.llama.fi/protocols"
DEFILLAMA_FEES_OVERVIEW_ENDPOINT = "https://api.llama.fi/overview/fees?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true&dataType=dailyFees"
DEFILLAMA_REVENUE_OVERVIEW_ENDPOINT = "https://api.llama.fi/overview/fees?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true&dataType=dailyRevenue"
COINMARKETCAP_LISTINGS_LATEST_ENDPOINT = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=5000"

DUCKDB_DATABASE_PATH = "data/crypto.duckdb"

def fetch_data(url, headers=None, max_retries=3, backoff_factor=1.0):
    """Fetches data from a given URL with retry logic."""
    for attempt in range(1, max_retries + 1):
        try:
            logging.info(f"Fetching data from {url} (attempt {attempt})")
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            logging.info(f"Successfully fetched data from {url}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt} failed for {url}: {e}")
            if attempt < max_retries:
                sleep_time = backoff_factor * (2 ** (attempt - 1))
                logging.info(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                logging.error(f"Error fetching data from {url} after {max_retries} attempts: {e}")
    return None

def fetch_defillama_protocols():
    return fetch_data(DEFILLAMA_PROTOCOLS_ENDPOINT)

def fetch_defillama_fees_overview():
    return fetch_data(DEFILLAMA_FEES_OVERVIEW_ENDPOINT)

def fetch_defillama_revenue_overview():
    return fetch_data(DEFILLAMA_REVENUE_OVERVIEW_ENDPOINT)

def fetch_coinmarketcap_listings(api_key):
    coinmarketcap_data_list = []
    if not api_key:
        logging.warning("COINMARKETCAP_API_KEY environment variable not set. Skipping CoinMarketCap data fetch.")
        return None
    headers = {"X-CMC_PRO_API_KEY": api_key}
    start = 1
    limit = 5000  # Fetch 5000 records at a time
    while True:
        paginated_url = f"{COINMARKETCAP_LISTINGS_LATEST_ENDPOINT.split('?')[0]}?start={start}&limit={limit}"
        logging.info(f"Fetching from: {paginated_url}")
        current_data = fetch_data(paginated_url, headers)
        if current_data and 'data' in current_data:
            coinmarketcap_data_list.extend(current_data['data'])
            if len(current_data['data']) < limit:
                break
            start += limit
        else:
            break
    if coinmarketcap_data_list:
        logging.info("Successfully fetched CoinMarketCap listings data.")
    else:
        logging.warning("No CoinMarketCap data fetched.")
    return {'data': coinmarketcap_data_list} if coinmarketcap_data_list else None

def normalize_protocols_data(raw_data):
    if not raw_data:
        return None
    return pd.DataFrame(raw_data)

def normalize_fees_overview_data(raw_data):
    if not raw_data or 'protocols' not in raw_data:
        return None
    return pd.DataFrame(raw_data['protocols'])

def normalize_revenue_overview_data(raw_data):
    if not raw_data or 'protocols' not in raw_data:
        return None
    return pd.DataFrame(raw_data['protocols'])

def normalize_coinmarketcap_data(raw_data):
    if not raw_data or 'data' not in raw_data:
        return None
    return pd.DataFrame(raw_data['data'])

def load_dataframe_to_duckdb(con, df, table_name):
    if df is None:
        return
    con.execute(f"DROP TABLE IF EXISTS {table_name};")
    con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")

def main():
    # Fetch DeFiLlama Data
    logging.info("Fetching DeFiLlama Protocols data...")
    protocols_data = fetch_defillama_protocols()
    logging.info("Fetching DeFiLlama Fees Overview data...")
    fees_overview_data = fetch_defillama_fees_overview()
    logging.info("Fetching DeFiLlama Revenue Overview data...")
    revenue_overview_data = fetch_defillama_revenue_overview()
    # Fetch CoinMarketCap Data with pagination
    coinmarketcap_api_key = os.getenv("COINMARKETCAP_API_KEY")
    logging.info("Fetching CoinMarketCap Listings Latest data with pagination...")
    coinmarketcap_data = fetch_coinmarketcap_listings(coinmarketcap_api_key)

    # Normalize data
    logging.info("Normalizing data...")
    df_protocols = normalize_protocols_data(protocols_data)
    df_fees_overview = normalize_fees_overview_data(fees_overview_data)
    df_revenue_overview = normalize_revenue_overview_data(revenue_overview_data)
    df_coinmarketcap = normalize_coinmarketcap_data(coinmarketcap_data)
    logging.info("Data normalization complete.")

    # Initialize DuckDB connection to a persistent file
    con = duckdb.connect(database=DUCKDB_DATABASE_PATH, read_only=False)

    # Load data into DuckDB tables
    try:
        load_dataframe_to_duckdb(con, df_protocols, "protocols_staging")
        logging.info("Protocols data ingested into DuckDB.")
    except Exception as e:
        logging.error(f"Error ingesting protocols data into DuckDB: {e}")
    try:
        load_dataframe_to_duckdb(con, df_fees_overview, "fees_overview_staging")
        logging.info("Fees Overview data ingested into DuckDB.")
    except Exception as e:
        logging.error(f"Error ingesting fees_overview data into DuckDB: {e}")
    try:
        load_dataframe_to_duckdb(con, df_revenue_overview, "revenue_overview_staging")
        logging.info("Revenue Overview data ingested into DuckDB.")
    except Exception as e:
        logging.error(f"Error ingesting revenue_overview data into DuckDB: {e}")
    try:
        load_dataframe_to_duckdb(con, df_coinmarketcap, "coinmarketcap_staging")
        logging.info("CoinMarketCap data ingested into DuckDB.")
    except Exception as e:
        logging.error(f"Error ingesting coinmarketcap data into DuckDB: {e}")

    logging.info(f"Raw data successfully ingested into {DUCKDB_DATABASE_PATH}")
    con.close()

if __name__ == "__main__":
    main() 
import requests
import duckdb
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# API Endpoints from prd.md
DEFILLAMA_PROTOCOLS_ENDPOINT = "https://api.llama.fi/protocols"
DEFILLAMA_FEES_OVERVIEW_ENDPOINT = "https://api.llama.fi/overview/fees?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true&dataType=dailyFees"
DEFILLAMA_REVENUE_OVERVIEW_ENDPOINT = "https://api.llama.fi/overview/fees?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true&dataType=dailyRevenue"
COINMARKETCAP_LISTINGS_LATEST_ENDPOINT = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=5000"

DUCKDB_DATABASE_PATH = "data/crypto.duckdb"

def fetch_data(url, headers=None):
    """Fetches data from a given URL."""
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def main():
    # Fetch DeFiLlama Data
    print("Fetching DeFiLlama Protocols data...")
    protocols_data = fetch_data(DEFILLAMA_PROTOCOLS_ENDPOINT)

    print("Fetching DeFiLlama Fees Overview data...")
    fees_overview_data = fetch_data(DEFILLAMA_FEES_OVERVIEW_ENDPOINT)

    print("Fetching DeFiLlama Revenue Overview data...")
    revenue_overview_data = fetch_data(DEFILLAMA_REVENUE_OVERVIEW_ENDPOINT)

    # Fetch CoinMarketCap Data with pagination
    coinmarketcap_api_key = os.getenv("COINMARKETCAP_API_KEY")
    coinmarketcap_data_list = []
    if not coinmarketcap_api_key:
        print("COINMARKETCAP_API_KEY environment variable not set. Skipping CoinMarketCap data fetch.")
    else:
        print("Fetching CoinMarketCap Listings Latest data with pagination...")
        headers = {"X-CMC_PRO_API_KEY": coinmarketcap_api_key}
        start = 1
        limit = 5000  # Fetch 5000 records at a time
        while True:
            paginated_url = f"{COINMARKETCAP_LISTINGS_LATEST_ENDPOINT.split('?')[0]}?start={start}&limit={limit}"
            print(f"Fetching from: {paginated_url}")
            current_data = fetch_data(paginated_url, headers)
            if current_data and 'data' in current_data:
                coinmarketcap_data_list.extend(current_data['data'])
                if len(current_data['data']) < limit:
                    # Less data than limit, means we reached the end
                    break
                start += limit
            else:
                break
    coinmarketcap_data = {'data': coinmarketcap_data_list} if coinmarketcap_data_list else None

    # Initialize DuckDB connection to a persistent file
    con = duckdb.connect(database=DUCKDB_DATABASE_PATH, read_only=False)

    # Load data into DuckDB tables
    if protocols_data:
        try:
            df_protocols = pd.DataFrame(protocols_data)
            con.execute("DROP TABLE IF EXISTS protocols;") # Drop if exists to ensure fresh data
            con.execute("CREATE TABLE protocols AS SELECT * FROM df_protocols")
            print("Protocols data ingested into DuckDB.")
        except Exception as e:
            print(f"Error ingesting protocols data into DuckDB: {e}")

    if fees_overview_data and 'protocols' in fees_overview_data:
        try:
            df_fees_overview = pd.DataFrame(fees_overview_data['protocols'])
            con.execute("DROP TABLE IF EXISTS fees_overview;")
            con.execute("CREATE TABLE fees_overview AS SELECT * FROM df_fees_overview")
            print("Fees Overview data ingested into DuckDB.")
        except Exception as e:
            print(f"Error ingesting fees_overview data into DuckDB: {e}")

    if revenue_overview_data and 'protocols' in revenue_overview_data:
        try:
            df_revenue_overview = pd.DataFrame(revenue_overview_data['protocols'])
            con.execute("DROP TABLE IF EXISTS revenue_overview;")
            con.execute("CREATE TABLE revenue_overview AS SELECT * FROM df_revenue_overview")
            print("Revenue Overview data ingested into DuckDB.")
        except Exception as e:
            print(f"Error ingesting revenue_overview data into DuckDB: {e}")

    if coinmarketcap_data and 'data' in coinmarketcap_data:
        try:
            df_coinmarketcap = pd.DataFrame(coinmarketcap_data['data'])
            con.execute("DROP TABLE IF EXISTS coinmarketcap;")
            con.execute("CREATE TABLE coinmarketcap AS SELECT * FROM df_coinmarketcap")
            print("CoinMarketCap data ingested into DuckDB.")
        except Exception as e:
            print(f"Error ingesting coinmarketcap data into DuckDB: {e}")

    print(f"\nRaw data successfully ingested into {DUCKDB_DATABASE_PATH}")
    con.close()

if __name__ == "__main__":
    main() 
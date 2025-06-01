import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the .env file in the parent directory
dotenv_path = os.path.join(script_dir, os.pardir, '.env')

# Load environment variables from the .env file in the parent directory
load_dotenv(dotenv_path=dotenv_path)

COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
COINMARKETCAP_LISTINGS_LATEST_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

# Define a default limit for CoinMarketCap listings. Free plans usually have a limit of 100, while paid plans can go up to 5000.
DEFAULT_CMC_LISTINGS_LIMIT = 5000

# Assuming config.py is in the same directory
from config import (
    DEFILLAMA_PROTOCOLS_URL,
    DEFILLAMA_FEES_OVERVIEW_URL,
    DEFILLAMA_REVENUE_OVERVIEW_URL,
    COINMARKETCAP_API_URL # Import the new API URL
)

DATA_DIR = "raw_data"
DOCS_DIR = "docs"

def fetch_data(url, headers=None, params=None):
    """Fetches data from the given URL with optional headers and parameters."""
    print(f"Fetching data from: {url}")
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def save_raw_data(data, filename_prefix):
    """Saves raw data to a JSON file in the DATA_DIR, overwriting if exists."""
    os.makedirs(DATA_DIR, exist_ok=True)
    # Removed timestamp for overwriting behavior
    filepath = os.path.join(DATA_DIR, f"{filename_prefix}.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Raw data saved to {filepath}")
    return filepath

def describe_columns(data, endpoint_name, level=0):
    """Generates a markdown string describing the columns of the data in a tree-like structure."""
    indentation = "  " * level
    description = ""

    if level == 0:
        description += f"# {endpoint_name} Data Structure\n\n"

    if isinstance(data, dict):
        if level > 0: # Add a header for nested dictionaries
            description += f"{indentation}- Type: `dict`\n"
        for key, value in data.items():
            col_type = type(value).__name__
            description += f"{indentation}- `{key}`: `{col_type}`\n"
            if isinstance(value, (list, dict)) and value:
                nested_endpoint_name = f"{endpoint_name}.{key}"
                description += describe_columns(value, nested_endpoint_name, level + 1)

    elif isinstance(data, list) and data:
        sample_entry = data[0]
        col_type = type(sample_entry).__name__
        description += f"{indentation}- Type: `list` (contains `{col_type}` elements)\n"
        if isinstance(sample_entry, (dict, list)):
            nested_endpoint_name = f"{endpoint_name}[]"
            description += describe_columns(sample_entry, nested_endpoint_name, level + 1)
        # No need to print primitive list contents again as type is already stated

    else:
        # This handles primitive types at any level, or empty structures
        if level == 0: # Only print for top-level non-dict/list
            description += f"{indentation}Raw data type: {type(data).__name__}\n"
            description += f"{indentation}Raw data sample: {str(data)[:200]}...\n"
        
    return description

def generate_markdown_file(content, filename_prefix):
    """Generates a markdown file in the DOCS_DIR."""
    os.makedirs(DOCS_DIR, exist_ok=True)
    filepath = os.path.join(DOCS_DIR, f"{filename_prefix}_data_dictionary.md")
    with open(filepath, "w") as f:
        f.write(content)
    print(f"Data dictionary saved to {filepath}")
    return filepath

def process_endpoint(url, filename_prefix, endpoint_name, headers=None, params=None):
    print(f"\n--- Processing {endpoint_name} ---")
    data = fetch_data(url, headers, params)

    if data:
        save_raw_data(data, filename_prefix)
        markdown_content = describe_columns(data, endpoint_name)
        generate_markdown_file(markdown_content, filename_prefix)
    else:
        print(f"Failed to fetch {endpoint_name} data. Skipping data saving and documentation generation.")

if __name__ == "__main__":
    # Process DeFiLlama Protocols endpoint
    process_endpoint(DEFILLAMA_PROTOCOLS_URL, "defillama_protocols", "DeFiLlama Protocols")

    # Process DeFiLlama Fees Overview endpoint
    process_endpoint(DEFILLAMA_FEES_OVERVIEW_URL, "defillama_fees_overview", "DeFiLlama Fees Overview")

    # Process DeFiLlama Revenue Overview endpoint
    process_endpoint(DEFILLAMA_REVENUE_OVERVIEW_URL, "defillama_revenue_overview", "DeFiLlama Revenue Overview")

    # --- New code for CoinMarketCap listings endpoint ---
    if COINMARKETCAP_API_KEY:
        cmc_headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
        }
        # The listings/latest endpoint takes 'start' and 'limit' parameters.
        # Max limit is usually 5000 for listings/latest on paid plans, 100 on free.
        cmc_params = {
            'start': '1',
            'limit': '5000' # Fetch up to 5000 listings
        }
        process_endpoint(COINMARKETCAP_LISTINGS_LATEST_URL, "coinmarketcap_listings_latest", "CoinMarketCap Listings Latest", headers=cmc_headers, params=cmc_params)
    else:
        print("\nSkipping CoinMarketCap Listings fetch: COINMARKETCAP_API_KEY is not set.") 
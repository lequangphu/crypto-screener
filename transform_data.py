import duckdb
import pandas as pd

DUCKDB_DATABASE_PATH = "data/crypto.duckdb"

def main():
    con = duckdb.connect(database=DUCKDB_DATABASE_PATH, read_only=False)

    # Add cmcId from protocols to fees_overview table
    print("Adding cmcId from protocols to fees_transformed table...")
    con.execute("""
        CREATE OR REPLACE TABLE fees_transformed AS
        SELECT
            fo.*,
            p.cmcId AS cmcId
        FROM fees_overview_staging fo
        LEFT JOIN protocols_staging p ON fo.id = p.id;
    """)
    print("cmcId from protocols added to fees_transformed table.")

    # Add fully_diluted_market_cap from coinmarketcap to fees_transformed table
    print("Adding fully_diluted_market_cap to fees_transformed table...")
    con.execute("""
        CREATE OR REPLACE TABLE fees_transformed AS
        SELECT
            fo.*,
            cmc.quote.USD.fully_diluted_market_cap
        FROM fees_transformed fo
        LEFT JOIN coinmarketcap_staging cmc ON fo.cmcId::BIGINT = cmc.id;
    """)
    print("fully_diluted_market_cap added to fees_transformed table.")

    # Add cmcId from protocols to revenue_overview table
    print("Adding cmcId from protocols to revenue_transformed table...")
    con.execute("""
        CREATE OR REPLACE TABLE revenue_transformed AS
        SELECT
            ro.*,
            p.cmcId AS cmcId
        FROM revenue_overview_staging ro
        LEFT JOIN protocols_staging p ON ro.id = p.id;
    """)
    print("cmcId from protocols added to revenue_transformed table.")

    # Add fully_diluted_market_cap from coinmarketcap to revenue_overview table
    print("Adding fully_diluted_market_cap to revenue_transformed table...")
    con.execute("""
        CREATE OR REPLACE TABLE revenue_transformed AS
        SELECT
            ro.*,
            cmc.quote.USD.fully_diluted_market_cap
        FROM revenue_transformed ro
        LEFT JOIN coinmarketcap_staging cmc ON ro.cmcId::BIGINT = cmc.id;
    """)
    print("fully_diluted_market_cap added to revenue_transformed table.")

    con.close()
    print(f"Data transformation complete. cmcId and fully_diluted_market_cap added to fees_transformed and revenue_transformed in {DUCKDB_DATABASE_PATH}")

if __name__ == "__main__":
    main() 
import duckdb
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

DUCKDB_DATABASE_PATH = "data/crypto.duckdb"

def add_cmcid_to_fees(con):
    logging.info("Adding cmcId from protocols to fees_transformed table...")
    con.execute("""
        CREATE OR REPLACE TABLE fees_transformed AS
        SELECT
            fo.*,
            p.cmcId AS cmcId
        FROM fees_overview_staging fo
        LEFT JOIN protocols_staging p ON fo.id = p.id;
    """)
    row_count = con.execute("SELECT COUNT(*) FROM fees_transformed").fetchone()[0]
    logging.info(f"cmcId from protocols added to fees_transformed table. Row count: {row_count}")

def add_fully_diluted_market_cap_to_fees(con):
    logging.info("Adding fully_diluted_market_cap to fees_transformed table...")
    con.execute("""
        CREATE OR REPLACE TABLE fees_transformed AS
        SELECT
            fo.*,
            cmc.quote.USD.fully_diluted_market_cap
        FROM fees_transformed fo
        LEFT JOIN coinmarketcap_staging cmc ON fo.cmcId::BIGINT = cmc.id;
    """)
    row_count = con.execute("SELECT COUNT(*) FROM fees_transformed").fetchone()[0]
    logging.info(f"fully_diluted_market_cap added to fees_transformed table. Row count: {row_count}")

def add_cmcid_to_revenue(con):
    logging.info("Adding cmcId from protocols to revenue_transformed table...")
    con.execute("""
        CREATE OR REPLACE TABLE revenue_transformed AS
        SELECT
            ro.*,
            p.cmcId AS cmcId
        FROM revenue_overview_staging ro
        LEFT JOIN protocols_staging p ON ro.id = p.id;
    """)
    row_count = con.execute("SELECT COUNT(*) FROM revenue_transformed").fetchone()[0]
    logging.info(f"cmcId from protocols added to revenue_transformed table. Row count: {row_count}")

def add_fully_diluted_market_cap_to_revenue(con):
    logging.info("Adding fully_diluted_market_cap to revenue_transformed table...")
    con.execute("""
        CREATE OR REPLACE TABLE revenue_transformed AS
        SELECT
            ro.*,
            cmc.quote.USD.fully_diluted_market_cap
        FROM revenue_transformed ro
        LEFT JOIN coinmarketcap_staging cmc ON ro.cmcId::BIGINT = cmc.id;
    """)
    row_count = con.execute("SELECT COUNT(*) FROM revenue_transformed").fetchone()[0]
    logging.info(f"fully_diluted_market_cap added to revenue_transformed table. Row count: {row_count}")

def validate_revenue_and_fees_non_null(con):
    logging.info("Validating that 'revenue' and 'fees' fields in revenue_transformed are non-null...")
    null_revenue_count = con.execute("SELECT COUNT(*) FROM revenue_transformed WHERE revenue IS NULL").fetchone()[0]
    null_fees_count = con.execute("SELECT COUNT(*) FROM revenue_transformed WHERE fees IS NULL").fetchone()[0]
    if null_revenue_count > 0 or null_fees_count > 0:
        logging.error(f"Validation failed: {null_revenue_count} rows with NULL revenue, {null_fees_count} rows with NULL fees in revenue_transformed.")
    else:
        logging.info("Validation passed: No NULL values in 'revenue' or 'fees' fields in revenue_transformed.")

def main():
    con = duckdb.connect(database=DUCKDB_DATABASE_PATH, read_only=False)
    add_cmcid_to_fees(con)
    add_fully_diluted_market_cap_to_fees(con)
    add_cmcid_to_revenue(con)
    add_fully_diluted_market_cap_to_revenue(con)
    validate_revenue_and_fees_non_null(con)
    con.close()
    logging.info(f"Data transformation complete. cmcId and fully_diluted_market_cap added to fees_transformed and revenue_transformed in {DUCKDB_DATABASE_PATH}")

if __name__ == "__main__":
    main() 
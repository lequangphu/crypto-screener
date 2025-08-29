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
            json_extract_string(cmc.quote, '$.USD.fully_diluted_market_cap')::DOUBLE AS fully_diluted_market_cap
        FROM fees_transformed fo
        LEFT JOIN coinmarketcap_staging cmc
          ON try_cast(fo.cmcId AS BIGINT) IS NOT NULL
         AND try_cast(fo.cmcId AS BIGINT) = cmc.id;
    """)
    row_count = con.execute("SELECT COUNT(*) FROM fees_transformed").fetchone()[0]
    logging.info(f"fully_diluted_market_cap added to fees_transformed table. Row count: {row_count}")

def add_cmcid_and_slug_to_fees(con):
    logging.info("Adding cmcId and slug from protocols to fees_transformed table...")
    con.execute("""
        CREATE OR REPLACE TABLE fees_transformed AS
        SELECT
            fo.*,
            try_cast(p.cmcId AS BIGINT) AS cmcId,
            p.slug AS slug
        FROM fees_overview_staging fo
        LEFT JOIN protocols_staging p ON fo.id = p.id;
    """)
    row_count = con.execute("SELECT COUNT(*) FROM fees_transformed").fetchone()[0]
    logging.info(f"cmcId and slug from protocols added to fees_transformed table. Row count: {row_count}")

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
            json_extract_string(cmc.quote, '$.USD.fully_diluted_market_cap')::DOUBLE AS fully_diluted_market_cap
        FROM revenue_transformed ro
        LEFT JOIN coinmarketcap_staging cmc
          ON try_cast(ro.cmcId AS BIGINT) IS NOT NULL
         AND try_cast(ro.cmcId AS BIGINT) = cmc.id;
    """)
    row_count = con.execute("SELECT COUNT(*) FROM revenue_transformed").fetchone()[0]
    logging.info(f"fully_diluted_market_cap added to revenue_transformed table. Row count: {row_count}")

def add_cmcid_and_slug_to_revenue(con):
    logging.info("Adding cmcId and slug from protocols to revenue_transformed table...")
    con.execute("""
        CREATE OR REPLACE TABLE revenue_transformed AS
        SELECT
            ro.*,
            try_cast(p.cmcId AS BIGINT) AS cmcId,
            p.slug AS slug
        FROM revenue_overview_staging ro
        LEFT JOIN protocols_staging p ON ro.id = p.id;
    """)
    row_count = con.execute("SELECT COUNT(*) FROM revenue_transformed").fetchone()[0]
    logging.info(f"cmcId and slug from protocols added to revenue_transformed table. Row count: {row_count}")

def main():
    con = duckdb.connect(database=DUCKDB_DATABASE_PATH, read_only=False)
    # Pre-check for protocols_staging table
    table_exists = con.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'protocols_staging'").fetchone()[0]
    if table_exists == 0:
        logging.error("protocols_staging table does not exist. Exiting transformation.")
        con.close()
        exit(1)
    add_cmcid_and_slug_to_fees(con)
    add_fully_diluted_market_cap_to_fees(con)
    add_cmcid_and_slug_to_revenue(con)
    add_fully_diluted_market_cap_to_revenue(con)
    con.close()
    logging.info(f"Data transformation complete. cmcId, slug, and fully_diluted_market_cap added to fees_transformed and revenue_transformed in {DUCKDB_DATABASE_PATH}")

if __name__ == "__main__":
    main() 
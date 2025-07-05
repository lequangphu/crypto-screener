import duckdb
import os
import logging

def analyze_and_export():
    """
    Connects to the DuckDB database, calculates valuation metrics for protocols,
    and exports the results as two JSON files: one for fees, one for revenue.
    """
    db_path = "data/crypto.duckdb"
    export_dir = "data/exports"
    fees_export_path = os.path.join(export_dir, "fees_analysis.json")
    revenue_export_path = os.path.join(export_dir, "revenue_analysis.json")

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
        logging.info(f"Created export directory: {export_dir}")

    try:
        con = duckdb.connect(database=db_path, read_only=True)
        logging.info(f"Successfully connected to {db_path}")

        # Fees Table
        fees_query = """
        SELECT
            f.name AS protocol_name,
            f.category AS category,
            f.fully_diluted_market_cap,
            f.total30d AS fees_30d,
            f.change_30dover30d AS fees_30d_change,
            CASE
                WHEN (f.total30d * 12) > 0 THEN f.fully_diluted_market_cap / (f.total30d * 12)
                ELSE NULL
            END AS pf_ratio_forward_1y,
            f.slug AS slug
        FROM
            fees_transformed f
        WHERE
            f.fully_diluted_market_cap IS NOT NULL
            AND f.fully_diluted_market_cap >= 1000000
            AND f.total30d > 0
        ORDER BY
            pf_ratio_forward_1y ASC NULLS LAST;
        """
        fees_result = con.execute(fees_query).fetchdf()
        fees_result.to_json(fees_export_path, orient='records', indent=2)
        logging.info(f"Exported {len(fees_result)} rows to {fees_export_path}")

        # Revenue Table
        revenue_query = """
        SELECT
            r.name AS protocol_name,
            r.category AS category,
            r.fully_diluted_market_cap,
            r.total30d AS revenue_30d,
            r.change_30dover30d AS revenue_30d_change,
            CASE
                WHEN (r.total30d * 12) > 0 THEN r.fully_diluted_market_cap / (r.total30d * 12)
                ELSE NULL
            END AS pr_ratio_forward_1y,
            r.slug AS slug
        FROM
            revenue_transformed r
        WHERE
            r.fully_diluted_market_cap IS NOT NULL
            AND r.fully_diluted_market_cap >= 1000000
            AND r.total30d > 0
        ORDER BY
            pr_ratio_forward_1y ASC NULLS LAST;
        """
        revenue_result = con.execute(revenue_query).fetchdf()
        revenue_result.to_json(revenue_export_path, orient='records', indent=2)
        logging.info(f"Exported {len(revenue_result)} rows to {revenue_export_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if 'con' in locals() and con:
            con.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    analyze_and_export() 
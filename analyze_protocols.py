import duckdb
import pandas as pd
import os
import logging

def analyze_and_export():
    """
    Connects to the DuckDB database, calculates valuation metrics for protocols,
    and exports the results as a JSON file for dashboard use.
    """
    db_path = "data/crypto.duckdb"
    export_dir = "data/exports"
    export_path = os.path.join(export_dir, "analysis.json")

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
        logging.info(f"Created export directory: {export_dir}")

    try:
        con = duckdb.connect(database=db_path, read_only=True)
        logging.info(f"Successfully connected to {db_path}")

        query = """
        SELECT
            f.total30d,
            f.total1y,
            f.change_30dover30d,
            f.name,
            f.category,
            f.fully_diluted_market_cap,
            (f.total30d * 12) AS fees_forward_1y,
            (r.total30d * 12) AS revenue_forward_1y,
            CASE
                WHEN f.total1y > 0 THEN f.fully_diluted_market_cap / f.total1y
                ELSE NULL
            END AS pf_ratio_1y,
            CASE
                WHEN r.total1y > 0 THEN r.fully_diluted_market_cap / r.total1y
                ELSE NULL
            END AS pr_ratio_1y,
            CASE
                WHEN (f.total30d * 12) > 0 THEN f.fully_diluted_market_cap / (f.total30d * 12)
                ELSE NULL
            END AS pf_ratio_forward_1y,
            CASE
                WHEN (r.total30d * 12) > 0 THEN r.fully_diluted_market_cap / (r.total30d * 12)
                ELSE NULL
            END AS pr_ratio_forward_1y,
            f.change_7d AS fees_change_7d,
            r.change_7d AS revenue_change_7d
        FROM
            fees_transformed f
        JOIN
            revenue_transformed r ON f.defillamaId = r.defillamaId
        WHERE
            f.fully_diluted_market_cap IS NOT NULL
            AND f.fully_diluted_market_cap > 0
            AND ((f.total1y > 0 OR r.total1y > 0) OR (f.total30d > 0 OR r.total30d > 0))
        ORDER BY
            pf_ratio_forward_1y ASC NULLS LAST,
            pr_ratio_forward_1y ASC NULLS LAST,
            pf_ratio_1y ASC NULLS LAST,
            pr_ratio_1y ASC NULLS LAST
        LIMIT 20;
        """

        result = con.execute(query).fetchdf()
        result.to_json(export_path, orient='records', indent=2)
        logging.info(f"Exported {len(result)} rows to {export_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if 'con' in locals() and con:
            con.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    analyze_and_export() 
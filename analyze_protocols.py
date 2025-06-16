import duckdb

def analyze_protocols():
    """
    Connects to the DuckDB database, calculates valuation metrics for protocols,
    and prints the results.
    """
    db_path = "data/crypto.duckdb"

    try:
        con = duckdb.connect(database=db_path, read_only=True)
        print(f"Successfully connected to {db_path}")

        query = """
        SELECT
            f.name,
            f.category,
            f.fully_diluted_market_cap AS fd_market_cap,
            f.total1y AS total_fees_1y,
            r.total1y AS total_revenue_1y,
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
        print("\nUndervalued Protocols (based on Annualized 30-day P/F and P/R ratios, then 1-year ratios):\n")
        print(result.to_string())

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'con' in locals() and con:
            con.close()
            print("Database connection closed.")

if __name__ == "__main__":
    analyze_protocols() 
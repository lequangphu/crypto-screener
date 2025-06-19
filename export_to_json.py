import duckdb
import pandas as pd
import os
import logging

EXPORT_DIR = 'data/exports'
DUCKDB_DATABASE_PATH = 'data/crypto.duckdb'

SELECTED_COLUMNS = [
    'total30d',
    'total1y',
    'change_30dover30d',
    'name',
    'category',
    'fully_diluted_market_cap',
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def ensure_export_dir():
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)
        logging.info(f"Created export directory: {EXPORT_DIR}")
    else:
        logging.info(f"Export directory exists: {EXPORT_DIR}")

def export_table_to_json(con, table_name, output_filename):
    query = f"SELECT {', '.join(SELECTED_COLUMNS)} FROM {table_name}"
    df = con.execute(query).df()
    output_path = os.path.join(EXPORT_DIR, output_filename)
    df.to_json(output_path, orient='records', indent=2)
    logging.info(f"Exported {len(df)} rows from {table_name} to {output_path}")

def main():
    ensure_export_dir()
    con = duckdb.connect(database=DUCKDB_DATABASE_PATH, read_only=True)
    export_table_to_json(con, 'fees_transformed', 'fees_transformed.json')
    export_table_to_json(con, 'revenue_transformed', 'revenue_transformed.json')
    con.close()
    logging.info("Export to JSON completed.")

if __name__ == "__main__":
    main() 
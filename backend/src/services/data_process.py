import duckdb
import polars as pl
import pandas as pd

def process_data(protocols_data, fees_data, revenue_data, market_data):
    # Convert to Polars DataFrames with schema inference
    protocols_df = pl.DataFrame(protocols_data)
    fees_df = pl.DataFrame(fees_data.get("protocols", []))
    revenue_df = pl.DataFrame(revenue_data.get("protocols", []))
    market_df = pl.DataFrame(market_data.get("data", []))

    # Ensure numeric columns are properly typed
    protocols_df = protocols_df.with_columns([
        pl.col("id").cast(pl.String),
        pl.col("name").cast(pl.String),
        pl.col("chain").cast(pl.String),
        pl.col("category").cast(pl.String)
    ])

    fees_df = fees_df.with_columns([
        pl.col("protocolId").cast(pl.String),
        pl.col("totalFees").cast(pl.Float64)
    ])

    revenue_df = revenue_df.with_columns([
        pl.col("protocolId").cast(pl.String),
        pl.col("totalRevenue").cast(pl.Float64)
    ])

    # Example: Merge protocols with fees using duckdb
    conn = duckdb.connect(database=':memory:', read_only=False)
    conn.register("protocols_df", protocols_df.to_pandas())
    conn.register("fees_df", fees_df.to_pandas())
    conn.register("revenue_df", revenue_df.to_pandas())

    # Perform joins
    merged_df_fees = conn.execute("""
        SELECT 
            p.id as protocolId, 
            p.name, 
            p.chain, 
            p.category, 
            COALESCE(f.totalFees, 0) as dailyFees 
        FROM protocols_df p 
        LEFT JOIN fees_df f ON p.id = f.protocolId
    """).fetchdf()

    merged_df_revenue = conn.execute("""
        SELECT 
            r.protocolId,
            COALESCE(r.totalRevenue, 0) as dailyRevenue 
        FROM revenue_df r
    """).fetchdf()

    final_df = pd.merge(merged_df_fees, merged_df_revenue, on='protocolId', how='left')

    # Process market data
    market_df_pd = market_df.to_pandas()
    cmc_data_processed = []
    for index, row in market_df_pd.iterrows():
        quote_usd = row["quote"]["USD"]
        cmc_data_processed.append({
            "name": str(row["name"]),
            "price": float(quote_usd.get("price", 0)),
            "marketCap": float(quote_usd.get("market_cap", 0))
        })
    cmc_df = pd.DataFrame(cmc_data_processed)

    # Merge with market data
    final_df = pd.merge(final_df, cmc_df, on='name', how='left')

    # Fill NaN values with 0 for numeric columns
    numeric_columns = ['dailyFees', 'dailyRevenue', 'price', 'marketCap']
    final_df[numeric_columns] = final_df[numeric_columns].fillna(0)

    return final_df.to_dict(orient="records") 
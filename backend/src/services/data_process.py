import duckdb
import polars as pl
import pandas as pd

def process_data(protocols_data, fees_data, revenue_data, market_data):
    # Convert to Polars DataFrames
    protocols_df = pl.DataFrame(protocols_data)
    fees_df = pl.DataFrame(fees_data.get("protocols", []))
    revenue_df = pl.DataFrame(revenue_data.get("protocols", []))
    market_df = pl.DataFrame(market_data.get("data", []))

    # Example: Merge protocols with fees using duckdb
    conn = duckdb.connect(database=':memory:', read_only=False)
    conn.register("protocols_df", protocols_df.to_pandas())
    conn.register("fees_df", fees_df.to_pandas())
    conn.register("revenue_df", revenue_df.to_pandas())

    # Perform joins
    merged_df_fees = conn.execute("SELECT p.id as protocolId, p.name, p.chain, p.category, f.totalFees as dailyFees FROM protocols_df p JOIN fees_df f ON p.id = f.protocolId").fetchdf()
    merged_df_revenue = conn.execute("SELECT r.totalRevenue as dailyRevenue, r.protocolId FROM revenue_df r").fetchdf()

    final_df = pd.merge(merged_df_fees, merged_df_revenue, on='protocolId', how='left')

    # Convert market_df to pandas for easier merging with the current setup
    market_df_pd = market_df.to_pandas()

    # Merge CoinMarketCap data (assuming 'name' is a common key)
    # The CMC data structure is a bit nested, so we need to flatten it or access it correctly.
    # For now, let's assume 'name' is directly available in market_df and prices/market_caps are under 'quote.USD'
    
    # To merge market data, we need a common key. Let's assume protocol name can be used for now.
    # We need to extract the relevant data from market_df_pd first.
    cmc_data_processed = []
    for index, row in market_df_pd.iterrows():
        cmc_data_processed.append({
            "name": row["name"],
            "price": row["quote"]["USD"]["price"],
            "marketCap": row["quote"]["USD"]["market_cap"],
        })
    cmc_df = pd.DataFrame(cmc_data_processed)

    final_df = pd.merge(final_df, cmc_df, on='name', how='left')

    return final_df.to_dict(orient="records") 
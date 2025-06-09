import duckdb
import polars as pl
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def process_data(protocols_data, fees_data, revenue_data, market_data):
    try:
        # Define a schema for protocols_df to ensure consistent type handling
        protocols_schema = {
            "id": pl.String,
            "name": pl.String,
            "slug": pl.String,
            "chain": pl.String,
            "category": pl.String,
            "logo": pl.String,
            "url": pl.String,
            "l2Data": pl.Boolean,
            "parentProtocol": pl.String,
            "chains": pl.List(pl.String),
            "type": pl.String,
            "redirect": pl.String,
            "module": pl.String,
            "gecko_id": pl.String,
            "cmcId": pl.String,
            "ossr": pl.Boolean,
            "language": pl.String,
            "twitter": pl.String,
            "audit_links": pl.List(pl.String),
            "grants": pl.List(pl.String),
            "deadWhere": pl.String
        }

        # Convert to Polars DataFrames with explicit schema
        protocols_df = pl.DataFrame(protocols_data, schema=protocols_schema, strict=False)
        fees_df = pl.DataFrame(fees_data.get("protocols", []), strict=False, infer_schema_length=1000)
        revenue_df = pl.DataFrame(revenue_data.get("protocols", []), strict=False, infer_schema_length=1000)
        market_df = pl.DataFrame(market_data.get("data", []), strict=False, infer_schema_length=1000)

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
            quote_usd = row.get("quote", {}).get("USD", {})
            cmc_data_processed.append({
                "name": str(row.get("name", "")),
                "price": float(quote_usd.get("price", 0)),
                "marketCap": float(quote_usd.get("market_cap", 0))
            })
        cmc_df = pd.DataFrame(cmc_data_processed)

        # Merge with market data
        final_df = pd.merge(final_df, cmc_df, on='name', how='left')

        # Fill NaN values with 0 for numeric columns
        numeric_columns = ['dailyFees', 'dailyRevenue', 'price', 'marketCap']
        final_df[numeric_columns] = final_df[numeric_columns].fillna(0)

        # Ensure all required fields are present and properly formatted
        result = []
        for _, row in final_df.iterrows():
            protocol = {
                "name": str(row.get("name", "")),
                "chain": str(row.get("chain", "")),
                "category": str(row.get("category", "")),
                "dailyFees": float(row.get("dailyFees", 0)),
                "dailyRevenue": float(row.get("dailyRevenue", 0)),
                "marketCap": float(row.get("marketCap", 0)),
                "price": float(row.get("price", 0))
            }
            result.append(protocol)

        logger.info(f"Successfully processed {len(result)} protocols")
        return result

    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        return [] 
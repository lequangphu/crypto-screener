# CoinMarketCap Table

This table contains data on cryptocurrencies from CoinMarketCap, including market data, supply information, and various price change percentages.

## Schema

*   `id`: BIGINT - Unique CoinMarketCap ID for the cryptocurrency.
*   `name`: VARCHAR - Name of the cryptocurrency.
*   `symbol`: VARCHAR - Symbol of the cryptocurrency (e.g., "BTC", "ETH").
*   `slug`: VARCHAR - URL-friendly name of the cryptocurrency.
*   `num_market_pairs`: BIGINT - Number of market pairs available for the cryptocurrency.
*   `date_added`: VARCHAR - Date the cryptocurrency was added to CoinMarketCap.
*   `tags`: VARCHAR[] - Tags associated with the cryptocurrency (e.g., "mineable", "pow").
*   `max_supply`: DOUBLE - Maximum supply of the cryptocurrency.
*   `circulating_supply`: DOUBLE - Current circulating supply of the cryptocurrency.
*   `total_supply`: DOUBLE - Total supply of the cryptocurrency.
*   `infinite_supply`: BOOLEAN - Indicates if the cryptocurrency has an infinite supply.
*   `platform`: STRUCT - Platform details if it's a token on another blockchain.
    *   `id`: INTEGER - Platform ID.
    *   `name`: VARCHAR - Platform name.
    *   `symbol`: VARCHAR - Platform symbol.
    *   `slug`: VARCHAR - Platform slug.
    *   `token_address`: VARCHAR - Token address on the platform.
*   `cmc_rank`: BIGINT - Current CoinMarketCap rank.
*   `self_reported_circulating_supply`: DOUBLE - Self-reported circulating supply.
*   `self_reported_market_cap`: DOUBLE - Self-reported market capitalization.
*   `tvl_ratio`: DOUBLE - TVL ratio.
*   `last_updated`: VARCHAR - Timestamp of the last update for this record.
*   `quote`: STRUCT - Price and market data in USD.
    *   `USD`: STRUCT - USD currency quote.
        *   `price`: DOUBLE - Current price in USD.
        *   `volume_24h`: DOUBLE - 24-hour trading volume in USD.
        *   `volume_change_24h`: DOUBLE - Percentage change in volume over 24 hours.
        *   `percent_change_1h`: DOUBLE - Percentage change in price over 1 hour.
        *   `percent_change_24h`: DOUBLE - Percentage change in price over 24 hours.
        *   `percent_change_7d`: DOUBLE - Percentage change in price over 7 days.
        *   `percent_change_30d`: DOUBLE - Percentage change in price over 30 days.
        *   `percent_change_60d`: DOUBLE - Percentage change in price over 60 days.
        *   `percent_change_90d`: DOUBLE - Percentage change in price over 90 days.
        *   `market_cap`: DOUBLE - Market capitalization in USD.
        *   `market_cap_dominance`: DOUBLE - Market capitalization dominance.
        *   `fully_diluted_market_cap`: DOUBLE - Fully diluted market capitalization in USD.
        *   `tvl`: DOUBLE - Total Value Locked (TVL).
        *   `last_updated`: VARCHAR - Timestamp of the last update for USD quote. 
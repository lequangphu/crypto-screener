# Protocols Table

This table contains information about various decentralized finance (DeFi) protocols, including their basic details, chain compatibility, and financial metrics like Total Value Locked (TVL).

## Schema

*   `id`: VARCHAR - Unique identifier for the protocol.
*   `name`: VARCHAR - Name of the protocol.
*   `address`: VARCHAR - Contract address (if applicable).
*   `symbol`: VARCHAR - Symbol of the native token (if applicable).
*   `url`: VARCHAR - Official website URL.
*   `description`: VARCHAR - A brief description of the protocol.
*   `chain`: VARCHAR - Primary chain the protocol operates on.
*   `logo`: VARCHAR - URL to the protocol's logo.
*   `audits`: VARCHAR - Audit status (e.g., number of audits).
*   `audit_note`: VARCHAR - Notes regarding audits.
*   `gecko_id`: VARCHAR - CoinGecko ID.
*   `cmcId`: VARCHAR - CoinMarketCap ID.
*   `category`: VARCHAR - Category of the protocol (e.g., "Lending", "Dexs").
*   `chains`: VARCHAR[] - Array of chains the protocol is available on.
*   `module`: VARCHAR - Internal module name.
*   `twitter`: VARCHAR - Twitter handle.
*   `forkedFrom`: INTEGER[] - IDs of protocols this protocol forked from.
*   `listedAt`: DOUBLE - Timestamp when the protocol was listed.
*   `methodology`: VARCHAR - Description of the data collection methodology.
*   `slug`: VARCHAR - URL-friendly name.
*   `tvl`: DOUBLE - Total Value Locked (TVL) of the protocol.
*   `chainTvls`: MAP(VARCHAR, DOUBLE) - TVL broken down by chain.
*   `change_1h`: DOUBLE - Percentage change in TVL over 1 hour.
*   `change_1d`: DOUBLE - Percentage change in TVL over 1 day.
*   `change_7d`: DOUBLE - Percentage change in TVL over 7 days.
*   `tokenBreakdowns`: MAP(INTEGER, INTEGER) - Breakdown of tokens.
*   `mcap`: DOUBLE - Market capitalization.
*   `oraclesBreakdown`: VARCHAR - Breakdown of oracles used.
*   `audit_links`: VARCHAR[] - Links to audit reports.
*   `parentProtocol`: VARCHAR - ID of the parent protocol, if applicable.
*   `wrongLiquidity`: BOOLEAN - Indicates if liquidity is misrepresented.
*   `hallmarks`: VARCHAR[][] - Significant historical events.
*   `referralUrl`: VARCHAR - Referral URL.
*   `treasury`: VARCHAR - Treasury information.
*   `openSource`: BOOLEAN - Indicates if the protocol is open source.
*   `governanceID`: VARCHAR[] - IDs related to governance.
*   `github`: VARCHAR[] - GitHub repository links.
*   `staking`: DOUBLE - Staking information.
*   `previousNames`: VARCHAR[] - Previous names of the protocol.
*   `assetToken`: VARCHAR - Asset token information.
*   `tokensExcludedFromParent`: MAP(VARCHAR, VARCHAR[]) - Tokens excluded from parent protocol.
*   `pool2`: DOUBLE - Pool2 information.
*   `misrepresentedTokens`: BOOLEAN - Indicates if tokens are misrepresented.
*   `forkedFromIds`: VARCHAR[] - IDs of protocols this protocol forked from.
*   `oracles`: VARCHAR[] - Oracles used by the protocol.
*   `tags`: VARCHAR[] - Tags associated with the protocol.
*   `stablecoins`: VARCHAR[] - Stablecoins associated with the protocol.
*   `language`: VARCHAR - Programming language.
*   `deadUrl`: BOOLEAN - Indicates if the URL is dead.
*   `deadFrom`: VARCHAR - Date from when the URL was dead.
*   `rugged`: BOOLEAN - Indicates if the protocol was rugged.
*   `deprecated`: BOOLEAN - Indicates if the protocol is deprecated. 
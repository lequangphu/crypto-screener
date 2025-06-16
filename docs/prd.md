# Crypto Protocols/Apps Valuation Analysis
get and calculate metrics derived from fees, revenue, and marketcap of crypto protocols.

## Objective

## Requirements

### Data Sources

The application will integrate with the following APIs:

#### DeFiLlama API
- Base URL: `https://api.llama.fi`
- Rate Limit: 100 requests per minute
- No API key required

#### CoinMarketCap API
- Base URL: `https://pro-api.coinmarketcap.com`
- Rate Limit: Varies by plan
- Requires API key

```json
{
    "defillama": {
        "protocols": {
            "endpoint": "https://api.llama.fi/protocols",
            "description": "Returns list of all protocols with their TVL and other metrics",
            "response_format": "JSON array of protocol objects"
        },
        "fees_overview": {
            "endpoint": "https://api.llama.fi/overview/fees?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true&dataType=dailyFees",
            "description": "Returns daily fees data for all protocols",
            "response_format": "JSON object with protocol fees data"
        },
        "revenue_overview": {
            "endpoint": "https://api.llama.fi/overview/fees?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true&dataType=dailyRevenue",
            "description": "Returns daily revenue data for all protocols",
            "response_format": "JSON object with protocol revenue data"
        }
    },
    "coinmarketcap": {
        "quotes_latest": {
            "endpoint": "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest",
            "description": "Returns latest cryptocurrency market data for specific IDs",
            "required_headers": {
                "X-CMC_PRO_API_KEY": "Your API key"
            },
            "response_format": "JSON object with cryptocurrency quotes"
        }
    }
}
```

from fastapi import APIRouter
from ..services.data_fetch import fetch_defillama_protocols, fetch_defillama_fees_overview, fetch_defillama_revenue_overview, fetch_coinmarketcap_listings
from ..services.data_process import process_data
from .models import Protocol, Filter

router = APIRouter()

@router.get("/protocols", response_model=list[Protocol])
async def get_protocols():
    protocols_data = fetch_defillama_protocols()
    fees_data = fetch_defillama_fees_overview()
    revenue_data = fetch_defillama_revenue_overview()
    market_data = fetch_coinmarketcap_listings()
    
    processed_protocols = process_data(protocols_data, fees_data, revenue_data, market_data)
    return processed_protocols

@router.get("/filters", response_model=Filter)
async def get_filters():
    protocols_data = fetch_defillama_protocols()
    chains = list(set([p.get("chain", "Unknown") for p in protocols_data if p.get("chain")]))
    protocol_types = list(set([p.get("category", "Unknown") for p in protocols_data if p.get("category")]))
    return {"chains": chains, "protocol_types": protocol_types} 
from fastapi import APIRouter, HTTPException
from services.data_fetch import fetch_defillama_protocols, fetch_defillama_fees_overview, fetch_defillama_revenue_overview, fetch_coinmarketcap_listings
from services.data_process import process_data
from api.models import Protocol, Filter
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/protocols", response_model=list[Protocol])
async def get_protocols():
    try:
        protocols_data = fetch_defillama_protocols()
        if not protocols_data:
            raise HTTPException(status_code=503, detail="Failed to fetch protocols data")
            
        fees_data = fetch_defillama_fees_overview()
        revenue_data = fetch_defillama_revenue_overview()
        market_data = fetch_coinmarketcap_listings()
        
        processed_protocols = process_data(protocols_data, fees_data, revenue_data, market_data)
        if not processed_protocols:
            raise HTTPException(status_code=503, detail="Failed to process protocols data")
            
        return processed_protocols
    except Exception as e:
        logger.error(f"Error in /protocols endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filters", response_model=Filter)
async def get_filters():
    try:
        protocols_data = fetch_defillama_protocols()
        if not protocols_data:
            raise HTTPException(status_code=503, detail="Failed to fetch protocols data")
            
        chains = list(set([p.get("chain", "Unknown") for p in protocols_data if p.get("chain")]))
        protocol_types = list(set([p.get("category", "Unknown") for p in protocols_data if p.get("category")]))
        return {"chains": chains, "protocol_types": protocol_types}
    except Exception as e:
        logger.error(f"Error in /filters endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 
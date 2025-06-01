from pydantic import BaseModel

class Protocol(BaseModel):
    name: str
    chain: str
    category: str | None = None
    dailyFees: float | None = None
    dailyRevenue: float | None = None
    marketCap: float | None = None
    price: float | None = None

class Filter(BaseModel):
    chains: list[str]
    protocol_types: list[str] 
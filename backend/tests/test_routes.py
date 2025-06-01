from fastapi.testclient import TestClient
from backend.src.main import app
import requests_mock
import pytest

client = TestClient(app)

@pytest.fixture
def mock_api_responses():
    with requests_mock.Mocker() as m:
        # Mock DeFiLlama protocols
        m.get("https://api.llama.fi/protocols", json=[
            {"id": "1", "name": "ProtocolA", "chain": "Ethereum", "category": "Lending"},
            {"id": "2", "name": "ProtocolB", "chain": "Polygon", "category": "DEX"}
        ])
        # Mock DeFiLlama fees
        m.get("https://api.llama.fi/overview/fees?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true&dataType=dailyFees", json={
            "protocols": [
                {"protocolId": "1", "totalFees": 1000},
                {"protocolId": "2", "totalFees": 2000}
            ]
        })
        # Mock DeFiLlama revenue
        m.get("https://api.llama.fi/overview/fees?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true&dataType=dailyRevenue", json={
            "protocols": [
                {"protocolId": "1", "totalRevenue": 500},
                {"protocolId": "2", "totalRevenue": 1000}
            ]
        })
        # Mock CoinMarketCap listings
        m.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest", json={
            "data": [
                {"name": "ProtocolA", "quote": {"USD": {"price": 1.0, "market_cap": 1000000}}},
                {"name": "ProtocolB", "quote": {"USD": {"price": 0.5, "market_cap": 500000}}}
            ]
        })
        yield

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Crypto Screener Backend!"}

def test_get_protocols(mock_api_responses):
    response = client.get("/protocols")
    assert response.status_code == 200
    protocols = response.json()
    assert len(protocols) > 0
    assert protocols[0]["name"] == "ProtocolA"

def test_get_filters(mock_api_responses):
    response = client.get("/filters")
    assert response.status_code == 200
    filters = response.json()
    assert "chains" in filters
    assert "protocol_types" in filters
    assert "Ethereum" in filters["chains"]
    assert "Lending" in filters["protocol_types"] 
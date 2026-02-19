from collections.abc import AsyncGenerator, Generator
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.dependencies.geo_service_dependence import get_geo_service
from src.main import app
from src.schemas.geo_response import GeoResponse
from src.schemas.ip_api_response import IPAPIResponse
from src.services.geolocation_service import GeoIPService


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client for integration tests."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def geo_service() -> GeoIPService:
    """Fresh GeoIPService instance for unit tests."""
    return GeoIPService(base_url="http://test-api.local", timeout=5)


@pytest.fixture
def valid_ip() -> str:
    return "8.8.8.8"


@pytest.fixture
def private_ip() -> str:
    return "192.168.1.1"


@pytest.fixture
def loopback_ip() -> str:
    return "127.0.0.1"


@pytest.fixture
def invalid_ip() -> str:
    return "not-an-ip"


@pytest.fixture
def mock_successful_api_response() -> dict[str, Any]:
    return {
        "status": "success",
        "country": "United States",
        "countryCode": "US",
        "region": "CA",
        "regionName": "California",
        "city": "Mountain View",
        "zip": "94035",
        "lat": 37.386,
        "lon": -122.0838,
        "timezone": "America/Los_Angeles",
        "isp": "Google LLC",
        "org": "Google LLC",
        "as": "AS15169 Google LLC",
        "query": "8.8.8.8",
        "mobile": False,
        "proxy": False,
        "hosting": True,
    }


@pytest.fixture
def mock_failed_api_response() -> dict[str, str]:
    return {
        "status": "fail",
        "message": "invalid query",
        "query": "invalid",
    }


@pytest.fixture
def mock_ip_api_response(mock_successful_api_response: dict[str, Any]) -> IPAPIResponse:
    return IPAPIResponse.model_validate(mock_successful_api_response)


@pytest.fixture
def mock_geo_response() -> GeoResponse:
    """Pre-built GeoResponse for mocking."""
    return GeoResponse(
        ip="8.8.8.8",
        country="United States",
        country_code="US",
        region="California",
        city="Mountain View",
        zip="94035",
        latitude=37.386,
        longitude=-122.0838,
        timezone="America/Los_Angeles",
        isp="Google LLC",
        is_mobile=False,
        is_proxy=False,
        is_hosting=True,
    )


@pytest.fixture
def mock_request_with_ip() -> MagicMock:
    request = MagicMock()
    request.client = MagicMock()
    request.client.host = "8.8.8.8"
    return request


@pytest.fixture
def mock_request_without_client() -> MagicMock:
    request = MagicMock()
    request.client = None
    return request


@pytest.fixture
def mock_request_without_host() -> MagicMock:
    request = MagicMock()
    request.client = MagicMock()
    request.client.host = None
    return request


@pytest.fixture
def mock_geo_service() -> AsyncMock:
    """
    Mocked GeoIPService used for dependency injection.
    """
    service = AsyncMock()
    service.get_geo = AsyncMock()
    service.get_geo_from_request = AsyncMock()
    return service


@pytest.fixture(autouse=True)
def override_geo_service(mock_geo_service: AsyncMock) -> Generator[None, None, None]:
    """
    Override get_geo_service dependency for all tests in this module.
    """
    app.dependency_overrides[get_geo_service] = lambda: mock_geo_service
    yield
    app.dependency_overrides.clear()

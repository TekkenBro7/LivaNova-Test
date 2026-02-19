from unittest.mock import AsyncMock

import pytest
from fastapi import status
from httpx import AsyncClient

from src.schemas.geo_response import GeoResponse

GEO_PREFIX = "/api/v1/geo"


class TestGetGeoEndpoint:
    """Integration tests for GET /geo endpoint."""

    @pytest.mark.asyncio
    async def test_get_geo_valid_ip_returns_200(
        self, client: AsyncClient, mock_geo_response: GeoResponse, mock_geo_service: AsyncMock
    ) -> None:
        """Valid IP returns 200 with geo data."""
        mock_geo_service.get_geo.return_value = mock_geo_response

        response = await client.get(GEO_PREFIX, params={"ip": "8.8.8.8"})

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["ip"] == "8.8.8.8"
        assert data["country"] == "United States"
        assert data["city"] == "Mountain View"

        mock_geo_service.get_geo.assert_awaited_once_with("8.8.8.8")

    @pytest.mark.asyncio
    async def test_get_geo_invalid_ip_returns_400(
        self, client: AsyncClient, mock_geo_service: AsyncMock
    ) -> None:
        """Invalid IP format returns 400."""
        mock_geo_service.get_geo.side_effect = ValueError("Invalid IP address: not-valid-ip")

        response = await client.get(GEO_PREFIX, params={"ip": "not-valid-ip"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid IP address" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_get_geo_private_ip_returns_400(
        self, client: AsyncClient, mock_geo_service: AsyncMock
    ) -> None:
        """Private IP returns 400."""
        mock_geo_service.get_geo.side_effect = ValueError("IP 192.168.1.1 is private or reserved")

        response = await client.get(GEO_PREFIX, params={"ip": "192.168.1.1"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "private or reserved" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_get_geo_loopback_ip_returns_400(
        self, client: AsyncClient, mock_geo_service: AsyncMock
    ) -> None:
        """Loopback IP returns 400."""
        mock_geo_service.get_geo.side_effect = ValueError("IP 127.0.0.1 is private or reserved")

        response = await client.get(GEO_PREFIX, params={"ip": "127.0.0.1"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "private or reserved" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_get_geo_missing_ip_param_returns_422(self, client: AsyncClient) -> None:
        """Missing required IP parameter returns 422."""
        response = await client.get(GEO_PREFIX)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    @pytest.mark.asyncio
    async def test_get_geo_api_failure_returns_400(
        self, client: AsyncClient, mock_geo_service: AsyncMock
    ) -> None:
        """API failure response returns 400."""
        mock_geo_service.get_geo.side_effect = ValueError("IP API failed: invalid query")

        response = await client.get(GEO_PREFIX, params={"ip": "8.8.8.8"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "IP API failed" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_get_geo_network_error_returns_400(
        self, client: AsyncClient, mock_geo_service: AsyncMock
    ) -> None:
        """Network error returns 400."""
        mock_geo_service.get_geo.side_effect = ValueError(
            "IP API request failed: Connection refused"
        )

        response = await client.get(GEO_PREFIX, params={"ip": "8.8.8.8"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "IP API request failed" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_get_geo_timeout_returns_400(
        self, client: AsyncClient, mock_geo_service: AsyncMock
    ) -> None:
        """Timeout error returns 400."""
        mock_geo_service.get_geo.side_effect = ValueError("IP API request failed: Timeout")

        response = await client.get(GEO_PREFIX, params={"ip": "8.8.8.8"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_get_geo_server_error_returns_400(
        self, client: AsyncClient, mock_geo_service: AsyncMock
    ) -> None:
        """External API 500 error returns 400."""
        mock_geo_service.get_geo.side_effect = ValueError("IP API returned error status: 500")

        response = await client.get(GEO_PREFIX, params={"ip": "8.8.8.8"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestGetGeoMeEndpoint:
    """Integration tests for GET /geo/me endpoint."""

    @pytest.mark.asyncio
    async def test_get_geo_me_returns_200(
        self, client: AsyncClient, mock_geo_response: GeoResponse, mock_geo_service: AsyncMock
    ) -> None:
        """/geo/me endpoint returns 200 with geo data."""
        mock_geo_service.get_geo_from_request.return_value = mock_geo_response

        response = await client.get(f"{GEO_PREFIX}/me")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["country"] == "United States"
        assert data["ip"] == "8.8.8.8"

    @pytest.mark.asyncio
    async def test_get_geo_me_no_client_ip_returns_400(
        self, client: AsyncClient, mock_geo_service: AsyncMock
    ) -> None:
        """When client IP cannot be determined, returns 400."""
        mock_geo_service.get_geo_from_request.side_effect = ValueError(
            "Cannot determine client IP from request"
        )

        response = await client.get(f"{GEO_PREFIX}/me")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Cannot determine client IP" in response.json()["detail"]


class TestGeoResponseFormat:
    """Tests verifying response format matches schema."""

    @pytest.mark.asyncio
    async def test_response_contains_all_expected_fields(
        self, client: AsyncClient, mock_geo_response: GeoResponse, mock_geo_service: AsyncMock
    ) -> None:
        """Response contains all expected fields from GeoResponse schema."""
        mock_geo_service.get_geo.return_value = mock_geo_response

        response = await client.get(GEO_PREFIX, params={"ip": "8.8.8.8"})

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Required fields
        assert "ip" in data
        assert "country" in data
        assert "country_code" in data
        assert "city" in data
        assert "latitude" in data
        assert "longitude" in data

        # Optional fields
        assert "region" in data
        assert "zip" in data
        assert "timezone" in data
        assert "isp" in data
        assert "is_mobile" in data
        assert "is_proxy" in data
        assert "is_hosting" in data

    @pytest.mark.asyncio
    async def test_response_field_types(
        self, client: AsyncClient, mock_geo_response: GeoResponse, mock_geo_service: AsyncMock
    ) -> None:
        """Response field types are correct."""
        mock_geo_service.get_geo.return_value = mock_geo_response

        response = await client.get(GEO_PREFIX, params={"ip": "8.8.8.8"})
        data = response.json()

        assert isinstance(data["ip"], str)
        assert isinstance(data["country"], str)
        assert isinstance(data["latitude"], float)
        assert isinstance(data["longitude"], float)
        assert isinstance(data["is_mobile"], bool)
        assert isinstance(data["is_proxy"], bool)
        assert isinstance(data["is_hosting"], bool)

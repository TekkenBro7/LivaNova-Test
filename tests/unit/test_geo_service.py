from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.core.enums import GeoAPIStatus
from src.schemas.geo_response import GeoResponse
from src.schemas.ip_api_response import IPAPIResponse
from src.services.geolocation_service import GeoIPService


class TestIPValidation:
    """Tests for IP address validation in get_geo."""

    @pytest.mark.asyncio
    async def test_invalid_ip_format_raises_value_error(
        self, geo_service: GeoIPService, invalid_ip: str
    ) -> None:
        """Invalid IP format raises ValueError."""
        with pytest.raises(ValueError, match="Invalid IP address"):
            await geo_service.get_geo(invalid_ip)

    @pytest.mark.asyncio
    async def test_private_ip_raises_value_error(
        self, geo_service: GeoIPService, private_ip: str
    ) -> None:
        """Private IP address raises ValueError."""
        with pytest.raises(ValueError, match="private or reserved"):
            await geo_service.get_geo(private_ip)

    @pytest.mark.asyncio
    async def test_loopback_ip_raises_value_error(
        self, geo_service: GeoIPService, loopback_ip: str
    ) -> None:
        """Loopback IP address raises ValueError."""
        with pytest.raises(ValueError, match="private or reserved"):
            await geo_service.get_geo(loopback_ip)

    @pytest.mark.asyncio
    async def test_reserved_ip_raises_value_error(self, geo_service: GeoIPService) -> None:
        """Reserved IP address raises ValueError."""
        reserved_ip = "0.0.0.0"
        with pytest.raises(ValueError, match="private or reserved"):
            await geo_service.get_geo(reserved_ip)

    @pytest.mark.asyncio
    async def test_empty_ip_raises_value_error(self, geo_service: GeoIPService) -> None:
        """Empty IP string raises ValueError."""
        with pytest.raises(ValueError):
            await geo_service.get_geo("")

    @pytest.mark.asyncio
    async def test_ipv6_loopback_raises_value_error(self, geo_service: GeoIPService) -> None:
        """IPv6 loopback raises ValueError."""
        with pytest.raises(ValueError, match="private or reserved"):
            await geo_service.get_geo("::1")


class TestGetGeoAPIInteraction:
    """Tests for get_geo API interaction."""

    @pytest.mark.asyncio
    async def test_successful_geo_lookup(
        self,
        geo_service: GeoIPService,
        valid_ip: str,
        mock_successful_api_response: dict[str, Any],
    ) -> None:
        """Successful API response returns GeoResponse."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_successful_api_response
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            result = await geo_service.get_geo(valid_ip)

        assert isinstance(result, GeoResponse)
        assert result.ip == valid_ip
        assert result.country == "United States"
        assert result.city == "Mountain View"

    @pytest.mark.asyncio
    async def test_api_returns_fail_status(
        self,
        geo_service: GeoIPService,
        valid_ip: str,
        mock_failed_api_response: dict[str, str],
    ) -> None:
        """API returning fail status raises ValueError."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_failed_api_response
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            with pytest.raises(ValueError, match="IP API failed"):
                await geo_service.get_geo(valid_ip)

    @pytest.mark.asyncio
    async def test_http_status_error_raises_value_error(
        self, geo_service: GeoIPService, valid_ip: str
    ) -> None:
        """HTTP status error raises ValueError."""
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        error = httpx.HTTPStatusError("Server error", request=MagicMock(), response=mock_resp)

        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock(side_effect=error)
            mock_get.return_value = mock_response

            with pytest.raises(ValueError, match="IP API returned error status"):
                await geo_service.get_geo(valid_ip)

    @pytest.mark.asyncio
    async def test_request_error_raises_value_error(
        self, geo_service: GeoIPService, valid_ip: str
    ) -> None:
        """Network request error raises ValueError."""
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = httpx.RequestError("Connection failed")
            with pytest.raises(ValueError, match="IP API request failed"):
                await geo_service.get_geo(valid_ip)

    @pytest.mark.asyncio
    async def test_timeout_error_raises_value_error(
        self, geo_service: GeoIPService, valid_ip: str
    ) -> None:
        """Timeout error raises ValueError."""
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = httpx.TimeoutException("Timeout")
            with pytest.raises(ValueError, match="IP API request failed"):
                await geo_service.get_geo(valid_ip)


class TestGetGeoFromRequest:
    """Tests for get_geo_from_request method."""

    @pytest.mark.asyncio
    async def test_successful_lookup_from_request(
        self,
        geo_service: GeoIPService,
        mock_request_with_ip: MagicMock,
        mock_successful_api_response: dict[str, Any],
    ) -> None:
        """Successfully extracts IP from request and returns geo data."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_successful_api_response
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            result = await geo_service.get_geo_from_request(mock_request_with_ip)

        assert isinstance(result, GeoResponse)
        assert result.ip == "8.8.8.8"

    @pytest.mark.asyncio
    async def test_request_without_client_raises_error(
        self,
        geo_service: GeoIPService,
        mock_request_without_client: MagicMock,
    ) -> None:
        """Request without client raises ValueError."""
        with pytest.raises(ValueError, match="Cannot determine client IP"):
            await geo_service.get_geo_from_request(mock_request_without_client)

    @pytest.mark.asyncio
    async def test_request_without_host_raises_error(
        self,
        geo_service: GeoIPService,
        mock_request_without_host: MagicMock,
    ) -> None:
        """Request without host raises ValueError."""
        with pytest.raises(ValueError, match="Cannot determine client IP"):
            await geo_service.get_geo_from_request(mock_request_without_host)


class TestConvertToGeoResponse:
    """Tests for _convert_to_geo_response method."""

    def test_full_conversion(
        self, geo_service: GeoIPService, mock_ip_api_response: IPAPIResponse
    ) -> None:
        """All fields are correctly mapped."""
        result = geo_service._convert_to_geo_response(mock_ip_api_response)

        assert result.ip == "8.8.8.8"
        assert result.country == "United States"
        assert result.country_code == "US"
        assert result.region == "California"
        assert result.city == "Mountain View"
        assert result.zip == "94035"
        assert result.latitude == 37.386
        assert result.longitude == -122.0838
        assert result.timezone == "America/Los_Angeles"
        assert result.isp == "Google LLC"
        assert result.is_mobile is False
        assert result.is_proxy is False
        assert result.is_hosting is True

    def test_region_fallback_to_region_code(self, geo_service: GeoIPService) -> None:
        """When regionName is None, falls back to region code."""
        api_response = IPAPIResponse(
            status=GeoAPIStatus.SUCCESS,
            query="8.8.8.8",
            country="Test",
            countryCode="TS",
            region="CA",
            regionName=None,
            city="Test City",
            lat=0.0,
            lon=0.0,
            **{"as": "AS12345 Test"},  # type: ignore
        )
        result = geo_service._convert_to_geo_response(api_response)
        assert result.region == "CA"

    def test_optional_fields_can_be_none(self, geo_service: GeoIPService) -> None:
        """Optional fields can be None."""
        api_response = IPAPIResponse(
            status=GeoAPIStatus.SUCCESS,
            query="8.8.8.8",
            country="Test",
            countryCode="TS",
            city="Test City",
            lat=0.0,
            lon=0.0,
            **{"as": None},
        )
        result = geo_service._convert_to_geo_response(api_response)

        assert result.zip is None
        assert result.timezone is None
        assert result.isp is None

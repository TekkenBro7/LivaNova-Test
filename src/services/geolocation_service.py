from ipaddress import ip_address

import httpx
from fastapi import Request

from src.core.config import geo_config
from src.core.enums import GeoAPIStatus
from src.core.logger import logger
from src.schemas.geo_response import GeoResponse
from src.schemas.ip_api_response import IPAPIResponse


class GeoIPService:
    """
    Service to fetch geolocation information from IP-API.

    Handles:
    - IP lookup for given IPv4 addresses.
    - Automatic detection of client IP from request.
    - Conversion of IPAPIResponse to internal GeoResponse model.
    - Error handling for invalid IPs and API failures.
    """

    def __init__(
        self, base_url: str = geo_config.IP_API_BASE_URL, timeout: int = geo_config.TIMEOUT
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        logger.info(
            f"GeoIPService initialized with base_url={self.base_url} and timeout={self.timeout}s"
        )

    async def get_geo(self, ip: str) -> GeoResponse:
        """
        Fetch geolocation information for the given IP address.

        Makes a GET request to the IP API, validates the response against the IPAPIResponse
        model, and converts it to the standard GeoResponse model.

        Args:
            ip (str): The IP address to look up.

        Returns:
            GeoResponse: Standardized geolocation information for the given IP.
        """
        logger.info(f"Looking up geolocation for IP: {ip}")

        try:
            ip_obj = ip_address(ip)
        except ValueError:
            raise ValueError(f"Invalid IP address: {ip}")

        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved:
            raise ValueError(f"IP {ip} is private or reserved and cannot be geolocated")

        url = f"{self.base_url}/{ip}"
        params = {"fields": geo_config.FIELDS}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                data = IPAPIResponse.model_validate(resp.json())
        except httpx.HTTPStatusError as e:
            logger.error(f"IP API returned error status {e.response.status_code} for IP {ip}")
            raise ValueError(f"IP API returned error status: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"IP API request failed for IP {ip}: {str(e)}")
            raise ValueError(f"IP API request failed: {str(e)}")

        if data.status != GeoAPIStatus.SUCCESS:
            logger.error(f"IP API failed for IP {ip}: {data.message or 'Unknown error'}")
            raise ValueError(f"IP API failed: {data.message or 'Unknown error'}")

        logger.info(f"Geolocation successfully retrieved for IP {ip}")
        return self._convert_to_geo_response(data)

    async def get_geo_from_request(self, request: Request) -> GeoResponse:
        """
        Lookup geolocation info for the client IP from the request.

        Args:
            request (Request): FastAPI Request object.

        Returns:
            GeoResponse: Standardized geolocation information.
        """
        client = request.client
        if client is None or client.host is None:
            logger.warning("Cannot determine client IP from request")
            raise ValueError("Cannot determine client IP from request")

        client_ip = client.host
        logger.info(f"Detected client IP: {client_ip}")
        return await self.get_geo(client_ip)

    def _convert_to_geo_response(self, ip_data: IPAPIResponse) -> GeoResponse:
        """
        Convert an IPAPIResponse object to a GeoResponse object.

        Args:
            ip_data (IPAPIResponse): The raw response from the IP API.

        Returns:
            GeoResponse: Standardized response with selected geolocation fields.
        """
        logger.debug(f"Converting IPAPIResponse to GeoResponse for IP {ip_data.query}")

        return GeoResponse(
            ip=ip_data.query,
            country=ip_data.country,
            country_code=ip_data.countryCode,
            region=ip_data.regionName or ip_data.region,
            city=ip_data.city,
            zip=ip_data.zip,
            latitude=ip_data.lat,
            longitude=ip_data.lon,
            timezone=ip_data.timezone,
            isp=ip_data.isp,
            is_mobile=ip_data.mobile,
            is_proxy=ip_data.proxy,
            is_hosting=ip_data.hosting,
        )

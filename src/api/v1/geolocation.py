from fastapi import APIRouter, HTTPException, Query, Request

from src.core.enums import HTTPStatusCode
from src.schemas.geo_response import GeoResponse
from src.services.geolocation_service import geo_service

router = APIRouter()


@router.get(
    "",
    response_model=GeoResponse,
    summary="Get geolocation for a specific IP",
    description=(
        "Retrieve detailed geolocation information for a given IPv4 address. "
        "Provide a valid IPv4 address as a query parameter. "
        "Returns HTTP 400 if the IP is invalid or cannot be processed."
    ),
    status_code=HTTPStatusCode.OK,
)
async def get_geo(ip: str = Query(..., description="The IPv4 address to lookup")) -> GeoResponse:
    """
    Get geolocation information for a provided IP address.

    Args:
        ip (str): The IPv4 address to query.

    Returns:
        GeoResponse: A Pydantic model containing geolocation details.

    Raises:
        HTTPException: Returns 400 Bad Request if IP is invalid.
    """
    try:
        return await geo_service.get_geo(ip)
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatusCode.BAD_REQUEST, detail=str(e))


@router.get(
    "/me",
    response_model=GeoResponse,
    summary="Get geolocation for the client IP",
    description=(
        "Automatically detect the client's IP from the request and return geolocation information. "
        "This endpoint is useful to determine the location of the client making the request. "
        "Returns HTTP 400 if the client's IP cannot be determined or is invalid."
    ),
    status_code=HTTPStatusCode.OK,
)
async def get_geo_me(request: Request) -> GeoResponse:
    """
    Get geolocation information for the requesting client's IP address.

    Args:
        request (Request): FastAPI request object to detect client IP.

    Returns:
        GeoResponse: A Pydantic model containing geolocation details.

    Raises:
        HTTPException: Returns 400 Bad Request if IP cannot be resolved.
    """
    try:
        return await geo_service.get_geo_from_request(request)
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatusCode.BAD_REQUEST, detail=str(e))

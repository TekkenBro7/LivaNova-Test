from pydantic import BaseModel, Field


class IPAPIResponse(BaseModel):
    """
    Represents the raw response returned by the IP-API service.

    Attributes:
        status: Status of the API request, typically "success" or "fail".
        message: Optional error message when status is "fail".
        continent: Continent name.
        continentCode: Continent code (e.g., "EU").
        country: Country name.
        countryCode: ISO country code (e.g., "BY").
        region: Region code.
        regionName: Full region name.
        city: City name.
        district: District name.
        zip: Postal code.
        lat: Latitude coordinate.
        lon: Longitude coordinate.
        timezone: Timezone string (e.g., "Europe/Minsk").
        offset: UTC offset in seconds.
        currency: Currency code (e.g., "BYN").
        isp: Internet Service Provider.
        org: Organization name.
        as_: Autonomous system (AS) number and name.
        asname: AS name.
        reverse: Reverse DNS for the IP.
        mobile: True if the IP is a mobile connection.
        proxy: True if the IP is a proxy.
        hosting: True if the IP is hosting server.
        query: The queried IP address.
    """

    status: str
    message: str | None = None
    continent: str | None = None
    continentCode: str | None = None
    country: str | None = None
    countryCode: str | None = None
    region: str | None = None
    regionName: str | None = None
    city: str | None = None
    district: str | None = None
    zip: str | None = None
    lat: float | None = None
    lon: float | None = None
    timezone: str | None = None
    offset: int | None = None
    currency: str | None = None
    isp: str | None = None
    org: str | None = None
    as_: str | None = Field(None, alias="as")
    asname: str | None = None
    reverse: str | None = None
    mobile: bool | None = None
    proxy: bool | None = None
    hosting: bool | None = None
    query: str

from pydantic import BaseModel, Field


class IPAPIResponse(BaseModel):
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

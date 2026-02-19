from pydantic import BaseModel, Field


class GeoResponse(BaseModel):
    ip: str = Field(..., examples=["46.53.134.81"])
    country: str | None = Field(default=None, examples=["Belarus"])
    country_code: str | None = Field(default=None, examples=["BY"])
    region: str | None = Field(default=None, examples=["Minsk City"])
    city: str | None = Field(default=None, examples=["Minsk"])
    zip: str | None = Field(default=None, examples=["220004"])
    latitude: float | None = Field(default=None, examples=[53.901])
    longitude: float | None = Field(default=None, examples=[27.5707])
    timezone: str | None = Field(default=None, examples=["Europe/Minsk"])
    isp: str | None = Field(default=None, examples=["Unitary enterprise A1"])
    is_mobile: bool | None = Field(default=None, examples=[False])
    is_proxy: bool | None = Field(default=None, examples=[False])
    is_hosting: bool | None = Field(default=None, examples=[False])

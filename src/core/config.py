import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    APP_NAME: str = os.getenv("APP_NAME", "IP Geolocation Service")

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOGS_DIR: str = os.getenv("LOGS_DIR", "logs")

    HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("APP_PORT", 8000))
    RELOAD: bool = os.getenv("APP_RELOAD", "True").lower() in ("true", "1")


class GeoConfig:
    IP_API_BASE_URL: str = os.getenv(
        "IP_API_BASE_URL",
        "http://ip-api.com/json",
    )

    TIMEOUT: float = float(
        os.getenv(
            "IP_API_TIMEOUT",
            10,
        )
    )

    FIELDS: str = os.getenv(
        "IP_API_FIELDS",
        (
            "status,message,query,"
            "continent,continentCode,"
            "country,countryCode,"
            "region,regionName,"
            "city,zip,"
            "lat,lon,"
            "timezone,"
            "isp,org,"
            "mobile,proxy,hosting"
        ),
    )


base_config = BaseConfig()
geo_config = GeoConfig()

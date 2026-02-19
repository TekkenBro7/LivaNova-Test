from src.services.geolocation_service import GeoIPService


def get_geo_service() -> GeoIPService:
    return GeoIPService()

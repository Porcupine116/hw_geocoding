from geocoders.geocoder import Geocoder
from api import API

# Алгоритм "в лоб"
class SimpleQueryGeocoder(Geocoder):
    def _apply_geocoding(self, area_id: str) -> str:
        """
            TODO:
            - Делать запросы к API для каждой area
            - Для каждого ответа формировать полный адрес
        """

        full_address = []
        while area_id:
            data = API.get_area(area_id)
            full_address.insert(0, data.name)
            area_id = data.parent_id
            return ', '.join(full_address)
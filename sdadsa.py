from api import TreeNode, API
from geocoders.geocoder import Geocoder


class MemorizedTreeGeocoder(Geocoder):
    def __init__(self, samples: int | None = None, data: list[TreeNode] | None = None):
        super().__init__(samples=samples)
        if data is None:
            self.__data = API.get_areas()
        else:
            self.__data = data

    def _apply_geocoding(self, area_id: str) -> str:
        address_dict = {}
        stack = []

        for node in self.__data:
            stack.append((node, [node]))

        while stack:
            node, path = stack.pop()
            current_path = f"{path}/{node.name}" if path else node.name
            address = ','.join(current_path.split('/') + [node.id])
            address_dict[node.id] = address

            for child_node in node.areas:
                stack.append((child_node, current_path))

        if area_id in address_dict:
            return address_dict[area_id]
        else:
            return f"Address not found for {area_id}"


class SimpleTreeGeocoder(Geocoder):
    def __init__(self, samples: int | None = None, data: list[TreeNode] | None = None):
        super().__init__(samples=samples)
        if data is None:
            self.__data = API.get_areas()
        else:
            self.__data = data

    def _apply_geocoding(self, area_id: str) -> str:

        stack = []

        for node in self.__data:
            stack.append((node, [node]))

        while stack:
            current_node, path = stack.pop()

            if current_node.id == area_id:
                full_adds = " ".join([n.name for n in path])
                return f"{area_id}: {full_adds}"

            for child_node in current_node.areas:
                stack.append((child_node, path + [child_node]))


class SimpleQueryGeocoder(Geocoder):
    def _apply_geocoding(self, area_id: str) -> str:

        node = API.get_area(area_id)
        full_adds = []
        full_adds.append(node.name)

        if node.parent_id is None:
            return ' '.join(full_adds)

        while node.parent_id:
            node = API.get_area(node.parent_id)
            full_adds.append(node.name)

            return ' '.join(full_adds)
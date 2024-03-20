from api import TreeNode, API
from geocoders.geocoder import Geocoder


# Инверсия дерева
class MemorizedTreeGeocoder(Geocoder):
    def __init__(self, samples, data):
        super().__init__(samples=samples)
        if data is None:
            self.__data = API.get_areas()
        else:
            self.__data = data
        self.address_dict = {}


    """
        TODO:
        Сделать функцию перебора дерева:
        - Для каждого узла сохранять в словарь адресов
    """

    def _traverse_tree(self, node: TreeNode, path: str = ""):

        current_path = f"{path}/{node.name}" if path else node.name

        self.address_dict[node.id] = current_path

        for child_node in node.areas:
            self._traverse_tree(child_node, current_path)


    def _apply_geocoding(self, area_id: str) -> str:
        """
            TODO:
            - Возвращать данные из словаря с адресами
        """
        if area_id in self.address_dict:
            return self.address_dict[area_id]

    def _build_address_dict(self, node, path):
        address = ','.join(path + [node.address])
        self.address_dict[node.area_id] = address
        for child in node.children:
            self._build_address_dict(child, path + [node.address])


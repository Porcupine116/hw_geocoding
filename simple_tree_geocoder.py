from api import API, TreeNode
from geocoders.geocoder import Geocoder


# Перебор дерева
class SimpleTreeGeocoder(Geocoder):
    def __init__(self, samples, data):
        super().__init__(samples=samples)
        if data is None:
            self.__data = API.get_areas()
        else:
            self.__data = data

    def _traverse_tree(self, node: TreeNode, target_id: str, path: list[TreeNode] = []):

        path.append(node)

        if node.id == target_id:
            return path

        for child_node in node.areas:
            found_path = self._traverse_tree(child_node, target_id, path.copy())
            if found_path is not None:
                return found_path

    def _apply_geocoding(self, area_id: str) -> str:

        for node in self.__data:
            path = self._traverse_tree(node, area_id, [])
            if path:
                address = " / ".join([n.name for n in path])
                return f"Полный адрес для {area_id}: {address}"
        """
            TODO:
            - Сделать перебор дерева для каждого area_id
            - В ходе перебора возвращать массив элементов, состоящих из TreeNode необходимой ветки
            - Из массива TreeNode составить полный адрес
        """





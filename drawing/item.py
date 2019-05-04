from typing import List


class Item:

    def __init__(self, vertices: List[int], type_item: int):
        self.vertices = ('v2i', tuple(vertices))
        self.type = type_item


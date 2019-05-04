import random
import shapes
from exceptions import exception
from scene import Scene
from typing import List, Dict, Set


class Figure:

    def __init__(self, scene: Scene):
        self._scene = scene
        self._state = []  # type: List[Dict[str, List or int]]
        self._current_figure = -1

    def new_figure(self):
        shape_number = random.randint(0, len(shapes.shapes) - 1)
        shape = shapes.shapes[shape_number]
        shape_height = shapes.shape_height(shape)

        shape = shapes.move_top(shapes.move_right(shapes.shapes[shape_number], 3),
                                self._scene.height - shape_height - 1)
        return shape
        # self._current_shape = self._draw_shape(shape)

        # return self._current_shape

    def get_current_figure(self):
        if self._current_figure < 0 or self._current_figure >= len(self._state):
            return []

        return self._state[self._current_figure]

    def store_figure(self, shape: List, gl_type: int, index: int):
        if index >= len(self._state):
            raise exception.UndefinedIndexError("index %d: is out of range" % index)
        if index < 0:
            self._state.append({'shape': shape, 'type': gl_type})
            index = len(self._state) - 1
        else:
            self._state[index] = {'shape': shape, 'type': gl_type}

        return index

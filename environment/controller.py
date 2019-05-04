from pyglet.gl import *
from exceptions import exception
import shapes
import random
from drawing.draw import Draw
from drawing.scale import Scale
from scene import Scene
from environment.trash import Trash
from typing import List, Dict, Set


class Controller:

    def __init__(self, window: pyglet.window.Window):
        if not isinstance(window, pyglet.window.Window):
            raise exception.IncorrectTypeError("window must be a pyglet.window.Window instance")

        self._scene = Scene(10, 20)
        self._draw_object = Draw(Scale(window, self._scene))
        self.state = []  # type: List[Dict[str, List or int]]
        self._trash = Trash(self._scene)
        self._current_shape = -1
        self._draw_grid()
        self._draw_boundaries()

    def _new_shape(self):
        shape_number = random.randint(0, len(shapes.shapes) - 1)
        shape = shapes.shapes[shape_number]
        shape_height = shapes.shape_height(shape)

        shape = shapes.move_top(shapes.move_right(shapes.shapes[shape_number], 3),
                                self._scene.height - shape_height - 1)
        self._current_shape = self._draw_shape(shape)

        return self._current_shape

    def _get_current_shape(self):
        if self._current_shape < 0 or self._current_shape >= len(self.state):
            self._new_shape()

        return self.state[self._current_shape]

    def control(self, symbol: int):
        current_shape = self._get_current_shape()
        shape_candidate = []
        if symbol == pyglet.window.key.UP:
            shape_candidate = shapes.move_top(current_shape['shape'], 1)
        elif symbol == pyglet.window.key.DOWN:
            self._move_down(True)
            return
        elif symbol == pyglet.window.key.LEFT:
            shape_candidate = shapes.move_left(current_shape['shape'], 1)
        elif symbol == pyglet.window.key.RIGHT:
            shape_candidate = shapes.move_right(current_shape['shape'], 1)
        elif symbol == pyglet.window.key.SPACE:
            shape_candidate = shapes.rotate(current_shape['shape'])

        if len(shape_candidate) > 0:
            self._draw_shape(shape_candidate, self._current_shape)

    def tick(self, dt):
        self._move_down()

    def _move_down(self, fall=False):
        current_shape = self._get_current_shape()
        shape_candidate = shapes.move_bottom(current_shape['shape'], 1)
        result = self._draw_shape(shape_candidate, self._current_shape)
        while result >= 0 and fall:
            shape_candidate = shapes.move_bottom(shape_candidate, 1)
            result = self._draw_shape(shape_candidate, self._current_shape)

        if result < 0:
            old_shape = self._current_shape
            self._current_shape = -1
            self._trash.put(self.state[old_shape]['shape'])
            del self.state[old_shape]

    def _draw_grid(self):
        dots = []

        for x in range(self._scene.width+1):
            for y in range(self._scene.height):
                if y == 0:
                    continue
                dots.append([x, y])

        self._draw_dots(dots)

    def _draw_boundaries(self):
        self._draw_lines([[0, self._scene.height-1], [0, 1]])
        self._draw_lines([[0, 1], [self._scene.width, 1]])
        self._draw_lines([[self._scene.width, 1], [self._scene.width, self._scene.height-1]])

    def _check_if_fits(self, coordinates: List, strict: bool):
        shape_candidate = []  # type: List

        for item in coordinates:
            if self._trash.is_set(item):
                continue

            if 0 <= item[0] < self._scene.width and 0 < item[1] <= self._scene.height:
                shape_candidate.append(item)

        if strict and len(shape_candidate) < len(coordinates):
            raise exception.OutOfRangeError("shape doesn't fit scene")

        return shape_candidate

    def _store_shape(self, shape: List, gl_type: int, index: int):
        if index >= len(self.state):
            raise exception.UndefinedIndexError("index %d: is out of range" % index)
        if index < 0:
            self.state.append({'shape': shape, 'type': gl_type})
            index = len(self.state) - 1
        else:
            self.state[index] = {'shape': shape, 'type': gl_type}

        return index

    def _draw(self, shape_candidate: List, gl_type: int, index: int, strict=False):
        try:
            if strict:
                shape_candidate = self._check_if_fits(shape_candidate, strict)
            index = self._store_shape(shape_candidate, gl_type, index)
        except exception.OutOfRangeError as e:
            return -1

        return index

    def _draw_dots(self, shape_candidate: List, index=-1):
        return self._draw(shape_candidate, Draw.DOTS, index)

    def _draw_lines(self, shape_candidate: List, index=-1):
        return self._draw(shape_candidate, Draw.LINE, index, False)

    def _draw_shape(self, shape_candidate: List, index=-1):
        return self._draw(shape_candidate, Draw.SQUARE, index, True)

    def refresh(self, batch):
        self._draw_object.draw_shape(self._trash.get_array(), batch)
        for item in self.state:
            if item['type'] == Draw.DOTS:
                self._draw_object.draw_dots(item['shape'], batch)
            elif item['type'] == Draw.LINE:
                self._draw_object.draw_lines(item['shape'], batch)
            else:
                self._draw_object.draw_shape(item['shape'], batch)

        return self._trash.get_score()

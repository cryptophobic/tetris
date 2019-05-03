from pyglet.gl import *
import exception
import shapes
import random
from draw import Draw
from scene import Scene


class Environment:

    def __init__(self, window):
        if not isinstance(window, pyglet.window.Window):
            raise exception.IncorrectTypeError("window must be a pyglet.window.Window instance")

        self._scene = Scene(10, 20)
        self._draw_object = Draw(window, self._scene)
        self.state = []
        self.trash = {}
        self._current_shape = -1
        self._draw_grid()

    def _new_shape(self):
        shape_number = random.randint(0, len(shapes.shapes) - 1)
        shape_number = 6
        shape = shapes.shapes[shape_number]
        shape_height = shapes.shape_height(shape)

        shape = shapes.move_top(shapes.move_right(shapes.shapes[shape_number], 3),
                                self._scene.height - shape_height - 1)
        self._current_shape = self._draw_polygon(shape)

        return self._current_shape

    def _get_current_shape(self):
        if self._current_shape < 0 or self._current_shape >= len(self.state):
            self._new_shape()

        return self.state[self._current_shape]

    def control(self, symbol):
        current_shape = self._get_current_shape()
        shape_candidate = []
        if symbol == pyglet.window.key.UP:
            shape_candidate = shapes.move_top(current_shape['shape'], 1)
        elif symbol == pyglet.window.key.DOWN:
            shape_candidate = shapes.move_bottom(current_shape['shape'], 1)
        elif symbol == pyglet.window.key.LEFT:
            shape_candidate = shapes.move_left(current_shape['shape'], 1)
        elif symbol == pyglet.window.key.RIGHT:
            shape_candidate = shapes.move_right(current_shape['shape'], 1)
        elif symbol == pyglet.window.key.SPACE:
            shape_candidate = shapes.rotate(current_shape['shape'])

        if len(shape_candidate) > 0:
            result = self._draw_polygon(shape_candidate, self._current_shape)
            if symbol == pyglet.window.key.DOWN and result < 0:
                old_shape = self._current_shape
                self._current_shape = -1
                self.put_to_trash(old_shape)

    def tick(self, dt):
        self.control(pyglet.window.key.DOWN)

    def put_to_trash(self, new_trash_id):
        shape = self.state[new_trash_id]['shape']

        for item in shape:
            if not item[1] in self.trash.keys():
                self.trash[item[1]] = set()
            self.trash[item[1]].add(item[0])

        del self.state[new_trash_id]
        print(shape)
        #print(self.trash)

    def _draw_grid(self):
        dots = []

        for x in range(self._scene.width):
            for y in range(self._scene.height):
                dots.append([x, y])

        self._draw_dots(dots)

    def _check_if_fits(self, coordinates, strict):
        shape_candidate = []

        for item in coordinates:
            if 0 <= item[0] < self._scene.width and 0 < item[1] < self._scene.height:
                shape_candidate.append(item)

        if strict and len(shape_candidate) < len(coordinates):
            raise exception.OutOfRangeError("shape doesn't fit scene")

        return shape_candidate

    def _store_shape(self, shape, gl_type, index):
        if index >= len(self.state):
            raise exception.UndefinedIndexError("index %d: is out of range" % index)
        if index < 0:
            self.state.append({'shape': shape, 'type': gl_type})
            index = len(self.state) - 1
        else:
            self.state[index] = {'shape': shape, 'type': gl_type}

        return index

    def _draw(self, shape_candidate, gl_type, index, strict=False):
        try:
            shape_candidate = self._check_if_fits(shape_candidate, strict)
            self._draw_object.draw(gl_type, shape_candidate)
            index = self._store_shape(shape_candidate, gl_type, index)
        except exception.OutOfRangeError as e:
            print(e)
            return -1

        return index

    def _draw_dots(self, shape_candidate, index=-1):
        return self._draw(shape_candidate, Draw.DOTS, index)

    def _draw_polygon(self, shape_candidate, index=-1):
        return self._draw(shape_candidate, Draw.POLYGON, index, True)

    def refresh(self):
        self.resize()
        self._draw_object.refresh()

        for index in range(len(self.state)):
            self._draw(self.state[index]['shape'], self.state[index]['type'], index)

    def resize(self):
        self._draw_object.resize()

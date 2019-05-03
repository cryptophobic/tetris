from pyglet.gl import *
import exception
import shapes
from draw import Draw
from scene import Scene


class Environment:

    def __init__(self, window):
        if not isinstance(window, pyglet.window.Window):
            raise exception.IncorrectTypeError("window must be a pyglet.window.Window instance")

        self._scene = Scene(10, 20)
        self._draw_object = Draw(window, self._scene)

        shape = shapes.move_top(shapes.move_right(shapes.shape_triple, 3), 4)

        self._shape = {'shape': shape, 'index': -1}

    def left(self):
        self._draw(shapes.move_left(self._shape['shape'], 1))

    def right(self):
        self._draw(shapes.move_right(self._shape['shape'], 1))

    def rotate(self):
        self._draw(shapes.rotate(self._shape['shape']))

    def up(self):
        self._draw(shapes.move_top(self._shape['shape'], 1))

    def down(self):
        self._draw(shapes.move_botttom(self._shape['shape'], 1))

    def _draw(self, shape_candidate):
        try:
            self._shape['index'] = self._draw_object.draw_polygon(shape_candidate, self._shape['index'], True)
            self._shape['shape'] = shape_candidate
        except exception.OutOfRangeError as e:
            print(e)

    def refresh(self):
        self._draw_object.redraw()

    def resize(self):
        self._draw_object.resize()


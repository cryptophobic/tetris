from pyglet.gl import *
from scene import Scene


class UndefinedIndexError(Exception):
    pass


class IncorrectTypeError(Exception):
    pass


class OutOfRangeError(Exception):
    pass


class Draw:

    def __init__(self, window, scene):
        if not isinstance(window, pyglet.window.Window):
            raise IncorrectTypeError("window must be a pyglet.window.Window instance")

        if not isinstance(scene, Scene):
            raise IncorrectTypeError("scene must be a scene.Scene instance")

        self._window = window
        self._scene = scene
        self._scene_denominator = -1
        self.state = []
        self.draw_grid()

    def _set_scene_denominator(self):

        if self._window.width < self._scene.width or self._window.height < self._scene.height:
            raise OutOfRangeError("too small window %d/%d vs %d/%d" % (self._window.width, self._window.height, self._scene.width, self._scene.height))

        window_ratio = self._window.width / self._window.height
        scene_ratio = self._scene.width / self._scene.height

        if window_ratio > scene_ratio:
            self._scene_denominator = self._window.height / self._scene.height
        else:
            self._scene_denominator = self._window.width / self._scene.width

    def get_scene_denominator(self):
        if self._scene_denominator < 0:
            self._set_scene_denominator()

        return self._scene_denominator

    def _scale(self, index):
        return [int(coord*self.get_scene_denominator()) for coord in self.state[index]]

    @staticmethod
    def _get_array_from_shape(shape_array):
        result = []

        for item in shape_array:
            result += item

        return result

    def _check_and_get_index(self, coordinates, index):
        if index < 0:
            self.state.append(self._get_array_from_shape(coordinates))
            index = len(self.state) - 1
        elif index >= len(self.state):
            raise UndefinedIndexError("index %d: is out of range" % index)

        return index

    def draw_grid(self):
        dots = []
        denominator = self.get_scene_denominator()

        for x in range(int(self._window.width / denominator)):
            for y in range(int(self._window.height / denominator)):
                dots.append([x, y])

        self.draw_dots(dots)

    def draw_dots(self, dots, index=-1):
        index = self._check_and_get_index(dots, index)
        pyglet.graphics.draw(len(self.state[index]) // 2, pyglet.gl.GL_POINTS, ('v2i', self._scale(index)))

        return index

    def draw_polygon(self, polygon, index=-1):
        index = self._check_and_get_index(polygon, index)
        pyglet.graphics.draw(len(self.state[index]) // 2, pyglet.gl.GL_POLYGON, ('v2i', self._scale(index)))

        return index

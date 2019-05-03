from pyglet.gl import *
from scene import Scene
import exception
import shapes


class Draw:

    def __init__(self, window, scene):
        if not isinstance(window, pyglet.window.Window):
            raise exception.IncorrectTypeError("window must be a pyglet.window.Window instance")

        if not isinstance(scene, Scene):
            raise exception.IncorrectTypeError("scene must be a scene.Scene instance")

        self._move_vector = [0, 0]
        self._window = window
        self._scene = scene
        self._scene_denominator = -1
        self.state = []
        #self.draw_grid()

    def _set_scene_denominator(self):

        if self._window.width < self._scene.width or self._window.height < self._scene.height:
            raise exception.OutOfRangeError("too small window %d/%d vs %d/%d" % (self._window.width, self._window.height, self._scene.width, self._scene.height))

        window_ratio = self._window.width / self._window.height
        scene_ratio = self._scene.width / self._scene.height

        # scene thin and tall
        if window_ratio > scene_ratio:
            self._scene_denominator = self._window.height / self._scene.height
            x_move = int((self._window.width - self._scene_denominator * self._scene.width) / 2)
            self._move_vector = [x_move, 0]
        # scene thick and short
        else:
            self._scene_denominator = self._window.width / self._scene.width

    def get_scene_denominator(self):
        if self._scene_denominator < 0:
            self._set_scene_denominator()

        return self._scene_denominator

    def _scale(self, index):
        result = []

        for item in self.state[index]:

            result += [int(item[0]*self.get_scene_denominator() + self._move_vector[0]),
                       int(item[1]*self.get_scene_denominator() + self._move_vector[1])]

        return result

    def _get_array_from_shape(self, shape_array):
        result = []

        for item in shape_array:
            # if item[0] < 0:
            #     return self._get_array_from_shape(shapes.move_right(shape_array))
            # if item[0] > self._scene.width:
            #     return self._get_array_from_shape(shapes.move_left(shape_array))
            # if item[1] < 0:
            #     return self._get_array_from_shape(shapes.move_top(shape_array))
            # if item[1] >= self._scene.height:
            #     return self._get_array_from_shape(shapes.move_botttom(shape_array))
            if 0 <= item[0] < self._scene.width and 0 < item[1] < self._scene.height:
                result.append(item)

        return result

    def _check_and_get_index(self, coordinates, index, strict):
        if index >= len(self.state):
            raise exception.UndefinedIndexError("index %d: is out of range" % index)

        shape_candidate = self._get_array_from_shape(coordinates)

        if strict and len(shape_candidate) < len(coordinates):
            raise exception.OutOfRangeError("shape doesn't fit scene")

        if index < 0:
            self.state.append(shape_candidate)
            index = len(self.state) - 1
        else:
            self.state[index] = shape_candidate

        return index

    def draw_grid(self):
        dots = []
        denominator = self.get_scene_denominator()

        for x in range(int(self._window.width / denominator)):
            for y in range(int(self._window.height / denominator)):
                dots.append([x, y])

        self.draw_dots(dots)

    def resize(self):
        self._scene_denominator = -1

    def redraw(self):
        self.resize()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        for index in range(len(self.state)):
            self.draw_polygon(self.state[index], index)

    def draw_dots(self, dots, index=-1, strict=False):
        index = self._check_and_get_index(dots, index, strict)
        scaled = self._scale(index)
        pyglet.graphics.draw(len(scaled) // 2, pyglet.gl.GL_POINTS, ('v2i', scaled))

        return index

    def draw_polygon(self, polygon, index=-1, strict=False):
        index = self._check_and_get_index(polygon, index, strict)
        scaled = self._scale(index)
        pyglet.graphics.draw(len(scaled) // 2, pyglet.gl.GL_POLYGON, ('v2i', scaled))

        return index

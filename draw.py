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
        self.draw_grid()

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

        for item in self.state[index]['shape']:
            result += [int(item[0]*self.get_scene_denominator() + self._move_vector[0]),
                       int(item[1]*self.get_scene_denominator() + self._move_vector[1])]

        return result

    def _check_and_get_index(self, coordinates, strict):
        shape_candidate = []

        for item in coordinates:
            # if item[0] < 0:
            #     return self._get_array_from_shape(shapes.move_right(shape_array))
            # if item[0] > self._scene.width:
            #     return self._get_array_from_shape(shapes.move_left(shape_array))
            # if item[1] < 0:
            #     return self._get_array_from_shape(shapes.move_top(shape_array))
            # if item[1] >= self._scene.height:
            #     return self._get_array_from_shape(shapes.move_botttom(shape_array))
            if 0 <= item[0] < self._scene.width and 0 < item[1] < self._scene.height:
                shape_candidate.append(item)

        if strict and len(shape_candidate) < len(coordinates):
            raise exception.OutOfRangeError("shape doesn't fit scene")

        return shape_candidate

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
            self._draw(self.state[index]['type'], self.state[index]['shape'], index, False)

    def draw_dots(self, dots, index=-1, strict=False):
        return self._draw(pyglet.gl.GL_POINTS, dots, index, strict)

    def draw_polygon(self, polygon, index=-1, strict=False):
        return self._draw(pyglet.gl.GL_POLYGON, polygon, index, strict)

    def _draw(self, gl_type, shape, index, strict):
        shape_candidate = self._check_and_get_index(shape, strict)
        index = self._store_shape(shape_candidate, gl_type, index)
        scaled = self._scale(index)
        pyglet.graphics.draw(len(scaled) // 2, gl_type, ('v2i', scaled))

        return index

    def _store_shape(self, shape, gl_type, index):
        if index >= len(self.state):
            raise exception.UndefinedIndexError("index %d: is out of range" % index)
        if index < 0:
            self.state.append({'shape': shape, 'type': gl_type})
            index = len(self.state) - 1
        else:
            self.state[index] = {'shape': shape, 'type': gl_type}

        return index


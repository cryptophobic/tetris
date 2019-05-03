from pyglet.gl import *
from scene import Scene
import exception


class Draw:

    POLYGON = pyglet.gl.GL_POLYGON

    DOTS = pyglet.gl.GL_POINTS

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

    def _scale(self, shape):
        result = []

        for item in shape:
            result += [int(item[0]*self.get_scene_denominator() + self._move_vector[0]),
                       int(item[1]*self.get_scene_denominator() + self._move_vector[1])]

        return result

    @staticmethod
    def refresh():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

    def resize(self):
        self._scene_denominator = -1

    def draw_dots(self, dots):
        return self.draw(pyglet.gl.GL_POINTS, dots)

    def draw_polygon(self, polygon):
        return self.draw(pyglet.gl.GL_POLYGON, polygon)

    def draw(self, gl_type, shape):
        scaled = self._scale(shape)
        pyglet.graphics.draw(len(scaled) // 2, gl_type, ('v2i', scaled))

        return gl_type


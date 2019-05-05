from typing import List
from scene import Scene
from exceptions import exception
import pyglet


class Scale:

    def __init__(self, window: pyglet.window.Window, scene: Scene):
        if not isinstance(window, pyglet.window.Window):
            raise exception.IncorrectTypeError("window must be a pyglet.window.Window instance")

        if not isinstance(scene, Scene):
            raise exception.IncorrectTypeError("scene must be a scene.Scene instance")

        self._move_vector = [0, 0]  # type: List[int, int]
        self._window = window
        self._scene = scene
        self._window_size = [0, 0]
        self._scene_denominator = 0.0

    def _set_scene_denominator(self):

        if self._window.width < self._scene.width or self._window.height < self._scene.height:
            raise exception.OutOfRangeError("too small window %d/%d vs %d/%d" % (self._window.width, self._window.height, self._scene.width, self._scene.height))

        window_ratio = self._window.width / self._window.height
        scene_ratio = self._scene.width / self._scene.height

        # scene thin and tall
        if window_ratio > scene_ratio:
            self._scene_denominator = self._window.height / self._scene.height
        # scene thick and short
        else:
            self._scene_denominator = self._window.width / self._scene.width

        self._x_positioning(window_ratio, scene_ratio)
        self._y_positioning(window_ratio, scene_ratio)

        self._window_size = self._window.get_size()

    def _x_positioning(self, window_ratio: float, scene_ratio: float):
        x_move = 0

        if self._scene.x_position == Scene.CENTER and window_ratio > scene_ratio:
            x_move = int((self._window.width - self._scene_denominator * self._scene.width) / 2)

        if self._scene.x_position == Scene.RIGHT and window_ratio > scene_ratio:
            x_move = int(self._window.width - self._scene_denominator * self._scene.width)

        self._move_vector[0] = x_move

    def _y_positioning(self, window_ratio: float, scene_ratio: float):
        y_move = 0

        if self._scene.y_position == Scene.CENTER and window_ratio < scene_ratio:
            y_move = int((self._window.height - self._scene_denominator * self._scene.height) / 2)

        if self._scene.y_position == Scene.TOP and window_ratio < scene_ratio:
            y_move = int(self._window.height - self._scene_denominator * self._scene.height)

        self._move_vector[1] = y_move

    def get_scene_denominator(self):
        if self._window.get_size() != self._window_size:
            self._set_scene_denominator()

        return self._scene_denominator

    def scale_shape(self, shape: List):
        result = []
        denominator = self.get_scene_denominator()

        for item in shape:
            square = [
                int(item[0] * denominator + self._move_vector[0]),
                int(item[1] * denominator + self._move_vector[1]),

                int(item[0] * denominator + self._move_vector[0] + denominator),
                int(item[1] * denominator + self._move_vector[1]),

                int(item[0] * denominator + self._move_vector[0] + denominator),
                int(item[1] * denominator + self._move_vector[1] + denominator),

                int(item[0] * denominator + self._move_vector[0]),
                int(item[1] * denominator + self._move_vector[1] + denominator),
            ]
            result.append(square)

        return result

    def scale_line(self, shape: List):
        result = []
        denominator = self.get_scene_denominator()

        for item in shape:
            result += [
                int(item[0] * denominator + self._move_vector[0]),
                int(item[1] * denominator + self._move_vector[1]),
            ]

        return result

    def scale_dots(self, shape: List):
        result = []

        for item in shape:
            result += [int(item[0]*self.get_scene_denominator() + self._move_vector[0]),
                       int(item[1]*self.get_scene_denominator() + self._move_vector[1])]

        return result


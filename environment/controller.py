from pyglet.gl import *

from environment.action import Action
from exceptions import exception
from drawing.draw import Draw
from drawing.scale import Scale
from scene import Scene
from environment.objects import Objects


class Controller:

    def __init__(self, window: pyglet.window.Window):
        if not isinstance(window, pyglet.window.Window):
            raise exception.IncorrectTypeError("window must be a pyglet.window.Window instance")

        self._scene = Scene(10, 20)
        self._draw_object = Draw(Scale(window, self._scene))
        self._objects = Objects(self._scene)

        self._draw_grid()
        self._draw_boundaries()

    def control(self, symbol: int):
        action = Action(symbol)
        if action.action is not None:
            self._objects.perform_action(action)

    def tick(self, dt):
        self._objects.move_down()

    def _draw_grid(self):
        dots = []

        for x in range(self._scene.width+1):
            for y in range(self._scene.height):
                if y == 0:
                    continue
                dots.append([x, y])

        self._objects.register_dots(dots)

    def _draw_boundaries(self):
        self._objects.register_dots([[0, self._scene.height-1], [0, 1]])
        self._objects.register_dots([[0, 1], [self._scene.width, 1]])
        self._objects.register_dots([[self._scene.width, 1], [self._scene.width, self._scene.height-1]])

    def refresh(self, batch):
        self._draw_object.draw_list(self._objects.get_array(), batch)
        return self._objects.get_score()

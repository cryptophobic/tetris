from pyglet.gl import *

from controller.base_controller import BaseController
from environment.action import Action
from scene import Scene
from environment.objects import Objects


class BucketController(BaseController):

    def __init__(self, window: pyglet.window.Window, scene: Scene):
        BaseController.__init__(self, window, scene)
        self._objects = Objects(self._scene)

        self._paused = False
        self._draw_grid()
        self._draw_boundaries()

    def control(self, symbol: int):
        action = Action(symbol)
        if action.action is not None:
            if action.action == Action.PAUSE:
                self._paused = True if self._paused == False else False
            elif not self._paused:
                self._objects.perform_action(action)

    def tick(self, dt):
        if not self._paused:
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
        self._objects.register_lines([[0, self._scene.height-1], [0, 1]])
        self._objects.register_lines([[0, 1], [self._scene.width, 1]])
        self._objects.register_lines([[self._scene.width, 1], [self._scene.width, self._scene.height-1]])

    def refresh(self, batch):
        self._draw_object.draw_list(self._objects.get_array(), batch)
        return [self._objects.get_lines(), self._objects.get_score()]

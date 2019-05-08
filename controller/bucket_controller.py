from pyglet.gl import *

from controller.base_controller import BaseController
from environment.action import Action
from exceptions import exception
from scene import Scene
from environment.objects import Objects


class BucketController(BaseController):

    def __init__(self, window: pyglet.window.Window, scene: Scene):
        BaseController.__init__(self, window, scene)
        self._objects = Objects(self._scene)

        self._paused = False
        self.game_over = False
        self._draw_grid()
        self._draw_boundaries()

    def re_init(self):
        self._objects = Objects(self._scene)

        self._paused = False
        self.game_over = False
        self._draw_grid()
        self._draw_boundaries()

    def clear(self):
        self._objects.clear()

    def control(self, symbol: int):
        action = Action(symbol)

        if action.action is not None:
            if action.action == Action.PAUSE:
                self._paused = True if not self._paused else False
            elif action.action == Action.EXIT:
                exit()
            elif not self._paused:
                try:
                    self._objects.perform_action(action)
                except exception.GameOverError as e:
                    self.game_over = True

    def tick(self, dt):
        try:
            if not self._paused:
                self._objects.move_down()
        except exception.GameOverError as e:
            self.game_over = True

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

    def get_stats(self):
        return [self._objects.get_lines(), self._objects.get_score(), self._objects.get_one(), self._objects.get_twix(),
                self._objects.get_triple(), self._objects.get_tetris()]

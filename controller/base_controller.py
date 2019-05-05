import abc
from pyglet.gl import *
from scene import Scene
from exceptions import exception
from drawing.draw import Draw
from drawing.scale import Scale


class BaseController:
    def __init__(self, window: pyglet.window.Window, scene: Scene):
        if not isinstance(window, pyglet.window.Window):
            raise exception.IncorrectTypeError("window must be a pyglet.window.Window instance")
        if not isinstance(scene, Scene):
            raise exception.IncorrectTypeError("scene must be a scene.Scene instance")

        self._scene = scene
        self._draw_object = Draw(Scale(window, self._scene))

    @abc.abstractmethod
    def refresh(self, batch: pyglet.graphics.Batch):
        """refresh scene"""

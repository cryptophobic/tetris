from pyglet.gl import *


class Action:

    LEFT = 1
    RIGHT = 2
    UP = 4
    DOWN = 8
    FIRE = 16
    PAUSE = 32

    action_mapping = {
        pyglet.window.key.ESCAPE: PAUSE,
        pyglet.window.key.LEFT: LEFT,
        pyglet.window.key.RIGHT: RIGHT,
        pyglet.window.key.UP: UP,
        pyglet.window.key.DOWN: DOWN,
        pyglet.window.key.SPACE: FIRE
    }

    def __init__(self, input_data: int):
        if input_data in self.action_mapping.keys():
            self.action = self.action_mapping[input_data]
        else:
            self.action = None

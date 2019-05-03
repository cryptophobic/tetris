from pyglet.gl import *

import shapes
from environment import Environment


# print(range(33))
#
# exit()

window = pyglet.window.Window(resizable=True)
environment = Environment(window)


def on_draw():
    environment.refresh()


def on_resize(width, height):
    environment.resize()


def on_key_press(symbol, modifiers):
    environment.control(symbol)


pyglet.clock.schedule_interval(environment.tick, 0.5)
#window.on_resize = on_resize
window.on_draw = on_draw
window.on_key_press = on_key_press
pyglet.app.run()

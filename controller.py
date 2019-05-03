from pyglet.gl import *

import shapes
from environment import Environment


# print(range(33))
#
# exit()

window = pyglet.window.Window(resizable=True)
environment = Environment(window)


def on_draw():
    print('draw')
    environment.refresh()


def on_resize(width, height):
    environment.resize()


def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.UP:
        environment.up()
        print('The "UP" key was pressed.')
    elif symbol == pyglet.window.key.DOWN:
        environment.down()
        print('The DOWN arrow key was pressed.')
    elif symbol == pyglet.window.key.LEFT:
        environment.left()
        print('The LEFT key was pressed.')
    elif symbol == pyglet.window.key.RIGHT:
        environment.right()
        print('The RIGHT key was pressed.')
    elif symbol == pyglet.window.key.SPACE:
        environment.rotate()
        print('The RIGHT key was pressed.')


#window.on_resize = on_resize
window.on_draw = on_draw
window.on_key_press = on_key_press
pyglet.app.run()

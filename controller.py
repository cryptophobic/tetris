from pyglet.gl import *

import shapes
from draw import Draw
from scene import Scene


# print(range(33))
#
# exit()

window = pyglet.window.Window(resizable=True)
scene = Scene(10, 25)


def on_draw():
    draw = Draw(window, scene)
    shape = shapes.move_top(shapes.shape_triple, 3)
    for move in range(4):
        shape = shapes.move_right(shapes.rotate(shape), 4)
        draw.draw_polygon(shape)


def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.UP:
        print('The "UP" key was pressed.')
    elif symbol == pyglet.window.key.DOWN:
        print('The DOWN arrow key was pressed.')
    elif symbol == pyglet.window.key.LEFT:
        print('The LEFT key was pressed.')
    elif symbol == pyglet.window.key.RIGHT:
        print('The RIGHT key was pressed.')


window.on_draw = on_draw
window.on_key_press = on_key_press
pyglet.app.run()

from pyglet.gl import *
import sys

from environment.controller import Controller

window = pyglet.window.Window(resizable=True)
environment = Controller(window)

label = pyglet.text.Label('',
                          font_name='Arial',
                          font_size=20,
                          x=20, y=window.height - 40,
                          anchor_x='left')


def on_draw():
    batch = pyglet.graphics.Batch()
    score = environment.refresh(batch)
    label.text = str(score)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    batch.draw()
    label.draw()


#def on_resize(width, height):
#    environment.resize()


def on_key_press(symbol, modifiers):
    environment.control(symbol)

timeout = 0.5
if len(sys.argv) > 0 and 0 < float(sys.argv[1]) < 1:
    timeout = float(sys.argv[1])


pyglet.clock.schedule_interval(environment.tick, timeout)
#window.on_resize = on_resize
window.on_draw = on_draw
window.on_key_press = on_key_press
pyglet.app.run()

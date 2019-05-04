from pyglet.gl import *

from environment.controller import Controller

window = pyglet.window.Window(resizable=True)
environment = Controller(window)


def on_draw():
    batch = pyglet.graphics.Batch()
    environment.refresh(batch)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    batch.draw()


#def on_resize(width, height):
#    environment.resize()


def on_key_press(symbol, modifiers):
    environment.control(symbol)


pyglet.clock.schedule_interval(environment.tick, 0.5)
#window.on_resize = on_resize
window.on_draw = on_draw
window.on_key_press = on_key_press
pyglet.app.run()

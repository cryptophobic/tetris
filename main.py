from controller.bucket_controller import BucketController
from scene import Scene
from settings import Settings
from pyglet.gl import *

window = pyglet.window.Window(resizable=True)
environment = BucketController(window, Scene(10, 20, Scene.CENTER))
level_label = pyglet.text.Label('', font_name='Arial', font_size=20, x=20, y=window.height - 40, anchor_x='left')
lines_label = pyglet.text.Label('', font_name='Arial', font_size=20, x=20, y=window.height - 70, anchor_x='left')
score_label = pyglet.text.Label('', font_name='Arial', font_size=20, x=20, y=window.height - 100, anchor_x='left')
settings = Settings()


def on_draw():
    batch = pyglet.graphics.Batch()
    (lines, score) = environment.refresh(batch)
    level_label.y = window.height - 40
    lines_label.y = window.height - 70
    score_label.y = window.height - 100
    level_label.text = "Level: " + str(settings.level)
    lines_label.text = "Lines: " + str(lines)
    score_label.text = "Score: " + str(score)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    batch.draw()
    score_label.draw()
    level_label.draw()
    lines_label.draw()
    if score >= (settings.limit * settings.level):
        settings.level += 1
        settings.timeout *= 2/3

        print(settings.timeout)
        pyglet.clock.unschedule(environment.tick)
        pyglet.clock.schedule_interval(environment.tick, settings.timeout)


# def on_resize(width, height):
#    environment.resize()


def on_key_press(symbol, modifiers):
    environment.control(symbol)


pyglet.clock.schedule_interval(environment.tick, settings.timeout)
# window.on_resize = on_resize
window.on_draw = on_draw
window.on_key_press = on_key_press
pyglet.app.run()

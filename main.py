from controller.bucket_controller import BucketController
from exceptions import exception
from scene import Scene
from settings import Settings
from pyglet.gl import *

window = pyglet.window.Window(resizable=True)
environment = BucketController(window, Scene(10, 20, Scene.CENTER))
level_label = pyglet.text.Label('', font_name='Arial', font_size=15, x=20, y=window.height - 40, anchor_x='left')
lines_label = pyglet.text.Label('', font_name='Arial', font_size=15, x=20, y=window.height - 70, anchor_x='left')
score_label = pyglet.text.Label('', font_name='Arial', font_size=15, x=20, y=window.height - 100, anchor_x='left')
one_label = pyglet.text.Label('', font_name='Arial', font_size=15, x=20, y=window.height - 130, anchor_x='left')
twix_label = pyglet.text.Label('', font_name='Arial', font_size=15, x=20, y=window.height - 160, anchor_x='left')
triple_label = pyglet.text.Label('', font_name='Arial', font_size=15, x=20, y=window.height - 190, anchor_x='left')
tetris_label = pyglet.text.Label('', font_name='Arial', font_size=15, x=20, y=window.height - 220, anchor_x='left')
settings = Settings()


def on_draw():
    batch = pyglet.graphics.Batch()
    (lines, score, one, twix, triple, tetris) = environment.get_stats()
    environment.refresh(batch)
    level_label.y = window.height - 40
    lines_label.y = window.height - 70
    score_label.y = window.height - 100
    one_label.y = window.height - 130
    twix_label.y = window.height - 160
    triple_label.y = window.height - 190
    tetris_label.y = window.height - 220

    level_label.text = "Level: " + str(settings.level)
    lines_label.text = "Lines: " + str(lines)
    score_label.text = "Score: " + str(score)
    one_label.text = "One: " + str(one)
    twix_label.text = "Twix: " + str(twix)
    triple_label.text = "Triple: " + str(triple)
    tetris_label.text = "Tetris: " + str(tetris)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    batch.draw()
    score_label.draw()
    level_label.draw()
    lines_label.draw()
    one_label.draw()
    twix_label.draw()
    triple_label.draw()
    tetris_label.draw()

    if environment.game_over:
        pyglet.clock.unschedule(environment.tick)
        game_over = pyglet.text.Label('Game Over! Press Enter', font_name='Arial', font_size=20,
                                      x=window.width // 2 - 150, y=window.height // 2,
                                      anchor_x='left')

        environment.clear()
        game_over.draw()

    if lines >= (settings.limit * settings.level):
        settings.level += 1
        settings.timeout *= 4 / 5

        #print(settings.timeout)
        pyglet.clock.unschedule(environment.tick)
        pyglet.clock.schedule_interval(environment.tick, settings.timeout)


# def on_resize(width, height):
#    environment.resize()


def on_key_press(symbol, modifiers):
    if environment.game_over and symbol == pyglet.window.key.ENTER:
        (lines, score, one, twix, triple, tetris) = environment.get_stats()
        print("lines:" + str(lines) + " score:" + str(score) + " one:" + str(one) + " twix:" + str(
            twix) + " triple:" + str(twix) + " tetris:" + str(tetris))
        settings.re_init()
        environment.re_init()
        pyglet.clock.schedule_interval(environment.tick, settings.timeout)

    environment.control(symbol)


pyglet.clock.schedule_interval(environment.tick, settings.timeout)
# window.on_resize = on_resize
window.on_draw = on_draw
window.on_key_press = on_key_press
pyglet.app.run()

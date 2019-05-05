import drawing.display as display
from drawing.scale import Scale
from drawing.item import Item
from typing import List
import pyglet


class Draw:

    SHAPE = pyglet.gl.GL_POLYGON

    DOTS = pyglet.gl.GL_POINTS

    SQUARE = pyglet.gl.GL_QUADS

    LINE = pyglet.gl.GL_LINES

    def __init__(self, scale: Scale):
        self._scale_object = scale

    def draw_shape(self, shape: List, batch):
        scaled = self._scale_object.scale_shape(shape)
        for primitive in scaled:
            item = Item(primitive, self.SQUARE)
            display.add(item, batch)

    def draw_lines(self, shape: List, batch):
        scaled = self._scale_object.scale_line(shape)
        item = Item(scaled, self.LINE)
        display.add(item, batch)

    def draw_dots(self, dots: List, batch):
        scaled = self._scale_object.scale_dots(dots)
        item = Item(scaled, self.DOTS)
        display.add(item, batch)

    def draw_list(self, list_items: List, batch):
        for item in list_items:
            if item['type'] == Draw.DOTS:
                self.draw_dots(item['shape'], batch)
            elif item['type'] == Draw.LINE:
                self.draw_lines(item['shape'], batch)
            else:
                self.draw_shape(item['shape'], batch)



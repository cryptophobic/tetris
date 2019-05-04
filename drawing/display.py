from pyglet.gl import *
from drawing.item import Item
from exceptions import exception


def add(item: Item, batch_object: pyglet.graphics.Batch):
    if not isinstance(item, Item):
        raise exception.IncorrectTypeError('item must be drawing.item.Item instance')
    return batch_object.add(len(item.vertices[1]) // 2, item.type, None, item.vertices)


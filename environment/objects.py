import shapes
import random

from environment.action import Action
from exceptions import exception
from scene import Scene
from environment.trash import Trash
from typing import List, Dict, Set
from drawing.draw import Draw


class Objects:
    def __init__(self, scene: Scene):
        self._current_object_id = -1
        self._objects = []  # type: List[Dict[str, List or int]]
        self._scene = scene
        self._trash = Trash(self._scene)

    def new_shape(self):
        shape_number = random.randint(0, len(shapes.shapes) - 1)
        shape = shapes.shapes[shape_number]
        shape_height = shapes.shape_height(shape)

        shape = shapes.move_top(shapes.move_right(shapes.shapes[shape_number], 3),
                                self._scene.height - shape_height - 1)
        return self.register_shape(shape)

    def _get_object(self, object_id: int):
        object_id = object_id if object_id > 0 else self._current_object_id

        if object_id < 0 or object_id >= len(self._objects):
            return False

        return self._objects[object_id]

    def _obtain_object(self, object_id: int):
        if not self._get_object(object_id):
            self._current_object_id = object_id = self.new_shape()

        object_id = object_id if object_id > 0 else self._current_object_id
        return object_id

    def _store_object(self, shape: List, gl_type: int, index: int):
        if index >= len(self._objects):
            raise exception.UndefinedIndexError("index %d: is out of range" % index)
        if index < 0:
            self._objects.append({'shape': shape, 'type': gl_type})
            index = len(self._objects) - 1
        else:
            self._objects[index] = {'shape': shape, 'type': gl_type}

        return index

    def _check_if_fits(self, coordinates: List, strict: bool):
        shape_candidate = []  # type: List

        for item in coordinates:
            if self._trash.is_set(item):
                continue

            if 0 <= item[0] < self._scene.width and 0 < item[1] <= self._scene.height:
                shape_candidate.append(item)

        if strict and len(shape_candidate) < len(coordinates):
            raise exception.OutOfRangeError("shape doesn't fit scene")

        return shape_candidate

    def register_object(self, object_candidate: List, gl_type: int, index: int, strict=False):
        try:
            if strict:
                object_candidate = self._check_if_fits(object_candidate, strict)
            index = self._store_object(object_candidate, gl_type, index)
        except exception.OutOfRangeError as e:
            return -1

        return index

    def register_dots(self, object_candidate: List, index=-1):
        return self.register_object(object_candidate, Draw.DOTS, index)

    def register_lines(self, object_candidate: List, index=-1):
        return self.register_object(object_candidate, Draw.LINE, index, False)

    def register_shape(self, object_candidate: List, index=-1):
        return self.register_object(object_candidate, Draw.SQUARE, index, True)

    def perform_action(self, action: Action, object_id=-1):

        if action.action == Action.DOWN:
            self.move_down(object_id, True)
            return

        object_id = self._obtain_object(object_id)
        current_object = self._objects[object_id]
        object_candidate = current_object
        if action.action == Action.UP:
            object_candidate = shapes.move_top(current_object['shape'], 1)
        if action.action == Action.LEFT:
            object_candidate = shapes.move_left(current_object['shape'], 1)
        if action.action == Action.RIGHT:
            object_candidate = shapes.move_right(current_object['shape'], 1)
        if action.action == Action.FIRE:
            object_candidate = shapes.rotate(current_object['shape'])

        self.register_shape(object_candidate, object_id)

    def move_down(self, object_id=-1, fall=False):
        object_id = self._obtain_object(object_id)
        object_candidate = self._objects[object_id]['shape']
        result = None
        while result != -1 and (fall or result is None):
            object_candidate = shapes.move_bottom(object_candidate, 1)
            result = self.register_shape(object_candidate, object_id)

        if result < 0:
            if object_id == self._current_object_id:
                self._current_object_id = -1

            self._trash.put(self._objects[object_id]['shape'])
            del self._objects[object_id]

    def move_left(self, object_id=-1):
        self.perform_action(Action.LEFT, object_id)

    def move_right(self, object_id=-1):
        self.perform_action(Action.RIGHT, object_id)

    def move_up(self, object_id=-1):
        self.perform_action(Action.UP, object_id)

    def rotate(self, object_id=-1):
        self.perform_action(Action.FIRE, object_id)

    def get_array(self):
        result = []
        trash = self._trash.get_array()
        if len(trash) > 0:
            result = trash

        return result + self._objects

    def get_score(self):
        return self._trash.get_score()


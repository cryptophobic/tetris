from typing import List, Dict, Set

from drawing.draw import Draw
from scene import Scene


class Trash:

    def __init__(self, scene: Scene):
        self._score = 0
        self._scene = scene
        self._state = []  # type: List[Set[int]]

    def put(self, shape: List):
        for item in shape:
            diff = item[1] - len(self._state) + 1
            if diff > 0:
                self._state += [set() for i in range(diff)]

            self._state[item[1]].add(item[0])

        self._check_solid_lines()

    def get_array(self):
        result = []

        for y in range(len(self._state)):
            for x in self._state[y]:
                result.append({'type': Draw.SQUARE, 'shape': [[x, y]]})

        return result

    def get_score(self):
        return self._score

    def is_set(self, point: List):
        if point[1] < len(self._state) and point[0] in self._state[point[1]]:
            return True

        return False

    def _check_solid_lines(self):

        indices_to_del = []

        for y in range(len(self._state)):
            if len(self._state[y]) == self._scene.width:
                indices_to_del.append(y)

        self._score += 1*len(indices_to_del)
        denom = 0
        for index in indices_to_del:
            del self._state[index - denom]
            denom += 1


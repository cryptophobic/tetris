from typing import List, Dict, Set

from drawing.draw import Draw
from scene import Scene


class Trash:

    def __init__(self, scene: Scene):
        self._score = self._lines = self._one = self._twix = self._triple = self._tetris = 0
        self._scene = scene
        self._state = []  # type: List[Set[int]]

    def put(self, shape: List):
        for item in shape:
            diff = item[1] - len(self._state) + 1
            if diff > 0:
                self._state += [set() for i in range(diff)]

            self._state[item[1]].add(item[0])

        self._check_solid_lines()

    def clear(self):
        self._state = []

    def get_array(self):
        result = []

        for y in range(len(self._state)):
            for x in self._state[y]:
                result.append({'type': Draw.SQUARE, 'shape': [[x, y]]})

        return result

    def get_score(self):
        return self._score

    def get_lines(self):
        return self._lines

    def get_one(self):
        return self._one

    def get_twix(self):
        return self._twix

    def get_triple(self):
        return self._triple

    def get_tetris(self):
        return self._tetris

    def is_set(self, point: List):
        if point[1] < len(self._state) and point[0] in self._state[point[1]]:
            return True

        return False

    def _check_solid_lines(self):

        indices_to_del = []

        for y in range(len(self._state)):
            if len(self._state[y]) == self._scene.width:
                indices_to_del.append(y)

        if len(indices_to_del) > 0:
            self._score += ((2*len(indices_to_del))-1) * (self._lines // 20 + 1)
            self._lines += len(indices_to_del)
            if len(indices_to_del) == 4:
                self._tetris += 1
            if len(indices_to_del) == 3:
                self._triple += 1
            if len(indices_to_del) == 2:
                self._twix += 1
            if len(indices_to_del) == 1:
                self._one += 1

        denom = 0
        for index in indices_to_del:
            del self._state[index - denom]
            denom += 1


import sys


class Settings:

    def __init__(self):
        self.timeout = 1
        self.level = 1
        self.limit = 20
        self.score = self.lines = self.one = self.twix = self.triple = self.tetris = 0
        self.game_over = False
        if len(sys.argv) > 1 > float(sys.argv[1]) > 0:
            self.timeout = float(sys.argv[1])

    def re_init(self):
        self.__init__()

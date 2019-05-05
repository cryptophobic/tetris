import sys


class Settings:

    def __init__(self):
        self.timeout = 1
        self.level = 1
        self.limit = 20
        if len(sys.argv) > 1 > float(sys.argv[1]) > 0:
            self.timeout = float(sys.argv[1])

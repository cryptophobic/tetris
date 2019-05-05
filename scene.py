class Scene:

    CENTER = 1

    LEFT = 2

    RIGHT = 4

    TOP = 8

    BOTTOM = 16

    def __init__(self, width: int, height: int, x_position=CENTER, y_position=BOTTOM):
        self.width = width
        self.height = height
        self.x_position = x_position
        self.y_position = y_position

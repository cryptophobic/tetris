_rotation_matrix = [[0, 1], [-1, 0]]

shapes = [
    [[0, 0], [0, 1], [-1, 1], [-1, -1], [2, -1], [2, 0]],  # ge
    [[0, 0], [0, -1], [-1, -1], [-1, 1], [2, 1], [2, 0]],  # reverted ge
    [[0, 0], [-1, 0], [-1, -1], [2, -1], [2, 0], [1, 0], [1, 1], [0, 1]],  # triple
    [[1, 1], [-1, 1], [-1, -1], [1, -1]],  # square
    [[0, 0], [0, -1], [1, -1], [1, 1], [0, 1], [0, 2], [-1, 2], [-1, 0]],  # twice
    [[0, 0], [0, -1], [-1, -1], [-1, 1], [0, 1], [0, 2], [1, 2], [1, 0]],  # twice reverted
    [[0, 0], [-2, 0], [-2, 1], [2, 1], [2, 0]],  # stick
]


# https://www.math10.com/ru/vysshaya-matematika/matrix/umnozhenie-matric.html
def rotate(shape_array):
    row_count = len(_rotation_matrix)
    column_count = len(shape_array)
    x_denominator = shape_array[0][0]
    y_denominator = shape_array[0][1]
    denominated_shape = [[pair[0] - x_denominator, pair[1] - y_denominator] for pair in shape_array]

    result = [[0 for i in range(row_count)] for i in range(column_count)]

    for i in range(len(_rotation_matrix)):
        for j in range(len(shape_array[0])):
            for k in range(len(shape_array)):
                result[k][j] += _rotation_matrix[i][j] * denominated_shape[k][i]

    return [[pair[0] + x_denominator, pair[1] + y_denominator] for pair in result]


def shape_height(shape_array):
    height = 0
    for item in shape_array:
        if item[1] > height:
            height = item[1]

    return height


def _move(shape_array, times_x, times_y):
    return [[pair[0] + times_x, pair[1] + times_y] for pair in shape_array]


def move_left(shape_array, times=1):
    return _move(shape_array, -times, 0)


def move_right(shape_array, times=1):
    return _move(shape_array, times, 0)


def move_top(shape_array, times=1):
    return _move(shape_array, 0, times)


def move_bottom(shape_array, times=1):
    return _move(shape_array, 0, -times)

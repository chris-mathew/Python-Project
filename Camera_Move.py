import math


def magnitude_forward(look_x, look_y, look_z):
    direction_forward = [0, 0, 0]
    magnitude = math.sqrt(math.pow(look_x, 2) + math.pow(look_x, 2) + math.pow(look_z, 2))
    direction_forward[0] = look_x / magnitude
    direction_forward[1] = look_y / magnitude
    direction_forward[2] = look_z / magnitude
    return direction_forward


def cross(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

    return c
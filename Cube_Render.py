from OpenGL.GL import *
import numpy as np
import copy
import math


cube_size = (
    (0.5, -0.5, -0.5),
    (0.5, 0.5, -0.5),
    (-0.5, 0.5, -0.5),
    (-0.5, -0.5, -0.5),
    (0.5, -0.5, 0.5),
    (0.5, 0.5, 0.5),
    (-0.5, -0.5, 0.5),
    (-0.5, 0.5, 0.5)
)

# verticies = [
#    [0.5, -0.5, -0.5],
#    [0.5, 0.5, -0.5],
#    [-0.5, 0.5, -0.5],
#    [-0.5, -0.5, -0.5],
#    [0.5, -0.5, 0.5],
#    [0.5, 0.5, 0.5],
#    [-0.5, -0.5, 0.5],
#    [-0.5, 0.5, 0.5]
# ]

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

surface = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)


# def cube(x, y, z):
#    for ver in range(8):
#        verticies[ver][0] = cube_size[ver][0] + x
#    for ver in range(8):
#        verticies[ver][1] = cube_size[ver][1] + y
#    for ver in range(8):
#        verticies[ver][2] = cube_size[ver][2] + z
#
#    glBegin(GL_QUADS)
#    for surfaces in surface:
#        glColor4fv((145, 250, 130, 255))
#        for vertex in surfaces:
#            glVertex3fv(verticies[vertex])
#    glEnd()


def outline(vert, corners):
    glBegin(GL_LINES)
    for edge in corners:
        glColor3fv((255, 255, 255))
        for vertex in edge:
            glVertex3fv(vert[vertex])

    glEnd()


def outline_curve(pos, rad_angle):
    glBegin(GL_LINES)
    angles = int(math.pi*4 - rad_angle[1])
    for angle in np.arange(0, angles, 0.01):
        x = pos[0] + (rad_angle[0]*math.cos(angle))
        y = pos[1] + (rad_angle[0]*math.sin(angle))
        z = pos[2]
        glVertex3f(x, y, z)

    glEnd()


def input_arc():
    a = input("\nInput first point (x,y)")
    b = input("\nInput second point (x,y)")
    r = float(input("\nInput radius"))
    c = [float(b[0])-float(a[0]), float(b[2])-float(a[2]), 0]
    c_mag = math.sqrt((c[0]*c[0]) + (c[1]*c[1]))
    angle = math.acos(((2*r*r) - (c_mag*c_mag))/(2*r*r))
    y_coff = c[0]/(-c[1])
    height = math.cos(angle/2)*r
    x = (((y_coff*y_coff)+1)/(height*height)) + (c[0]/2) + float(a[0])
    y = (((y_coff * y_coff) + 1)*y_coff/ (height * height)) + (c[1]/2) + float(a[2])
    print(math.sqrt(math.pow(x-float(a[0]), 2)+math.pow(y-float(a[2]), 2)))
    print("\n")
    print(math.sqrt(math.pow(x - float(b[0]), 2) + math.pow(y - float(b[2]), 2)))
    return [x, y, r, angle]


def input_vertex():
    vert = []
    terminate = False
    while not terminate:
        vertex = input("Input x,y: ")
        if vertex != 'None':
            vert.append([float(vertex[0]), float(vertex[2]), 0])
        else:
            break
    return vert


def remove_vertex(vert_matrix):
    terminate = False
    for vert_mat in range(len(vert_matrix)):
        print(str(vert_mat) + " " + str(vert_matrix[vert_mat]) + "\n")
    while not terminate:
        delete = input("No. of the Point you want to Delete \n")
        if delete != 'None':
            del vert_matrix[delete]
        else:
            break
    return vert_matrix


def corner(vert_matrix):
    corner_matrix = []
    terminate = False
    for vert_mat in range(len(vert_matrix)):
        print(str(vert_mat) + " " + str(vert_matrix[vert_mat]) + "\n")
    while not terminate:
        corners = input("Input corner in the format point1,point2: ")
        if corners != "None":
            corner_matrix.append([int(corners[0]), int(corners[2])])
        else:
            break
    return corner_matrix


def select(all_list):
    for vert_mat in range(len(all_list)):
        print(str(vert_mat) + " " + str(all_list[vert_mat]) + "\n")
    selected = int(input("Select the No. : "))
    return all_list[selected]


def extrude_cad(coord, dis):
    extruded = copy.deepcopy(coord)
    length = len(coord[0])
    for original in range(len(coord[0])):
        extruded[0][original][2] = dis
        coord[0].append(extruded[0][original])

    for original_cor in range(len(coord[1])):
        extruded[1][original_cor][0] = coord[1][original_cor][0] + length
        extruded[1][original_cor][1] = coord[1][original_cor][1] + length
        coord[1].append(extruded[1][original_cor])
        coord[1].append([original_cor, original_cor+length])
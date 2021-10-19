from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import keyboard
import Camera_Move as cam_move
import math
import Cube_Render as cube


if not glfw.init():
    print("GLFW was not initialized")
window = glfw.create_window(600, 600, "Game", None, None)

glfw.make_context_current(window)
# Initial Constants
look_y = 0
pitch = 0
look_x = 0
yaw = math.pi
look_z = -1
distance = 2
cam_x = 0
cam_y = 0
cam_z = 1
speed = 0.01
rotate_speed = 0.025
View_Cam = 'Focus'
lookat_x = 0.5
lookat_y = 0
lookat_z = 0.5
objects = []
selected = []
time = 0
extrudable = False
cam_z_draw = 3


glMatrixMode(GL_MODELVIEW)
while not glfw.window_should_close(window):
    while glfw.get_time() > time:
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)

        if keyboard.is_pressed('TAB'):
            View_Cam = input("\nWhich view would you like? 'Free' 'Focus' 'Drawing': ")

        if View_Cam == 'Drawing':
            if keyboard.is_pressed('+') and cam_z_draw > 0:
                cam_z_draw -= 0.01
            if keyboard.is_pressed('-'):
                cam_z_draw += 0.01

            gluPerspective(90, 1, 0.1, 200)
            gluLookAt(0, 0, cam_z_draw, 0, 0, 0, 0, 1, 0)
            for objective in objects:
                cube.outline(objective[0], objective[1])



        else:
            if View_Cam == 'Free':
                if keyboard.is_pressed('W'):
                    direction_forward = cam_move.magnitude_forward(look_x, look_y, look_z)
                    cam_x += speed * direction_forward[0]
                    cam_y += speed * direction_forward[1]
                    cam_z += speed * direction_forward[2]
                if keyboard.is_pressed('S'):
                    direction_forward = cam_move.magnitude_forward(look_x, look_y, look_z)
                    cam_x -= speed * direction_forward[0]
                    cam_y -= speed * direction_forward[1]
                    cam_z -= speed * direction_forward[2]
                if keyboard.is_pressed('D'):
                    direction_forward = cam_move.magnitude_forward(look_x, look_y, look_z)
                    direction_forward = cam_move.cross(direction_forward, [0, 1, 0])
                    cam_x += speed * direction_forward[0]
                    cam_y += speed * direction_forward[1]
                    cam_z += speed * direction_forward[2]
                if keyboard.is_pressed('A'):
                    direction_forward = cam_move.magnitude_forward(look_x, look_y, look_z)
                    direction_forward = cam_move.cross(direction_forward, [0, 1, 0])
                    cam_x -= speed * direction_forward[0]
                    cam_y -= speed * direction_forward[1]
                    cam_z -= speed * direction_forward[2]

                if keyboard.is_pressed('up'):
                    pitch += rotate_speed
                    if pitch >= math.pi / 2:
                        pitch = math.pi / 2
                    look_y = math.sin(pitch)

                if keyboard.is_pressed('down'):
                    pitch -= rotate_speed
                    if pitch <= -math.pi / 2:
                        pitch = -math.pi / 2
                    look_y = math.sin(pitch)

                if keyboard.is_pressed('left'):
                    yaw += rotate_speed
                    look_z = math.cos(yaw)
                    look_x = math.sin(yaw)
                if keyboard.is_pressed('right'):
                    yaw -= rotate_speed
                    look_z = math.cos(yaw)
                    look_x = math.sin(yaw)
                lookat_x = distance * look_x + cam_x
                lookat_y = distance * look_y + cam_y
                lookat_z = distance * look_z + cam_z
            elif View_Cam == 'Focus':
                if keyboard.is_pressed('+') and distance > 0:
                    distance -= 0.001
                    cam_y = math.sin(pitch) * distance
                    cam_z = math.sin(yaw) * distance
                    cam_x = math.cos(yaw) * distance
                if keyboard.is_pressed('-'):
                    distance += 0.001
                    cam_y = math.sin(pitch) * distance
                    cam_z = math.sin(yaw) * distance
                    cam_x = math.cos(yaw) * distance
                if keyboard.is_pressed('left'):
                    yaw += rotate_speed
                    cam_x = math.cos(yaw) * distance
                    cam_z = math.sin(yaw) * distance
                if keyboard.is_pressed('right'):
                    yaw -= rotate_speed
                    cam_z = math.sin(yaw) * distance
                    cam_x = math.cos(yaw) * distance
                if keyboard.is_pressed('up'):
                    pitch += rotate_speed
                    if pitch >= math.pi / 2:
                        pitch = math.pi / 2
                    cam_y = math.sin(pitch) * distance

                if keyboard.is_pressed('down'):
                    pitch -= rotate_speed
                    if pitch <= -math.pi / 2:
                        pitch = -math.pi / 2
                    cam_y = math.sin(pitch) * distance

                lookat_x = 0
                lookat_y = 0
                lookat_z = 0

            gluPerspective(90, 1, 0.1, 200)
            gluLookAt(cam_x, cam_y, cam_z, lookat_x, lookat_y, lookat_z, 0, 1, 0)

            if keyboard.is_pressed('P'):
                vert = cube.input_vertex()
                corner = cube.corner(vert)
                objects.append([vert, corner, "Line"])

            if keyboard.is_pressed('O'):
                selected = cube.select(objects)
                extrudable = True

            if keyboard.is_pressed('J'):
                arc = cube.input_arc()
                objects.append([[arc[0], arc[1], 0], [arc[2], arc[3]], "Curve"])

            if keyboard.is_pressed('L') and extrudable:
                cube.extrude_cad(selected, 3)
                extrudable = False

            for objective in objects:
                if objective[2] == "Line":
                    cube.outline(objective[0], objective[1])
                elif objective[2] == "Curve":
                    cube.outline_curve(objective[0], objective[1])

        glfw.poll_events()
        glfw.swap_buffers(window)
        time += 0.01666667
    if keyboard.is_pressed('esc'):
        break
glfw.terminate()
import data_structures as ds
import operations as op
import pygame, sys
from random import randint, seed, choice
from pygame.locals import *
import time

#seed(138)

def draw_screen():

    screen.fill(black_color)

    if draw_vertices_points:
        if len(vertice_list) > 0:
            for vertice in vertice_list:
                vertice.draw(screen)
                if draw_coordinates:
                    vertice.draw_pos(screen, font, black_color)

    if draw_boundingbox:
        pygame.draw.rect(screen, red_color, bounding_box, 2)
    
    # First triangle is aways the super
    # Skip it if should not draw
    if len(draw_triangles) > 0:
        for triangle in draw_triangles:
            if triangle == super_triangle and not draw_super_triangle:
                continue
            triangle.draw(triangle_width, screen)

    pygame.display.update()
    
def generate_random_vertices(n_vertices):
    vertice_list = []

    for i in range(n_vertices):
        x = randint(border, screen_w - border)
        y = randint(border, screen_h - border)
        point = ds.vertice(x, y, black_color, vertice_size)
        vertice_list.append(point)

    return vertice_list

def get_bounding_box(vertice_list):

    x_min = 9999
    y_min = 9999
    x_max = 0
    y_max = 0

    for vertice in vertice_list:
        if vertice.x < x_min:
            x_min = vertice.x
        if vertice.x > x_max:
            x_max = vertice.x
        if vertice.y < y_min:
            y_min = vertice.y
        if vertice.y > y_max:
            y_max = vertice.y


    rect = pygame.Rect((x_min, y_min), (x_max - x_min, y_max - y_min))
    return rect

def get_super_triangle(bounding_box, vertice_color):
    padding = 20
    cx = int((bounding_box.right + bounding_box.left)/2)
    cy = int((bounding_box.bottom + bounding_box.top)/2)

    v1 = (cx, int(cy - 1.5 * bounding_box.height - padding))
    v2 = (cx - bounding_box.width - padding, bounding_box.bottom + padding)
    v3 = (cx + bounding_box.width + padding, bounding_box.bottom + padding)

    global vertice_buffer, edge_buffer, vertice_list

    vt1 = ds.vertice(v1[0], v1[1], vertice_color, vertice_size)
    vt2 = ds.vertice(v2[0], v2[1], vertice_color, vertice_size)
    vt3 = ds.vertice(v3[0], v3[1], vertice_color, vertice_size)
    vt1, vt2, vt3 = op.sort_pontos_poly([vt1, vt2, vt3])
    vertice_buffer.append(vt1)
    vertice_buffer.append(vt2)
    vertice_buffer.append(vt3)
    vertice_list.append(vt1)
    vertice_list.append(vt2)
    vertice_list.append(vt3)

    edge1 = ds.edge(vt1, vt2, vertice_color, edge_width)
    edge2 = ds.edge(vt2, vt3, vertice_color, edge_width)
    edge3 = ds.edge(vt3, vt1, vertice_color, edge_width)
    edge_buffer.append(edge1)
    edge_buffer.append(edge2)
    edge_buffer.append(edge3)

    super_triangle = ds.triangle(edge1, edge2, edge3)

    return super_triangle

def get_sorted_triangle(vertices, color, width):
    global edge_buffer

    vt1, vt2, vt3 = op.sort_pontos_poly(vertices)
    edge1 = ds.edge(vt1, vt2, color, width)
    edge2 = ds.edge(vt2, vt3, color, width)
    edge3 = ds.edge(vt3, vt1, color, width)

    edge_buffer.append(edge1)
    edge_buffer.append(edge2)
    edge_buffer.append(edge3)

    return ds.triangle(edge1, edge2, edge3)

def update_screen():
    global vertice_list, vertice_reference, triangle_buffer, removing_phase, end_phase

    vertice_reference -= 1
    if vertice_reference >= 0:
        vertice = vertice_list[vertice_reference]
        buffer = []

        for triangle in triangle_buffer:
            if triangle.in_circumcircle(vertice):
                buffer.append(triangle)

        if len(buffer) > 0:

            new_triangles = []
            for triangle in buffer:
                e1, e2, e3 = triangle.edges
                a1, a2, a3 = (e1.a, e2.a, e3.a)

                vert1 = [vertice, a1, a2]
                vert2 = [vertice, a2, a3]
                vert3 = [vertice, a3, a1]
                
                # Either the color is random
                # or is a value based on the y value of the centroid
                if set_color_random:

                    color1 = op.random_color() 
                    color2 = op.random_color() 
                    color3 = op.random_color() 

                else:
                    
                    y1 = op.calcular_centroide_poly(vert1)[1]
                    y2 = op.calcular_centroide_poly(vert2)[1]
                    y3 = op.calcular_centroide_poly(vert3)[1]
                
                    color1 = op.get_shade(default_color, y1/bounding_box.height)
                    color2 = op.get_shade(default_color, y2/bounding_box.height)
                    color3 = op.get_shade(default_color, y3/bounding_box.height)
 
                tri1 = get_sorted_triangle(vert1, color1, edge_width)
                tri2 = get_sorted_triangle(vert2, color2, edge_width)
                tri3 = get_sorted_triangle(vert3, color3, edge_width)

                new_triangles.append(tri1)
                new_triangles.append(tri2)
                new_triangles.append(tri3)

            for n in new_triangles:
                if n not in triangle_list:
                    triangle_list.append(n)
                    triangle_buffer.append(n)
    
    else:

        init_size = len(triangle_list)

        for triangle in triangle_list:
            if (
                triangle.has_vertice(vertice_list[-1]) or
                triangle.has_vertice(vertice_list[-2]) or
                triangle.has_vertice(vertice_list[-3])
                ):
                triangle_list.remove(triangle)
        final_size = len(triangle_list)

        if init_size == final_size:
            removing_phase = True

    if removing_phase:

        init_size = len(triangle_list)

        for triangle in triangle_list:
            for vertice in vertice_list:
                if triangle.in_circumcircle(vertice):
                    try:
                        triangle_list.remove(triangle)
                    except:
                        continue

        final_size = len(triangle_list)

        if init_size == final_size:
            removing_phase = False
            end_phase = True

    if end_phase:  

        if print_delta_time:
            global i_time
            print("Delta time: " + str(time.time() - i_time))

        list_setup()
        draw_screen()
        i_time = time.time()
        end_phase = False

        global it

        pygame.image.save(screen,"gif/" +  str(it) + "iteration.jpeg")

        it += 1

        

def move_vertices(vertices, sensibility):
    new_vertices = []

    for vertice in vertices:

        # Get new vertex sligthly out of place (random)
        x, y = vertice.xy
        v_x, v_y = (choice([-sensibility, sensibility]), choice([-sensibility, sensibility]))
        new_x, new_y = (x + v_x, y + v_y)

        # Bound new vertex location to screen
        if new_x < 0 or new_x > screen_w:
            new_x -= 2 * v_x
        if new_y < 0 or new_y > screen_h:
            new_y -= 2 * v_y

        new_vertice = ds.vertice(new_x, new_y, vertice.color, vertice_size)
        new_vertices.append(new_vertice)
    
    return new_vertices

def list_setup():

    global edge_buffer, vertice_buffer, triangle_buffer
    global vertice_list, bounding_box, super_triangle
    global triangle_list, draw_triangles
    global vertice_reference, i_time

    edge_buffer = []
    vertice_buffer = []
    triangle_buffer = []

    # Remove vertices of super triangle
    vertice_list = vertice_list[:-3]
    vertice_list = move_vertices(vertice_list, move_speed)
    bounding_box = get_bounding_box(vertice_list)
    super_triangle = get_super_triangle(bounding_box, red_color)

    draw_triangles = triangle_list
    triangle_buffer = [super_triangle]
    triangle_list = [super_triangle]

    vertice_reference = len(vertice_list) - 3

# MAIN
pygame.init()
pygame.display.set_caption("Delaunay Triangulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)

w, h = (600, 600)
screen_decrease_factor = 1
screen_w, screen_h = (int(w/screen_decrease_factor), int(h/screen_decrease_factor))
screen = pygame.display.set_mode((screen_w, screen_h))

white_color = (255, 255, 255)
black_color = (0, 0, 0)
blue_color = (0, 0, 255)
green_color = (100, 255, 0)
gray_color = (125, 125, 125)
red_color = (255, 0, 0)
teal_color = (100, 200, 200)
default_color = blue_color

n_vertices = 20
vertice_size = 3
edge_width = 3
border = 10

# 0 (zero) to fill triangles
triangle_width = 0
move_speed = 6

draw_vertices_points = False
draw_coordinates = False
draw_boundingbox = False
draw_super_triangle = False
removing_phase = False
set_color_random = False
end_phase = False
print_delta_time = True 

edge_buffer = []
vertice_buffer = []
triangle_buffer = []

vertice_list = generate_random_vertices(n_vertices)
bounding_box = get_bounding_box(vertice_list)
super_triangle = get_super_triangle(bounding_box, red_color)

draw_triangles = []
triangle_buffer = [super_triangle]
triangle_list = [super_triangle]

vertice_reference = len(vertice_list) - 3

i_time = time.time()
it = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    update_screen()

    clock.tick(240)
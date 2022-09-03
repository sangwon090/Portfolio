import math
import pygame
from sympy import Symbol, solve, expand

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

stations = [
    [0, 200, 25],
    [-200, 0, 25],
    [100, 0, 38]
]

def ps_to_radius(v_p, v_s, t):
    return (v_p * v_s) / (v_p - v_s) * t

def convert_pos(x, y):
    center_x = SCREEN_WIDTH / 2
    center_y = SCREEN_HEIGHT / 2

    return center_x + x, center_y - y

def calc_epicenter(x, y, v_p, v_s):
    x1 = stations[0][0]
    y1 = stations[0][1]
    t1 = stations[0][2]
    r1 = ps_to_radius(v_p, v_s, t1)

    x2 = stations[1][0]
    y2 = stations[1][1]
    t2 = stations[1][2]
    r2 = ps_to_radius(v_p, v_s, t2)

    x3 = stations[2][0]
    y3 = stations[2][1]
    t3 = stations[2][2]
    r3 = ps_to_radius(v_p, v_s, t3)

    c1 = (x - x1) ** 2 + (y - y1) ** 2 - r1 ** 2
    c2 = (x - x2) ** 2 + (y - y2) ** 2 - r2 ** 2
    c3 = (x - x3) ** 2 + (y - y3) ** 2 - r3 ** 2

    l12 = expand(c1 - c2)
    l23 = expand(c2 - c3)
    l31 = expand(c3 - c1)

    return solve((l12, l23, l31), dict=True)[0]

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
is_alive = True
clock = pygame.time.Clock()

x = Symbol('x')
y = Symbol('y')
epicenter = calc_epicenter(x, y, 8, 4)
e_x, e_y = convert_pos(epicenter[x], epicenter[y])

pygame.display.set_caption(f'진앙의 위치: ({e_x}, {e_y})')

while is_alive:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_alive = False
    
    screen.fill((255, 255, 255))
  
    for station in stations:
        x, y = convert_pos(station[0], station[1])
        radius = ps_to_radius(8, 4, station[2])
        pygame.draw.circle(screen, (0, 0, 255), [x, y], 3)
        pygame.draw.circle(screen, (0, 0, 0), [x, y], radius, 2)

    pygame.draw.circle(screen, (255, 0, 0), [e_x, e_y], 5)
    pygame.display.flip()

pygame.quit()
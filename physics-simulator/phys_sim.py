import json
import math
import pygame

with open('objects.json') as f:
    objs = json.load(f)

pygame.init()
pygame.display.set_caption('물체의 운동 시뮬레이터')
screen = pygame.display.set_mode((1600, 800))
clock = pygame.time.Clock()
is_alive = True
time = 0

def convert_pos(x, y):
    return (x, 800-y)

def handle_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_alive = False

def draw_grid():
    for i in range(1, 33, 1):
        pygame.draw.line(screen, (192, 192, 192), [i * 50, 0], [i * 50, 800])
        pygame.draw.line(screen, (192, 192, 192), [0, i * 50], [1600, i * 50])

def draw_objs():
    for obj in objs:
        delay = obj['delay']
        pos = obj['position']

        if obj['type'] == 'normal':
            vel = obj['velocity']
            acc = obj['acceleration']

            if delay > 0:
                obj['delay'] -= 1
                continue

            pos['x'] += vel['x']
            pos['y'] += vel['y']
            vel['x'] += acc['x']
            vel['y'] += acc['y']

            x, y = convert_pos(pos['x'], pos['y'])
            pygame.draw.circle(screen, (0, 0, 0), [x, y], 10)
        elif obj['type'] == 'circular':
            rad = obj['radius']
            agv = obj['angular_velocity']

            x = pos['x'] + rad * math.cos(agv * time)
            y = pos['y'] + rad * math.sin(agv * time)
            pygame.draw.circle(screen, (0, 0, 0), [x, y], 10)

while is_alive:
    screen.fill((255, 255, 255))
    handle_event()
    draw_grid()
    draw_objs()
    pygame.display.flip()
    clock.tick(30)

    time += 1

pygame.quit()
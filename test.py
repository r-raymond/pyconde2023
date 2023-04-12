import pygame
import random
from python import Vec, Sphere, Line
import time
import statistics

pygame.init()
window = pygame.display.set_mode((800, 600))

run = True
window.fill(0)

times = []


def color(x, y):
    start = time.time_ns()

    screen_point = Vec(8.0 * x / 800, 6.0 * y / 600, 0.0)
    screen_dir = Vec(0.0, 0.0, 1.0)
    sphere = Vec(4.0, 3.0, 10.0)
    radius = 2.0
    light = Vec(8.0, 0.0, 7.0)

    line = Line(screen_point, screen_dir)
    sphere = Sphere(sphere, radius)

    intersect = sphere.intersect(line)

    if intersect is None:
        return (100, 100, 100)

    normal = sphere.get_normal(intersect)
    light_ray = (light - intersect).normal()

    result = (max(int(normal * light_ray * 255), 30), 0, 0)
    end = time.time_ns()
    times.append(end - start)

    return result


start = 0
j = 0

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for i in range(start, min(800 * 600, start + 200)):
        x = i % 800
        y = i // 800
        window.set_at((x, y), color(x, y))

    start += 200

    if j % 1000 == 0:
        pygame.image.save(pygame.display.get_surface(), f"{j}.png")
    j += 1
    pygame.display.flip()

pygame.quit()

print(len(times))
print(statistics.mean(times))
print(statistics.stdev(times))

exit()

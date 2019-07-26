import os
from body import *
import body
from body_data import sun_mass, mass_scale
import body_data as info
import pygame
from timeit import default_timer as timer
from datetime import timedelta
from math import radians, cos, sin


run_again = True

clear_trail = True
name_tags = True

screen_width, screen_height = 1920, 1080
window_width, window_height = 1000, 1000

os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % ((screen_width - window_width) // 2, (screen_height - window_height) // 2)

pygame.init()
size = (window_width, window_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Solar System Simulator")

clock = pygame.time.Clock()


def get_initial_zoom(bodies):
    d = 0
    for body in bodies:
        d = max(body.y, body.x, d)

    # print("D:", d, "/", max(size))
    return max(size) / (d * 2)


def get_translation(zoom, center):
    return size[0] // 2 - (center[0] * zoom), size[1] // 2 - (center[1] * zoom)


def generate_planet(name, sun, bodies, angle=90.0):
    rat = 400 * info.get_distance_ratio(name)
    return Body(sun.x + rat * cos(radians(angle)),
                sun.y + rat * sin(radians(angle)),
                bodies, info.get_mass_ratio(name) * sun.mass,
                info.get_radius_ratio(name) * info.get_info(info.earth, info.diameter) * mass_scale,
                info.colors[name], -2.5795003538340437, radians(angle + 90), name)


def get_nearest_body(point, bodies):
    least_dist = size[0] * 2
    closest_bod = (-size[0], -size[1])
    for body in reversed(bodies):
        dist = ((body.scaled_x - point[0]) ** 2 + (body.scaled_y - point[1]) ** 2) ** 0.5
        if dist < least_dist:
            least_dist = dist
            closest_bod = body
    return least_dist, closest_bod


def lock_center_zoom(mouse_pos, bodies):
    least_dist, closest_bod = get_nearest_body(mouse_pos, bodies)
    if least_dist < 25:
        mouse_pos = (closest_bod.x, closest_bod.y)

    return mouse_pos


def main():
    running = True
    can_control = True
    paused = False
    draw = True

    bodies = []
    # sun_mass * mass_scale
    sun = Body(size[0] // 2, size[1] // 2, bodies, info.data["sun"][0] * 1e-4,
               info.get_radius_ratio("sun") * info.get_info(info.earth, info.diameter) * mass_scale,
               (255, 255, 0), 0, 0, "sun")
    bodies.append(sun)

    for i, planet in enumerate(info.planets):
        bodies.append(generate_planet(planet, sun, bodies, 45 * i))

    bodies = bodies[0:3]

    center_zoom = (sun.x, sun.y)
    zoom = get_initial_zoom(bodies)
    translation = get_translation(zoom, center_zoom)

    print("Zoom:", zoom)

    last_time = timer()
    frames = 0

    while running:
        frames += 1
        current_time = timer()
        td = timedelta(seconds=current_time - last_time)
        if td.seconds > .1:
            pygame.display.set_caption("Solar System Simulator - " + str(round(frames / td.seconds)) + "fps")
            frames = 0
            last_time = current_time

        for event in pygame.event.get():
            pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and can_control:
                key = event.key
                if key == pygame.K_r:
                    return True
                if key == pygame.K_p:
                    paused = not paused
                if key == pygame.K_c:
                    center_zoom = (size[0] // 2, size[1] // 2)
                    zoom = get_initial_zoom(bodies)
                    translation = get_translation(zoom,  center_zoom)
                if key == pygame.K_i and (pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]):
                    draw = not draw
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:  # scroll wheel press
                    center_zoom = (size[0] // 2, size[1] // 2)
                    zoom = get_initial_zoom(bodies)
                    translation = get_translation(zoom,  center_zoom)
                if event.button == 4:
                    center_zoom = lock_center_zoom(pygame.mouse.get_pos(), bodies)
                    zoom *= 1.1
                    translation = get_translation(zoom, center_zoom)
                elif event.button == 5:
                    center_zoom = lock_center_zoom(pygame.mouse.get_pos(), bodies)
                    zoom /= 1.1
                    translation = get_translation(zoom, center_zoom)

        if draw:
            screen.fill((0, 0, 0))

        for body in reversed(bodies):
            if draw:
                body.draw(screen, zoom, translation)
            if not paused:
                body.tick()
        if draw:
            pygame.display.update()
            clock.tick(120)
        else:
            clock.tick(240)


if __name__ == "__main__":
    while run_again:
        run_again = main()


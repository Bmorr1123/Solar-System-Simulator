import math
import body_data
import solsyssim
import pygame
import rounded_rects_pygame as rr


G = 6.673 * (10 ** -11)

#
# print(self.name + ": Velocity: (" + str(self.yv) + ", " + str(self.xv) + ")")


class Body:
    def __init__(self, x, y, bodies, mass=1000, radius=25, color=(255, 255, 0), velocity=0, angle=0, name="null"):
        self.name = name

        self.x = x
        self.y = y

        self.scaled_x = None
        self.scaled_y = None

        self.xv = velocity * math.cos(angle)
        self.yv = velocity * math.sin(angle)
        self.mass = mass
        self.radius = radius
        self.color = color
        self.bodies = bodies

        # print(self.name + ": Angled Velocity: (" + str(velocity) + ", " + str(math.degrees(angle)) + ")")
        # print(self.name + ": Linear Velocity: (" + str(self.yv) + ", " + str(self.xv) + ")")

        self.forces = []
        self.trail = []
        self.trail_length = .75 * math.pi * math.sqrt((solsyssim.size[0] // 2 - self.x) ** 2 + (solsyssim.size[1] // 2 - self.y) ** 2)

    def tick(self):
        xf, yf = 0, 0
        for body in self.bodies:
            if body is not self:
                v = self.force(body)
                # print("F:", v.force, ">", v.angle)
                xf += (math.cos(v.angle) * v.force) * body_data.force_scale
                yf += (math.sin(v.angle) * v.force) * body_data.force_scale

        for vector in self.forces:
            xf += (math.cos(vector.angle) * vector.force) * body_data.force_scale
            yf += (math.sin(vector.angle) * vector.force) * body_data.force_scale
        self.forces.clear()

        self.xv += xf / self.mass
        self.yv += yf / self.mass

        self.x += self.xv
        self.y += self.yv

    def text_objects(self, text, font, rect_color):
        text_surface = font.render(text, True, self.color, rect_color)
        alpha_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
        alpha_surface.fill((255, 255, 255, 0))
        text_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return text_surface, text_surface.get_rect()

    def message_display(self, text, pos, size, screen):
        font = pygame.font.Font('freesansbold.ttf', size)
        rect_color = (255, 255, 255)
        not_rect_color = (0, 0, 0)
        if sum(self.color) // 3 > 255 // 2:
            rect_color = (0, 0, 0)
            not_rect_color = (255, 255, 255)
            pass
        text_surface, text_rect = self.text_objects(text, font, rect_color)
        text_rect.center = pos
        s = 6
        bubble = pygame.Rect(text_rect.topleft[0] - s // 2, text_rect.topleft[1] - s // 2, text_rect.width + s,
                             text_rect.height + s)
        try:
            rr.aa_round_rect(screen, bubble, not_rect_color, 6)
            s = 4
            bubble = pygame.Rect(text_rect.topleft[0] - s // 2, text_rect.topleft[1] - s // 2, text_rect.width + s, text_rect.height + s)
            rr.aa_round_rect(screen, bubble, rect_color, 5)
            screen.blit(text_surface, text_rect)
        except OverflowError:
            pass

    def draw(self, screen, zoom, translation):
        self.trail.insert(0, (int(self.x), int(self.y)))

        self.scaled_x, self.scaled_y = (int(self.x * zoom + translation[0]),  int(self.y * zoom + translation[1]))

        self.trail.clear()
        if len(self.trail) > self.trail_length and solsyssim.clear_trail:
            self.trail.pop(-1)
        for i in reversed(range(round(len(self.trail)))):
            gray = 255
            perc = (1 - (i / len(self.trail)))
            if solsyssim.clear_trail:
                gray = 255 * (perc ** 2)
            pygame.draw.circle(screen, (gray, gray, gray), (round(self.trail[i][0] * zoom + translation[0]), round(self.trail[i][1] * zoom + translation[1])), round(self.radius * .3 * zoom))

        pygame.draw.circle(screen, self.color, (self.scaled_x, self.scaled_y), round(self.radius * zoom))
        if solsyssim.name_tags:
            self.message_display(self.name, (self.scaled_x, self.scaled_y - 20), 10, screen)

    def dist(self, b):
        return math.sqrt(((b.x - self.x)**2) + ((b.y - self.y) ** 2))

    def angle(self, b):
        return math.atan2(b.y - self.y, b.x - self.x)

    def force(self, b):
        return Vector2D((G * b.mass * self.mass) / self.dist(b), self.angle(b))

    def angled_velocity(self, velocity, angle):
        self.xv += math.cos(angle) * velocity
        self.yv += math.sin(angle) * velocity


class Vector2D:
    def __init__(self, force, angle):
        self.force = force
        self.angle = angle

    def __add__(self, other):
        return math.atan2(math.sin(self.angle) * self.force + math.sin(other.angle) * other.force,
                          math.cos(self.angle) * self.force + math.cos(other.angle) * other.force)

    def __sub__(self, other):
        return math.atan2(math.sin(self.angle) * self.force + math.sin(-other.angle) * other.force,
                          math.cos(self.angle) * self.force + math.cos(-other.angle) * other.force)

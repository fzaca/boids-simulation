import pygame as pg
from config import *
from random import randint, uniform

class Boid:
    def __init__(self, start_position, size, radius, vision_range):
        self.size = size
        self.position = pg.math.Vector2(start_position)
        self.speed = pg.math.Vector2(uniform(-1, 1), uniform(-1, 1)).normalize() * MAX_SPEED
        self.radius = radius
        self.vision_range = vision_range

    def draw(self, screen):
        tip = self.position + self.speed.normalize() * self.size * 2
        side1 = self.position + self.speed.normalize().rotate(135) * self.size
        side2 = self.position + self.speed.normalize().rotate(-135) * self.size
        vertices = [tip, side1, side2]

        pg.draw.polygon(screen, BOID_BACKGROUND_COLOR, vertices)
        pg.draw.polygon(screen, BOID_BORDER_COLOR, vertices, 2)

    def update(self, dt):
        self.position += self.speed * dt

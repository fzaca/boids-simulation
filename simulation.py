import pygame as pg
from math import floor
from boid import Boid
from random import randint
from config import *

DT = floor((1/FPS)*10**3)/10**3 # Delta Time Const

class Simulation:
    def __init__(self, screen):
        self.screen = screen

        self.boids = [
            Boid(
                (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)),
                BOID_SIZE, BOID_RADIUS, BOID_VISION_RANGE
            )
            for boid in range(DENSITY)
        ]

    def update(self):
        for boid in self.boids:
            boid.draw(self.screen)
            boid.update(DT)

            total_force = self.calculate_force(boid)

            boid.speed += total_force * DT
            if boid.speed.length() > MAX_SPEED:
                boid.speed.scale_to_length(MAX_SPEED)

            if boid.position.x < TURN_RANGE:
                boid.speed.x += (TURN_RANGE - boid.position.x) / 10
            elif boid.position.x > SCREEN_WIDTH - TURN_RANGE:
                boid.speed.x -= (boid.position.x - (SCREEN_WIDTH - TURN_RANGE)) / 10
            if boid.position.y < TURN_RANGE:
                boid.speed.y += (TURN_RANGE - boid.position.y) / 10
            elif boid.position.y > SCREEN_HEIGHT - TURN_RANGE:
                boid.speed.y -= (boid.position.y - (SCREEN_HEIGHT - TURN_RANGE)) / 10

    def calculate_force(self, target):
        separation_force = pg.math.Vector2(0, 0)
        total_direction = pg.math.Vector2(0, 0)
        total_center = pg.math.Vector2(0, 0)
        neighbors = 0

        for boid in self.boids:
            if target == boid:
                continue

            distance = target.position.distance_to(boid.position)

            if distance < target.radius:
                angle = (boid.position - target.position).angle_to(target.speed)
                if abs(angle) <= target.vision_range / 2:
                    # Separation
                    diff = target.position - boid.position
                    diff.normalize_ip()
                    separation_force += diff / distance
                    # Alignment
                    total_direction += boid.speed
                    # Cohesion
                    total_center += boid.position

                    neighbors += 1

        if neighbors > 0:
            # Alignment
            total_direction /= neighbors
            alignment_direction = total_direction.normalize()
            # Cohesion
            average_center = total_center / neighbors
            cohesion_direction = average_center - target.position
            cohesion_direction.normalize_ip()
        else:
            cohesion_direction = total_center
            alignment_direction = total_direction

        if separation_force.length() > 0:
            separation_force = separation_force.normalize()

        # Sumar las tres fuerzas para obtener la dirección de movimiento
        total_force = separation_force * SEP_COEF + alignment_direction * ALIGN_COEF + cohesion_direction * COH_COEF

        return total_force

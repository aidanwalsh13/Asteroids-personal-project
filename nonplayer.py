import pygame
from circleshape import CircleShape
from constants import *
import random
from player import Player

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, player):
        super().__init__(x, y, radius)
        self.player = player

        self.homing_delay = 1

    def draw(self, screen): # pygame method
        pygame.draw.circle(
            screen, # where
            "white", # colour
            self.position,
            self.radius,
            2 # width
        )

    def split(self):
        self.kill()

        hit_score = 0

        if self.radius >= 3 * ASTEROID_MIN_RADIUS:
            hit_score = 5
        elif self.radius >= 2 * ASTEROID_MIN_RADIUS:
            hit_score = 10
        else:
            hit_score = 15

        if self.radius <= ASTEROID_MIN_RADIUS:
            return hit_score

        new_angle = random.uniform(20, 50)
        v1 = self.velocity.rotate(new_angle)
        v2 = self.velocity.rotate(-new_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        a1 = Asteroid(self.position.x, self.position.y, new_radius, self.player)
        a2 = Asteroid(self.position.x, self.position.y, new_radius, self.player)

        a1.velocity = v1 * 1.2
        a2.velocity = v2 * 1.2

        return hit_score

    def update(self, dt): # we call upon the seperate variable, player.pos for the individual player position
        direction = (self.player.pos - self.position).normalize()
        if self.homing_delay >= 0:
            self.homing_delay -= dt
        # homing block
        if self.radius == ASTEROID_MAX_RADIUS and self.position.distance_to(self.player.pos) <= ASTEROID_HOMING_RANGE:
            if self.homing_delay <= 0:
                self.velocity = self.velocity.lerp(direction * ASTEROID_HOMING_SPEED, 0.01)
        if self.radius == ASTEROID_MAX_RADIUS - ASTEROID_MIN_RADIUS and self.position.distance_to(self.player.pos) <= (ASTEROID_HOMING_RANGE * 0.80):
            if self.homing_delay <= 0:
                self.velocity = self.velocity.lerp(direction * ASTEROID_HOMING_SPEED, 0.02)
        if self.radius == ASTEROID_MIN_RADIUS and self.position.distance_to(self.player.pos) <= (ASTEROID_HOMING_RANGE * 0.60):
            if self.homing_delay <= 0:
                self.velocity = self.velocity.lerp(direction * ASTEROID_HOMING_SPEED, 0.03)
        # LERP = LINEAR INTERPOLATION. the smooth blending of two values. 0.0 -> 1.0 : slow -> fast tracking

        # move asteroid
        self.position += self.velocity * dt

# how to kill asteroids when they leave the screen, BUT NOT ADD TO THE SCORE!

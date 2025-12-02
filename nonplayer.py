import pygame
from circleshape import CircleShape
from constants import *
import random
from player import Player

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, player):
        super().__init__(x, y, radius)
        self.player = player

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
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        new_angle = random.uniform(20, 50)
        v1 = self.velocity.rotate(new_angle)
        v2 = self.velocity.rotate(-new_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        from nonplayer import Asteroid

        a1 = Asteroid(self.position.x, self.position.y, new_radius, self.player)
        a2 = Asteroid(self.position.x, self.position.y, new_radius, self.player)

        a1.velocity = v1 * 1.2
        a2.velocity = v2 * 1.2

    def update(self, dt): # we call upon the seperate variable, player.pos for the individual player position
        direction = (self.player.pos - self.position).normalize()
        if self.radius == ASTEROID_MAX_RADIUS and self.position.distance_to(self.player.pos) <= ASTEROID_HOMING_RANGE:
            self.velocity = self.velocity.lerp(direction * ASTEROID_HOMING_SPEED, 0.01)
        if self.radius == ASTEROID_MAX_RADIUS - ASTEROID_MIN_RADIUS and self.position.distance_to(self.player.pos) <= (ASTEROID_HOMING_RANGE * 0.80):
            self.velocity = self.velocity.lerp(direction * ASTEROID_HOMING_SPEED, 0.02)
        if self.radius == ASTEROID_MIN_RADIUS and self.position.distance_to(self.player.pos) <= (ASTEROID_HOMING_RANGE * 0.60):
            self.velocity = self.velocity.lerp(direction * ASTEROID_HOMING_SPEED, 0.03)
        # LERP = LINEAR INTERPOLATION. the smooth blending of two values. 0.0 -> 1.0 : slow -> fast tracking

        # move asteroid
        self.position += self.velocity * dt

    #self.rect.center = self.position  # if you maintain rect; or set in draw
        #x, y = self.position.x, self.position.y
        #if x < -PADDING or x > SCREEN_WIDTH + PADDING or y < -PADDING or y > SCREEN_HEIGHT + PADDING:
        #    self.kill()
# kill asteroids when they leave the screen, BUT DONT ADD TO THE SCORE!

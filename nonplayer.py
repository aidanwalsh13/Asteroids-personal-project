import pygame
from circleshape import CircleShape
from constants import *
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen): # pygame method
        pygame.draw.circle(
            screen, # where
            "black", # colour
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

        a1 = Asteroid(self.position.x, self.position.y, new_radius)
        a2 = Asteroid(self.position.x, self.position.y, new_radius)

        a1.velocity = v1 * 1.2
        a2.velocity = v2 * 1.2

    def update(self, dt):
        self.position += self.velocity * dt

        #self.rect.center = self.position  # if you maintain rect; or set in draw
        #x, y = self.position.x, self.position.y
        #if x < -PADDING or x > SCREEN_WIDTH + PADDING or y < -PADDING or y > SCREEN_HEIGHT + PADDING:
        #    self.kill()
# kill asteroids when they leave the screen, BUT DONT ADD TO THE SCORE!

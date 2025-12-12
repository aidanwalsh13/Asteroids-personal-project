import pygame
import math
import random
from constants import *
from circleshape import *

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

        self.spawn_x = x
        self.spawn_y = y

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

        dx = self.position.x - self.spawn_x # dx; left/right movement since spawn tracking
        dy = self.position.y - self.spawn_y # dy; up/down

        if math.hypot(dx, dy) >= SHOT_DISTANCE: # equation; hypot(the square root of (dx^2 + dy^2)) The straight line distance taken from 0.0 to dx.dy
            self.kill()

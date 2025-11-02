import pygame # essential graphic, sound, input
import random # for nonplayer properties and spawn
from nonplayer import Asteroid
from constants import * # values for screen size, asteroid size, asteroid kinds
from player import Player

class AsteroidField(pygame.sprite.Sprite):
    edges = [ # 4 possible edges. each a list, containing two elements
        [ # top left corner is x=0 y=0. list[0] = direction of movement. list[1] = lambda calculation for initial position, just outside screen boundary
            pygame.Vector2(1, 0), # left edge, velocity right
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0), # right edge, velocity left
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1), # top edge, velocity down
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1), # bottom edge, velocity up
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self, self.containers) # parent class; pygame.sprite.Sprite
        self.spawn_timer = 0.0 # initialise to track time since last spawn
        self.player = player
        self.asteroids = []

    def spawn(self, radius, position, velocity): # method for creating objects
        asteroid = Asteroid(position.x, position.y, radius, self.player)
        asteroid.velocity = velocity
        self.asteroids.append(asteroid)

    def update(self, dt):
        self.spawn_timer += dt # keeps track of time elapsed
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0 # reset

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges) # where to spawn, random select
            speed = random.randint(40, 100) # random object speed
            velocity = edge[0] * speed # direction vector from random edge * random select speed
            velocity = velocity.rotate(random.randint(-30, 30)) # direction of movement from start, random select
            position = edge[1](random.uniform(0, 1)) # edge lambda function * a random position along that edge = spawn point
            kind = random.randint(1, ASTEROID_KINDS) # kind (or type) of asteroid, random select
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity) # call spawn method on these four properties

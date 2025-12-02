import pygame # essential graphic, sound, input
import random # for nonplayer properties and spawn
from nonplayer import Asteroid
from constants import * # values for screen size, asteroid size, asteroid kinds
from player import Player
from upgrades import Upgrade
import random

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
        self.spawn_timer = 0.0 # initialise to track time since last asteroid spawn
        self.spawn_rate = 2.0
        self.timer = 0.0
        self.player = player
        self.asteroids = []
        self.upgrades = []
        self.upgrade_timer = 0.0
        self.upgrade_rate = random.uniform(30, 60)

    def spawn_asteroid(self, radius, position, velocity): # method for creating objects
        asteroid = Asteroid(position.x, position.y, radius, self.player)
        asteroid.velocity = velocity
        self.asteroids.append(asteroid)

    def spawn_upgrade(self, radius, position, velocity): # method for creating objects
        upgrade = Upgrade(position.x, position.y, radius, self.player)
        upgrade.velocity = velocity
        self.upgrades.append(upgrade)

    def update(self, dt):
        # for spawning a new asteroid at a random edge
        edge = random.choice(self.edges) # where to spawn, random select
        speed = random.randint(40, 100) # random object speed
        velocity = edge[0] * speed # direction vector from random edge * random select speed
        velocity = velocity.rotate(random.randint(-30, 30)) # direction of movement from start, random select
        position = edge[1](random.uniform(0, 1)) # edge lambda function * a random position along that edge = spawn point
        kind = random.randint(1, ASTEROID_KINDS) # kind (or type) of asteroid, random select
        
        self.spawn_timer += dt # keeps track of time elapsed
        self.timer += dt
        
        if self.spawn_timer >= self.spawn_rate:
            self.spawn_asteroid(ASTEROID_MIN_RADIUS * kind, position, velocity) # call spawn method on these four properties
            self.spawn_timer = 0.0 # reset
        if self.timer >= 5.0:
            self.spawn_rate *= 0.9 # spawn faster, shorter interval
            self.timer = 0.0 # reset

        self.upgrade_timer += dt
        if self.upgrade_timer >= self.upgrade_rate:
            self.spawn_upgrade(UPGRADE_RADIUS, position, velocity)
            self.upgrade_timer = 0.0 # reset

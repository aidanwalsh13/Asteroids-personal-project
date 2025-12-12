import pygame # essential graphic, sound, input
import random # for nonplayer properties and spawn
from nonplayer import *
from constants import * # values for screen size, asteroid size, asteroid kinds
from player import Player
from upgrades import *
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

        self.clock = 0.0 # clock value for display, tbc

        self.player = player
        self.timer = 0.0

        self.spawn_timer = 0.0 # initialise to track time since last asteroid spawn
        self.spawn_rate = 0.5
        self.asteroids = []
        
        self.smg_timer = 0.0 # since last upgrade
        self.smg_rate = random.uniform(10, 15) # every 10-15 secs
        self.smgs = []

        self.SG_timer = 0.0
        self.SG_rate = random.uniform(10, 15) # every 10-15 secs
        self.SGs = []

    def spawn_asteroid(self, radius, position, velocity): # method for creating nonplayer object
        asteroid = Asteroid(position.x, position.y, radius, self.player)
        asteroid.velocity = velocity
        self.asteroids.append(asteroid)

    def spawn_SMGUpgrade(self, radius, position, velocity): # method for creating upgrade object
        smg = SMGUpgrade(position.x, position.y, radius, self.player)
        #upgrade_class = random.choice([SMGUpgrade, ShotgunUpgrade, etc]) # randomise choice, or create new specific sub-class
        #upgrade = upgrade_class(position.x, position.y, radius, self.player)
        smg.velocity = velocity
        self.smgs.append(smg)

    def spawn_ShotgunUpgrade(self, radius, position, velocity): # method for creating upgrade object
        SG = ShotgunUpgrade(position.x, position.y, radius, self.player)
        SG.velocity = velocity
        self.SGs.append(SG)

    def update(self, dt):
        self.spawn_timer += dt # keeps track of time elapsed
        self.smg_timer += dt
        self.SG_timer += dt
        self.timer += dt
        self.clock += dt

        # for spawning a new asteroid at a random edge
        edge = random.choice(self.edges) # where to spawn, random select
        speed = random.randint(40, 100) # random object speed
        velocity = edge[0] * speed # direction vector from random edge * random select speed
        velocity = velocity.rotate(random.randint(-30, 30)) # direction of movement from start, random select
        position = edge[1](random.uniform(0, 1)) # edge lambda function * a random position along that edge = spawn point
        kind = random.randint(1, ASTEROID_KINDS) # kind (or type) of asteroid, random select
        
        if self.spawn_timer >= self.spawn_rate:
            self.spawn_asteroid(ASTEROID_MIN_RADIUS * kind, position, velocity) # call spawn method on these four properties
            self.spawn_timer = 0.0 # reset. counts until it matches spawn_rate, then spawns and resets

        if self.timer >= 8.0:
            self.spawn_rate *= 0.95 # spawn faster, shorter interval
            self.timer = 0.0 # reset. every 5 secs, asteroid spawn rate goes up

        if self.smg_timer >= self.smg_rate:
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            smg_velocity = edge[0] * speed
            smg_velocity = smg_velocity.rotate(random.randint(-30, 30))
            smg_position = edge[1](random.uniform(0, 1))

            self.spawn_SMGUpgrade(UPGRADE_RADIUS, smg_position, smg_velocity)
            self.smg_timer = 0.0

        if self.SG_timer >= self.SG_rate:
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            sg_velocity = edge[0] * speed
            sg_velocity = sg_velocity.rotate(random.randint(-30, 30))
            sg_position = edge[1](random.uniform(0, 1))

            self.spawn_ShotgunUpgrade(UPGRADE_RADIUS, sg_position, sg_velocity)
            self.SG_timer = 0.0

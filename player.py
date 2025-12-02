from circleshape import CircleShape
from constants import *
import pygame
from shot import *

class Player(CircleShape):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, PLAYER_RADIUS) # super/parent constructor (circleshape)
        self.rotation = 0
        self.timer = 0

    @property
    def pos(self):
        # return the specific player position when someone accesses `player.pos`
        return self.position

    def triangle(self): # this def requires more study
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c] # isosceles triangle

    def draw(self, screen): # pygame method
        pygame.draw.polygon(
            screen, # where
            "white", # colour
            self.triangle(), # what
            2 # width. formerly 4
        )

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt # eg 300 / 60 = 5 degrees per frame (per millisecond) OR 300 per sec

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:  # key:d = rotate right
            self.rotate(dt)
        if keys[pygame.K_a]:  # key:a = rotate left
            self.rotate(-dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if self.timer > 0:
            self.timer -= dt
        if self.timer < 0:
            self.timer = 0

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation) # currently facing
        self.position += forward * PLAYER_SPEED * dt # when keys(w and s) are pressed in update, forward and back

    def shoot(self):
        if self.timer > 0:
            return None
        
        #shotgun mode //
        spread = [20, 10, 0, -10, -20]
        base_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        #5 shots
        for s in spread:
            shot = Shot(self.position.x, self.position.y)
            direction = base_direction.rotate(s)
            shot.velocity = direction * PLAYER_SHOOT_SPEED
        # //

        #single shot //
        #shot = Shot(self.position.x, self.position.y)
        #shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        # //
        self.timer = PLAYER_SHOOT_COOLDOWN
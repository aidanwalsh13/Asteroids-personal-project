import pygame

class CircleShape(pygame.sprite.Sprite): # all game objects are really circles
    def __init__(self, x, y, radius): # init position and size
        if hasattr(self, "containers"): # objects with "containers" include asteroids, bullets, players
            super().__init__(self.containers) # so init these in CircleShape class
        else:
            super().__init__() # avoid containers if you need more time for set up, or more specific logic

        self.position = pygame.Vector2(x, y) # place from pygame
        self.velocity = pygame.Vector2(0, 0) # speed from pygame
        self.radius = radius # size to be input during construction

    def collide(self, other):
        distance = self.position.distance_to(other.position) # position is a pygame.Vector2. distance_to is pygame method
        return distance <= self.radius + other.radius

    def draw(self, screen):
        # sub-classes will override
        pass

    def update(self, dt):
        # sub-classes will override
        pass

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import sys
import pygame
from constants import *
from player import Player
from nonplayer import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    print("This IS my time to shhshhshhSHINE")

    pygame.init()
    clock = pygame.time.Clock()
    # using dt # delta time: the amount of time since last frame generated
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable) # Player object containers. update and draw these
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # instantiate player. creating instance in centre of screen
    field = AsteroidField(player)

    while True: # this game will run FOREVER... or until I close it down and it doensn't get buggy
# useful for games, servers, event monitoring (ie waiting for a button input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # able to close the game when necessary
                return

        dt = clock.tick(60) / 1000 # 1/60th of a second. 60 seconds, dt: the amount of time since last frame

        screen.fill("gold") # any colour I want

        for sprite in updatable:
            sprite.update(dt)
        for sprite in drawable:
            sprite.draw(screen)

        for asteroid in asteroids:
            if player.collide(asteroid):
                sys.exit()
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collide(shot):
                    shot.kill()
                    asteroid.split()

        pygame.display.flip() # flip the canvas over and see what I have created!
# BE SURE TO CALL THIS LAST TO ENSURE IT REFRESHES THE SCREEN AT THE END OF EACH LOOP

# now our screen runs and stays open
if __name__ == "__main__":
    main()

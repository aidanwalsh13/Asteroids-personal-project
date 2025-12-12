import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import sys
import pygame
from constants import *
from player import Player
from nonplayer import Asteroid
from shot import Shot
from asteroidfield import AsteroidField
from upgrades import *

def load_high_score():
	try:
		with open(HIGH_SCORE_FILE, "r") as file:
			high_score = int(file.read())
	except (FileNotFoundError, ValueError):
		high_score = 0
	return high_score

def save_high_score(new_score):
	try:
		with open(HIGH_SCORE_FILE, "w") as file:
			file.write(str(new_score))
	except IOError as e:
		print(f"Error saving high score: {e}")

def main():

    pygame.init()

    pygame.font.init()
    score_font = pygame.font.SysFont("AriaL", 30)

    clock = pygame.time.Clock()
    # using dt # delta time: the amount of time since last frame generated
    dt = 0.0
    timer = 0.0 # keeping track of how long has passed since game start

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    score = 0
    current_high_score = load_high_score()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    upgrades = pygame.sprite.Group()

    Player.containers = (updatable, drawable) # Player object containers. update and draw these
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)
    Upgrade.containers = (updatable, drawable, upgrades)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # instantiate player. creating instance in centre of screen
    field = AsteroidField(player)

    while True: # this game will run FOREVER... or until I close it down and it doesn't get buggy
# useful for games, servers, event monitoring (ie waiting for a button input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # able to close the game when necessary
                return

        dt = clock.tick(60) / 1000 # 1/60th of a second. 60 seconds, dt: the amount of time since last frame

        timer += dt # tick tock

        screen.fill("black") # any colour I want

        for sprite in updatable:
            sprite.update(dt)
        for sprite in drawable:
            sprite.draw(screen)

        for asteroid in asteroids:
            if player.collide(asteroid):
                print(f"Game over! Your final score was: {score}")
                if score > current_high_score:
                    print(f"Congratulations! Your new high score is: {score}")
                    save_high_score(score)
                else:
                    print(f"The high score remains: {current_high_score}")
                sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collide(shot):
                    shot.kill()
                    hit_score = asteroid.split()
                    score += hit_score

        for upgrade in upgrades:
            if player.collide(upgrade):
                upgrade.buff(player)
                upgrade.kill()

        score_text_string = f"Score: {score}"
        text_surface = score_font.render(score_text_string, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        pygame.display.flip() # flip the canvas over and see what I have created!
# BE SURE TO CALL THIS LAST TO ENSURE IT REFRESHES THE SCREEN AT THE END OF EACH LOOP

# now our screen runs and stays open
if __name__ == "__main__":
    main()
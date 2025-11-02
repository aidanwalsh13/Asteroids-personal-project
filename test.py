import pygame
from nonplayer import Asteroid

pygame.init()
screen = pygame.display.set_mode((200, 200))

a = Asteroid(50, 60)
a.velocity = pygame.Vector2(30, -20)  # px/sec

dt = 1.0  # one second
before = a.position.copy()
a.update(dt)
after = a.position

print("moved:", after - before)  # expect ~[30, -20]

screen.fill((0, 0, 0))
a.draw(screen)
pygame.display.flip()
pygame.time.delay(500)
pygame.quit()

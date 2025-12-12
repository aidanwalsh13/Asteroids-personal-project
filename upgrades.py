import pygame
from circleshape import CircleShape
from constants import *
import random
from player import Player

class Upgrade(CircleShape): # dont forget to add to containers
	def __init__(self, x, y, radius, player):
		super().__init__(x, y, radius)
		self.player = player

	def draw(self, screen):
		pass

	def update(self, dt):
		self.position += self.velocity * dt
	
	def buff(self, player):
		pass

# gun type upgrades
class SMGUpgrade(Upgrade):
	def __init__(self, x, y, radius, player):
		super().__init__(x, y, radius, player)

	def draw(self, screen):
		pygame.draw.circle(
			screen,
			"green",
			self.position,
			self.radius,
			4
		)

	def buff(self, player):
		player.fire_rate /= 1.1

class ShotgunUpgrade(Upgrade):
	def __init__(self, x, y, radius, player):
		super().__init__(x, y, radius, player)

	def draw(self, screen):
		pygame.draw.circle(
			screen,
			"orange",
			self.position,
			self.radius,
			4
		)

	def buff(self, player):
		player.spread_layer += 1
		offset = player.spread_layer * 10
		player.spread.append(-offset)
		player.spread.append(offset)


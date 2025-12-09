import pygame
from circleshape import CircleShape
from constants import *
import random
from player import Player

class Upgrade(CircleShape): # dont forget to add to containers
	def __init__(self, x, y, radius, player):
		super().__init__(x, y, radius)
		self.player = player

	#def buff(self, player):
	#	distance = self.position.distance_to(player.position)
	#	return distance <= self.radius + player.radius
	# this replaced with def collide in circleshape.py

	def draw(self, screen):
		pygame.draw.circle(
			screen,
			"green",
			self.position,
			self.radius,
			4
		)

	def update(self, dt):
		self.position += self.velocity * dt
	
	def buff(self, player):
		pass

class SMGupgrade(Upgrade):
	def __init__(self, x, y, radius, player):
		super().__init__(x, y, radius, player)

	def buff(self, player):
		player.fire_rate /= 5
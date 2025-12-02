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
		pygame.draw.circle(
			screen,
			"green",
			self.position,
			self.radius,
			4
		)

	def buff(self, player):
		distance = self.position.distance_to(player.position)
		return distance <= self.radius + player.radius

	def update(self, dt):
		self.position += self.velocity * dt
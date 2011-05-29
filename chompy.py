import pygame
class Chompy(pygame.sprite.Sprite):
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("gfx/chompy.png").convert_alpha()
		
		self.rect = self.image.get_rect()
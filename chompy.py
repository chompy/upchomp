import pygame, math

GRAVITY = -9.81
grav_rate = GRAVITY / 20
max_speed = 16

class Chompy(pygame.sprite.Sprite):
    def __init__(self):
        self.speed = 0.0    
        self.falling = 0    
        		
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("gfx/chompy.png").convert_alpha()
		
        self.rect = self.image.get_rect()
        self.colliderect = pygame.Rect(self.rect.x, self.rect.x, self.rect.w, self.rect.h)
    
        self.pos = [self.rect.x, self.rect.y]
		
    def update(self,scroll,move,size):
        # Gravity
        self.falling += grav_rate * -1
        if self.falling > GRAVITY * -1: self.falling = GRAVITY * -1
        self.pos[1] += self.falling
   
        # Movement
        if move:              
            if move > size[0] / 2:
                self.pos[0] += math.floor(self.speed)
                if self.speed < max_speed: self.speed += float(max_speed) / 32.0
            else:
                self.pos[0] += math.floor(self.speed)
                if self.speed > max_speed * -1: self.speed -= float(max_speed) / 32.0
        else: 
            self.pos[0] += math.floor(self.speed)
            if abs(self.speed) < 1: self.speed = 0
            elif self.speed > 0: self.speed -= float(max_speed) / 64.0
            elif self.speed < 0: self.speed += float(max_speed) / 64.0            

        # Update position
        self.colliderect.x = self.pos[0]
        self.colliderect.y = self.pos[1]
       
        self.rect.x= self.pos[0] + scroll[0]
        self.rect.y= self.pos[1] + scroll[1]
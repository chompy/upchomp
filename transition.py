import pygame,math

SPEED = 16

class Transition(object):

    def __init__(self):
        self.type = 0

    def verticalSwipe(self,size):
        self.type = 1
        self.speed = math.floor(size[1] / SPEED)
        self.size = size
        self.surface = pygame.Surface((size[0],size[1]))
        self.surface.fill([0,0,0])
        self.pos = [0,-size[1]]

    def update(self,screen):
        if not self.type: return 0
        
        # Update a vertical swipe
        elif self.type == 1:
            if self.pos[1] < self.size[1] * 2:
                self.pos[1] += self.speed 
                screen.blit(self.surface, (self.pos[0],self.pos[1]))
            return (self.size[1] * 2.0) / (self.pos[1] + self.size[1])
        
        
        
        

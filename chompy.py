import pygame, math

GRAVITY = -9.81
grav_rate = GRAVITY / 20
max_speed = 8.0
speed_rate = max_speed * 2.0

class Chompy(pygame.sprite.Sprite):
    def __init__(self):
       		
        """Load a Chompy sprite."""
    
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("gfx/chompy.png").convert_alpha()
		
        self.rect = self.image.get_rect()
        self.colliderect = pygame.Rect(self.rect.x, self.rect.x, self.rect.w, self.rect.h)
        
        self.moveok = 1
        
        self.skills = {
            'heli'    : 0,
            'up'      : 0
        }
   	
    def reset(self):
    
        """Resets Chompy back to his default state."""
        
        self.speed = 0.0    
        self.falling = 0  
        self.pos = [self.rect.x, self.rect.y]  
    
    def activateSkill(self, name):
        """
        Activates a Chompy skill!
        
        @param string name - Name of skill to activate.
        @return bool - True if skill was activated.
        """ 

        if name == "heli":
            self.skills['heli'] = 90
            return 1
        elif name == "up":
            self.falling = -10
        else:
            return 0
        	
    def update(self,scroll,move,size):
    
        """
        Updates Chompy's position.
        
        @param array scroll Screen scroll position.
        @param double move Direction player is attempt to make Chompy move in.
        @param array size Current screen size.
        """
        
        # Skills
        if self.skills['heli'] > 0: self.skills['heli'] -= 1
        
        # Gravity [Ignore gravity when Heli skill is activate or Chompy is jumping]
        if not self.skills['heli'] or self.falling < 0:
            self.falling += (grav_rate) * -1
            if self.falling > GRAVITY * -1: self.falling = (GRAVITY * -1)
            self.pos[1] += self.falling
        
        # Movement
        if move and self.moveok:              
            if move > 1:
                self.pos[0] += math.floor(self.speed)
                if self.speed < max_speed: self.speed += ((float(max_speed) / speed_rate))
            elif move < -1:
                self.pos[0] += math.floor(self.speed)
                if self.speed > max_speed * -1: self.speed -= ((float(max_speed) / speed_rate))
        else: 
            self.pos[0] += math.floor(self.speed)
            if abs(self.speed) < 1: self.speed = 0
            elif self.speed > 0: self.speed -= (float(max_speed) / (speed_rate * 2.0) )
            elif self.speed < 0: self.speed += (float(max_speed) / (speed_rate * 2.0) )
        
        # If Chompy goes up into the air reenable movement.
        if self.falling < 0: self.moveok = 1

        # Update position
        self.colliderect.x = self.pos[0]
        self.colliderect.y = self.pos[1]
        
        self.rect.x= self.pos[0] + scroll[0]
        self.rect.y= self.pos[1] + scroll[1]

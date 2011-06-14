import pygame, math

GRAVITY = -9.81
grav_rate = GRAVITY / 20
max_speed = 8.0
speed_rate = max_speed * 2.0

TILE_SIZE = [32,32]

class Chompy(pygame.sprite.Sprite):
    def __init__(self):
       		
        """Load a Chompy sprite."""
    
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("gfx/chompy.png").convert_alpha()
        
        # Heli Skill tiles
        self.heli = pygame.image.load("gfx/heli.png").convert_alpha()
        self.heli_tiles = self.loadTiles(self.heli)

        self.progress = pygame.Surface((TILE_SIZE[0], 1))
		
        self.rect = self.image.get_rect()
        self.colliderect = pygame.Rect(self.rect.x, self.rect.x, self.rect.w, self.rect.h)
        
        self.moveok = 1
        
        self.skills = {
            'heli'    : 0,
            'up'      : 0
        }
        
    def loadTiles(self, image):
    
        """
        Load tiled images.
        
        @param pygame.image.load 
        @return array Tile table
        """
    
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_x in range(0, image_width/TILE_SIZE[0]):
            line = []
            tile_table.append(line)
            for tile_y in range(0, image_height/TILE_SIZE[1]):
                rect = (tile_x*TILE_SIZE[0], tile_y*TILE_SIZE[1], TILE_SIZE[0], TILE_SIZE[1])
                line.append(image.subsurface(rect))         
        
        return tile_table
   	
    def reset(self):
    
        """Resets Chompy back to his default state."""
        
        self.speed = 0.0    
        self.falling = 0  
        self.pos = [self.rect.x, self.rect.y]  
        self.moveok = 1       
        
        self.skills = {
            'heli'    : 0,
            'up'      : 0
        }
    
    
    def activateSkill(self, name, sound = ""):
        """
        Activates a Chompy skill!
        
        @param string name - Name of skill to activate.
        @return bool - True if skill was activated.
        """ 

        if name == "heli":
            self.skills['heli'] = 90
            self.progress_max = 90
            
            if sound: sound.playSfx("sfx/heli.wav", -1)
            return 1
        elif name == "up":
            self.falling = -10
        else:
            return 0
        	
    def update(self, scroll, screen, move, size, sound):
    
        """
        Updates Chompy's position.
        
        @param array scroll Screen scroll position.
        @param pygame.display.set_mode screen
        @param double move Direction player is attempt to make Chompy move in.
        @param array size Current screen size.
        """
        
        # Skills
        
        # Heli
        if self.skills['heli'] > 0: 
            self.skills['heli'] -= 1
            ani = pygame.time.get_ticks() % 4
                        
            screen.blit(self.heli_tiles[ani][0], (self.rect.x, self.rect.y - TILE_SIZE[1]))
            
            if self.falling > 0: self.falling = 0
        
        if self.skills['heli'] == 1: sound.stopSfxFile("sfx/heli.wav")
                    
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

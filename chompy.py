"""
    UpChomp - A momentum game staring Chompy
    Copyright (C) 2011 Nathan Ogden
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pygame, math, imagehelper

# Image Helper Object
imghelp = imagehelper.imageHelper()

# Constants
GRAVITY = -9.81
grav_rate = GRAVITY / 20
max_speed = 6.0
speed_rate = max_speed / 10

TILE_SIZE = [256,256]

class Chompy(pygame.sprite.Sprite):
    def __init__(self, screen, sound):

        """
        Load a Chompy sprite.
        
        @param pygame.screen - Screen rendering object.
        @param sound object - Sound handler class.        
        """
        
        self.screen = screen
        self.sound = sound

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("gfx/chompy.png").convert_alpha()
        self.image2 = self.image
               
        self.rect = self.image.get_rect()
        self.colliderect = pygame.Rect(self.rect.x, self.rect.x, self.rect.w, self.rect.h)

        self.moveok = 1
        self.stopclock = -1

        self.skills = {
            'heli'    : 0,
            'up'      : 0
        }
        
        self.tile_size  = 32
        
        self.splashTimer = 0
        self.splashPos = [0,0]
        self.hasSplashed = 0

    def resize(self, size):
    
        """
        Resizes Chompy and objects related to Chompy
        to the current screen size.
        
        @param array size - Width and Height of current screen.
        """
    
        # Heli Skill tiles
        self.heli = pygame.image.load("gfx/heli.png").convert_alpha()
        self.splash = pygame.image.load("gfx/splash.png").convert_alpha()
        
        heli_size = self.heli.get_size()
        heli_tile = [heli_size[0] / 256, heli_size[1] / 256]
        self.heli = pygame.transform.smoothscale(self.heli, (int(heli_tile[0] * size), int(heli_tile[1] * size)))
        self.heli_tiles = imghelp.makeTiles(self.heli, [int(size), int(size)])
            
        self.image = pygame.transform.smoothscale(self.image2, (int(size), int(size)))   
        self.rect = self.image.get_rect()
        self.colliderect = pygame.Rect(self.rect.x, self.rect.x, self.rect.w, self.rect.h)
        
        self.splash = pygame.transform.smoothscale(self.splash, (int(size), int(size)))   
        
        old_tile_size = self.tile_size        
        self.tile_size = size         
        
        self.pos[0] = self.pos[0] * (self.tile_size / old_tile_size)
        self.pos[1] = self.pos[1] * (self.tile_size / old_tile_size)
        
    def reset(self):

        """Resets Chompy back to his default state."""

        self.speed = 0.0
        self.falling = 0
        self.pos = [self.rect.x, self.rect.y]
        self.moveok = 1
        
        self.splashTimer = 0
        self.splashPos = [0,0]
        self.hasSplashed = 0        

        self.skills = {
            'heli'    : 0,
            'up'      : 0
        }

    def setSplash(self, pos):
    
        """
        Make Chompy splash in water.
        
        @param array pos - X and Y pos of where the splash should occur.
        """
    
        if self.splashTimer <= 0:
            self.splashPos = pos
            self.splashTimer = 40
            self.hasSplashed = 1  
            self.sound.playSfx("sfx/splash.wav", 0) 
                    
    def activateSkill(self, name):
        """
        Activates a Chompy skill!

        @param string name - Name of skill to activate.
        @return bool - True if skill was activated.
        """

        # Heli Skill - Chompy floats in mid air for ~3 seconds.
        if name == "heli":
            self.skills['heli'] = 90 # Ticks down every frame, 30 FPS = 3 seconds.
            self.progress_max = 90
            self.falling = -1

            if self.sound: self.sound.playSfx("sfx/heli.wav", -1)
            return 1
            
        # Up Skill - Makes Chompy shoot up.
        elif name == "up":
            if self.sound: self.sound.playSfx("sfx/up.wav", 0)
            self.falling = -10
        else:
            return 0
            
    def update(self, scroll, move, size):

        """
        Updates Chompy's position.

        @param array scroll Screen scroll position.
        @param double move Direction player is attempt to make Chompy move in.
        @param array size Current screen size.
        """

        # === Skills ===

        # Heli
        if self.skills['heli'] > 0:
            self.skills['heli'] -= 1
            ani = pygame.time.get_ticks() % 4

            self.screen.blit(self.heli_tiles[ani][0], (self.rect.x, self.rect.y - self.tile_size))

            if self.falling > 0: self.falling = 0

        if self.skills['heli'] == 1: self.sound.stopSfxFile("sfx/heli.wav")

        # Start the clock when Chompy is not moving...if it hits 0 game over.
        if self.stopclock > 0:
            self.stopclock -= 1

        # Gravity [Ignore gravity when Heli skill is activate or Chompy is jumping]
        if not self.skills['heli'] or self.falling < 0:
            self.falling += (grav_rate) * -1
            if self.falling > GRAVITY * -1: self.falling = (GRAVITY * -1)
            self.pos[1] += self.falling / (32 / self.tile_size)

        # Movement
        if move and self.moveok:
            if move > 4: move = 4
            elif move < -4: move = -4

            if move > 0 and move < .5: move = .5
            elif move < 0 and move > -.5: move = -.5

            self.pos[0] += math.floor(self.speed) / (32 / self.tile_size)
            if move > 0 and self.speed < max_speed: self.speed += speed_rate
            if move < 0 and self.speed > max_speed * -1: self.speed -= speed_rate
 
        else:
            self.pos[0] += math.floor(self.speed) / (32 / self.tile_size)
            if abs(self.speed) < 1: self.speed = 0
            elif self.speed > 0: self.speed -= speed_rate / 4
            elif self.speed < 0: self.speed += speed_rate / 4
           
        # Water Splash
        if self.splashTimer > 0:
            self.splashTimer -= 1
            self.screen.blit(self.splash, (self.splashPos[0], self.splashPos[1]))
            
        # If Chompy goes up into the air reenable movement.
        if self.falling < 0 or self.falling > 1: self.moveok = 1

        # Update position
        self.colliderect.x = self.pos[0]
        self.colliderect.y = self.pos[1]

        self.rect.x= self.pos[0] + scroll[0]
        self.rect.y= self.pos[1] + scroll[1]

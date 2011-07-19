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

import pygame,math

SPEED = 16

class Transition(object):

    def __init__(self):
    
        """ Inits transition object. """
    
        self.type = 0

    def verticalSwipe(self,size):
    
        """
        Begins rendering a vertical swipe.
        
        @param array size - Width and height of game window.
        """
    
        self.type = 1
        self.speed = math.floor(size[1] / SPEED)
        self.size = size
        self.surface = pygame.Surface((size[0],size[1]))
        self.surface.fill([0,0,0])
        self.pos = [0,-size[1]]

    def update(self,screen):
    
        """
        Updates and renders the transition again.
        
        @param pygame.screen screen - Pygame screen object.
        @return float - Vertical position of transition.
        """
    
        if not self.type: return 0

        # Update a vertical swipe
        elif self.type == 1:
            if self.pos[1] < self.size[1] * 2:
                self.pos[1] += self.speed
                screen.blit(self.surface, (self.pos[0],self.pos[1]))
            return (self.size[1] * 2.0) / (self.pos[1] + self.size[1])

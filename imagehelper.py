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

class imageHelper(object):
    
    """
    Handles various image related task.
    """

    def makeTiles(self, surface, tilesize):
    
        """
        Makes tiles out of a surface.
        
        @param pygame.surface surface - Pygame Surface object.
        @param array tilesize - Array containing width and height of tiles.
        
        @return array - Contains a seperate surface for each tile created.
        """
    
        image_width, image_height = surface.get_size()       
        tile_table = []
        for tile_x in range(0, int(image_width/tilesize[0])):
            line = []
            tile_table.append(line)
            for tile_y in range(0, int(image_height/tilesize[1])):
                rect = (tile_x * tilesize[0], tile_y * tilesize[1], int(tilesize[0]), int(tilesize[1]))
                line.append(surface.subsurface(rect))       
        return tile_table
        
        
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
        for tile_x in range(0, image_width/tilesize[0]):
            line = []
            tile_table.append(line)
            for tile_y in range(0, image_height/tilesize[1]):
                rect = (tile_x * tilesize[0], tile_y * tilesize[1], tilesize[0], tilesize[1])
                line.append(surface.subsurface(rect))       
        return tile_table
        
        
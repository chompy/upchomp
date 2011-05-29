import pygame
class Gamemap(object): 

    def __init__(self, filename, width, height, maptilewidth):
        self.maptilewidth = maptilewidth
        image = pygame.image.load(filename).convert()
        image_width, image_height = image.get_size()
        self.tile_table = []
        for tile_x in range(0, image_width/width):
            line = []
            self.tile_table.append(line)
            for tile_y in range(0, image_height/height):
                rect = (tile_x*width, tile_y*height, width, height)
                line.append(image.subsurface(rect))
                
    def collision(self,sprite,tile):
        return 0

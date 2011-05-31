import pygame, math
class Gamemap(object): 

    def __init__(self, filename, width, height, maptilewidth):
        self.tilewidth = width
        self.tileheight = height
        self.maptilewidth = maptilewidth
        self.scroll = [0,0]
        
        image = pygame.image.load(filename).convert()
        image_width, image_height = image.get_size()
        self.tile_table = []
        for tile_x in range(0, image_width/width):
            line = []
            self.tile_table.append(line)
            for tile_y in range(0, image_height/height):
                rect = (tile_x*width, tile_y*height, width, height)
                line.append(image.subsurface(rect))
                
    def collision(self,sprite,tileno,scroll):
        tile_x = ((tileno % self.maptilewidth) * self.tilewidth) + scroll[0]
        tile_y = math.floor((tileno / self.maptilewidth) * self.tileheight) + scroll[1]

        if ((sprite.rect.x >= tile_x and sprite.rect.x <= tile_x + self.tilewidth)) or ((sprite.rect.x + sprite.rect.w >= tile_x and sprite.rect.x + sprite.rect.w <= tile_x + self.tilewidth)):
          if ((sprite.rect.y >= tile_y and sprite.rect.y <= tile_y + self.tileheight) or (sprite.rect.y + sprite.rect.h >= tile_y and sprite.rect.y + sprite.rect.h <= tile_y + self.tileheight)):
            
            return [tile_x  - sprite.rect.x, tile_y - sprite.rect.y]
        return 0

import pygame, math, ConfigParser
class Gamemap(object): 

    def __init__(self, map="map1.map"):
        self.parser = ConfigParser.ConfigParser()
        self.parser.read("map/"+map)
        
        self.themeparser = ConfigParser.ConfigParser()
        self.themeparser.read("tile/" + self.parser.get("level","theme") + ".ini")
        
        self.tilesize = [int(self.themeparser.get("images","tile_width")), int(self.themeparser.get("images","tile_height"))]
        
        
        # Begin parsing map
        mapp = self.parser.get("level","map")
        # Remove all spaces...
        mapp = mapp.replace(" ","")
        # Each line is seperated by a return.
        mapp = mapp.split("\n")
               
        # Load the tiles into an array.
        self.map = []
        self.mapwidth = 0
        self.mapheight = len(mapp)
        for i in mapp:
            if len(i) > self.mapwidth: self.mapwidth = len(i)
            for x in range(len(i)):
                self.map.append(i[x])
     
        # Load the tile images and begin placing them...               
        image = pygame.image.load("gfx/" + self.themeparser.get("images","tileset")).convert_alpha()
        image_width, image_height = image.get_size()
        self.tile_image_size = [image_width,image_height]
        self.tile_table = []
        for tile_x in range(0, image_width/self.tilesize[0]):
            line = []
            self.tile_table.append(line)
            for tile_y in range(0, image_height/self.tilesize[1]):
                rect = (tile_x*self.tilesize[0], tile_y*self.tilesize[1], self.tilesize[0], self.tilesize[1])
                line.append(image.subsurface(rect))

                
        # Load background
        if self.themeparser.get("images","background"):
            self.background = pygame.image.load("gfx/" + self.themeparser.get("images","background")).convert()
            self.bg_rect = self.background.get_rect()
            screensize = pygame.display.get_surface()
            screensize = screensize.get_size()
            if screensize[1] > self.mapheight * self.tilesize[1]: self.bgrows = (int(screensize[1]/self.bg_rect.height) + 1) * 4
            else: self.bgrows = (int( (self.mapheight * self.tilesize[1]) /self.bg_rect.height) + 1) * 4
            
            if screensize[0] > self.mapwidth * self.tilesize[0]: self.bgcolumns = (int(screensize[0]/self.bg_rect.width) + 1) * 4
            else: self.bgcolumns = (int( (self.mapwidth * self.tilesize[0]) /self.bg_rect.width) + 1) * 4
                                        
    def collision(self,rect,tileno):
        tile_x = ((tileno % self.mapwidth) * self.tilesize[0])
        tile_y = math.floor((tileno / self.mapwidth) * self.tilesize[1])
        tile_rect = pygame.Rect(tile_x, tile_y, self.tilesize[0], self.tilesize[1])
        return rect.colliderect(tile_rect)
import pygame, math, ConfigParser
class Gamemap(object): 

    def __init__(self, map="map1.map"):
        self.parser = ConfigParser.ConfigParser()
        self.parser.read("map/"+map)
        
        self.themeparser = ConfigParser.ConfigParser()
        self.themeparser.read("tile/" + self.parser.get("level","theme") + ".ini")
        
        self.tilesize = [int(self.themeparser.get("images","tile_width")), int(self.themeparser.get("images","tile_height"))]
        
        # Variables to use...
        
        # Level states... 0-Playing, 1-Won, 2-Lost
        self.state = 0

        # Animation Clock
        self.animation = pygame.time.get_ticks()
        self.collide_animation = []
        
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
        
    
    def drawBackground(self,screen,scroll):

        if self.themeparser.get("images","background"):
            self.bg_rect.x -= self.bg_rect.w + (scroll[0] / 8)
            self.bg_rect.y -= self.bg_rect.h + (scroll[1] / 8)
            for yy in xrange(self.bgrows):
                for xx in xrange(self.bgcolumns):
                    # Start a new row
                    if xx == 0 and yy > 0:
                        # Move the rectangle
                        self.bg_rect = self.bg_rect.move([-(self.bgcolumns -1 ) * self.bg_rect.width, self.bg_rect.height])
                    # Continue a row
                    if xx > 0:
                        # Move the rectangle
                        self.bg_rect = self.bg_rect.move([self.bg_rect.width, 0])
                    screen.blit(self.background,self.bg_rect)
            self.bg_rect.x = 0
            self.bg_rect.y = 0
            
    def updateTiles(self,screen,scroll,clock,chomp):
        # Animation clock
        self.animation = pygame.time.get_ticks()
        
        # Draw the level
        x = 0
        i = 0 
        for i in self.map:
            # Render Tiles
    
            tile_x = ((x % self.mapwidth) * self.tilesize[0])
            tile_y = (math.floor(x / self.mapwidth) * self.tilesize[1])        
            
            if self.themeparser.get(i, "tile"):
                
                tile = self.themeparser.getint(i, "tile")
                
                # Tiles with animation
                if self.themeparser.get(i, "animation"):
                    if not self.themeparser.get(i, "collide") or not self.themeparser.getboolean(i, "animate_on_collide"):
                        tile = tile + (math.floor(self.animation / (1000 / self.themeparser.getint("images", "animation_framerate")) ) % (self.themeparser.getint(i, "animation") - self.themeparser.getint(i, "tile")))
                    else:
    
                        for y in range(len(self.collide_animation)):
                           
                            if self.collide_animation[y][0] == x and self.collide_animation[y][1] > math.floor(self.collide_animation[y][2] / (math.floor(clock.get_fps()) / self.themeparser.getint("images", "animation_framerate"))):                          
                                tile = tile + math.floor(self.collide_animation[y][2] / (math.floor(clock.get_fps()) / self.themeparser.getint("images", "animation_framerate")))
                                self.collide_animation[y][2] += 1
                                break
                 
                tile_frame_x = tile % (self.tile_image_size[0] / self.tilesize[0])
                tile_frame_y = math.floor(tile / (self.tile_image_size[0] / self.tilesize[0]))
    
                
    
                screen.blit(self.tile_table[int(tile_frame_x)][int(tile_frame_y)], (tile_x + scroll[0], tile_y + scroll[1] ) )
    
                
            # Collision with a tile
            if self.themeparser.getboolean(i,"collide"):
                col = self.collision(chomp.colliderect,x)
                tilename = self.themeparser.get(i, "name")
                
                # If a collision happens...
                if col:
                    
                    # If an animation was supposed to play when the collision happened...
                    if self.themeparser.get(i, "animation") and self.themeparser.getboolean(i, "animate_on_collide"):
                        
                        # Check to make sure this animation isn't already queued..
                        add_to_collide = 1                  
                        for y in range(len(self.collide_animation)):
                           
                            # If queued already reset the animation frame back to 0.
                            if self.collide_animation[y][0] == x: 
                                if math.floor(self.collide_animation[y][2] / (math.floor(clock.get_fps()) / self.themeparser.getint("images", "animation_framerate"))) == self.collide_animation[y][1]: self.collide_animation[y][2] = 0
                                add_to_collide = 0                           
                                break
                        
                        # If not queued add it to the queue..
                        if add_to_collide: 
                            self.collide_animation.append( [x, self.themeparser.getint(i, "animation") - self.themeparser.getint(i, "tile"), 0] )
                        
                    # If player hits a spring...
                    if tilename == "spring":
                        # Wait till first frame of animation is shown before springing.
                        for y in range(len(self.collide_animation)):
                            if self.collide_animation[y][0] == x: 
                                if self.collide_animation[y][2] / (math.floor(clock.get_fps()) / self.themeparser.getint("images", "animation_framerate")) > .3: chomp.falling = self.themeparser.getint(i, "value") * -1
                       
                    # If player hits the end of the level...
                    elif tilename == "level_end":
                        self.state = 1     # Set level state to win.                        
                                         
                    # Any other collision should just be treated like a wall or floor collision...
                    else:
                        tilerect = pygame.Rect(tile_x,tile_y,self.tilesize[0],self.tilesize[1])  
                        offset = [chomp.colliderect.x - tilerect.x, chomp.colliderect.y - tilerect.y]
    
                        # Check for horizontal collision...
                        if abs(offset[1]) <  self.tilesize[1] / 2:
                            if offset[0] >  self.tilesize[0] / 2: chomp.pos[0] = tilerect.x + self.tilesize[0]
                            elif offset[0] <=  self.tilesize[0] / 2: chomp.pos[0] = tilerect.x - self.tilesize[0]
                            chomp.speed = 0
                            
                        # Check for vertical collision.
                        if abs(offset[0]) < self.tilesize[0] / 2:
                            if offset[1] > 0: chomp.pos[1] = tilerect.y + self.tilesize[1]
                            elif offset[1] <= 0: chomp.pos[1] = tilerect.y -  self.tilesize[1]
                            chomp.falling = 0                
                       
            x += 1                

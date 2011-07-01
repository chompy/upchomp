import pygame, math, iniget, imagehelper, hashlib

# Image Helper Object
imghelp = imagehelper.imageHelper()

class Gamemap(object):

    def __init__(self, sound, save):

        """
        Inits the gamemap module, allows maps to be loaded and rendered.
        """

        # Animation Clock
        self.animation = pygame.time.get_ticks()
        self.collide_animation = []

        # Level states... 0-Playing, 1-Won, 2-Lost
        self.state = 0

        self.current_map = 0
        
        # Load Sound Object
        self.sound = sound
        
        # Load Save Ini
        self.save = save
        
        self.packMaps = []

    def loadLevel(self, map="map1.map", stage = -1):

        """
        Loads current map which is specified by the self.current_map var.
        @param string map - Map Pack Filename
        @param int stage - Map Pack Stage
        """
        # Load current map
        self.parser = iniget.iniGet("map/"+map)
        
        # Get selected stage.
        if stage > 0: self.current_map = stage
        
        # Get map hash (Used in save file)
        self.maphash = hashlib.sha224(open("map/"+map).read()).hexdigest()

        # Current map
        self.packMaps = self.parser.get("pack","order").split(",")

        # Load theme
        self.themeparser = iniget.iniGet("tile/" + self.parser.get(self.packMaps[self.current_map],"theme") + ".ini")

        # Load Music
        music = self.themeparser.get("music","file")
        if music: 
            self.sound.playSfx("sfx/" + music, 1, 1)
        
        # Get size of this maps tiles
        self.tilesize = [int(self.themeparser.get("tiles","tile_width")), int(self.themeparser.get("tiles","tile_height"))]

        # Begin parsing map
        mapp = self.parser.get(self.packMaps[self.current_map],"map")

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
        image = pygame.image.load("gfx/" + self.themeparser.get("tiles","tileset")).convert_alpha()
        image_width, image_height = image.get_size()
        self.tile_image_size = [image_width,image_height]
        tile_table = imghelp.makeTiles(image, self.tilesize)

        self.tile_table = []
        for x in range(len(tile_table)):
            self.tile_table.append([])
            for y in range(len(tile_table[x])):
                self.tile_table[x].append({
                    'original'          :   tile_table[x][y],
                    'v-flip'            :   pygame.transform.flip(tile_table[x][y], 0, 1),
                    '90deg'             :   pygame.transform.rotate(tile_table[x][y], 90),
                    '90deg_v-flip'      :   pygame.transform.flip(pygame.transform.rotate(tile_table[x][y], 90), 0, 1),
                    '180deg'            :   pygame.transform.rotate(tile_table[x][y], 180),
                    '180deg_v-flip'     :   pygame.transform.flip(pygame.transform.rotate(tile_table[x][y], 180), 0, 1),
                    '270deg'            :   pygame.transform.rotate(tile_table[x][y], 270),
                    '270deg_v-flip'     :   pygame.transform.flip(pygame.transform.rotate(tile_table[x][y], 270), 0, 1)
                })

        screensize = pygame.display.get_surface()
        screensize = screensize.get_size()

        # Load background
        bg_list = self.themeparser.get("background","images")
        bg_paralax = self.themeparser.get("background","paralax")
        bg_paralax = str(bg_paralax).split(",")
        if not bg_paralax: bg_paralax = 8
        
        self.background = []
        if bg_list:
            bg_list = bg_list.split(",")
           
            for i in range(len(bg_list)):
                image = pygame.image.load("gfx/" + bg_list[i]).convert_alpha()
                rect = image.get_rect()
            
                if self.themeparser.getBool("background","fit_to_window"):
                    tmprect = pygame.Rect(0, 0, screensize[0], screensize[1])
                    rect =  rect.fit(tmprect)
                    image = pygame.transform.scale(image, (rect.w, rect.h))    
                
                if not self.themeparser.getBool("background","no_repeat_y"):
                    if screensize[1] > self.mapheight * self.tilesize[1]: bgrows = (int(screensize[1] / rect.height) + 1) * 4
                    else: bgrows = (int( (self.mapheight * self.tilesize[1]) / rect.height) + 1) * 4
                else: bgrows = 1
    
                
                if screensize[0] > self.mapwidth * self.tilesize[0]: bgcolumns = (int(screensize[0] / rect.width) + 1) * 4
                else: bgcolumns = (int( (self.mapwidth * self.tilesize[0]) / rect.width) + 1) * 4            

                # Try to get paralax ammount, if none was specified then it won't be an array.
                try:
                    this_paralax = bg_paralax[i]
                except:
                    this_paralax = bg_paralax
                
                self.background.append({
                    'image'     :   image,
                    'rect'      :   rect,
                    'cols'      :   bgcolumns,
                    'rows'      :   bgrows,
                    'paralax'   :   int(this_paralax)
                })
                
        # Calculate Map stuff
        self.calcMap(screensize)


    def collision(self,rect,tileno):

        """
        Checks for a collision before a given rect and a map tile.

        @param pygame.rect rect - Rectangle of object colliding with a tile.
        @param int tileno - Tile number. Tile number goes from top left tile to bottom right tile.
        @return true if there is a collision
        """

        tile_x = ((tileno % self.mapwidth) * self.tilesize[0])
        tile_y = math.floor((tileno / self.mapwidth) * self.tilesize[1])
        tile_rect = pygame.Rect(tile_x, tile_y, self.tilesize[0], self.tilesize[1])
        return rect.colliderect(tile_rect)


    def drawBackground(self, screen, scroll, size):
        
        """
        Draws a background image and gives it paralax.

        @param pygame.display.set_mode screen - Screen object used to render items to the screen
        @param array scroll - X and Y offset of current map scroll.
        """

        for i in self.background:            
            i['rect'].x -= i['rect'].x - (scroll[0] / i['paralax']) + size[0]
            i['rect'].y -= i['rect'].y - (scroll[1] / i['paralax']) + size[1]
            for yy in xrange(i['rows']):
                for xx in xrange(i['cols']):
                    # Start a new row
                    if xx == 0 and yy > 0:
                        # Move the rectangle
                        i['rect'] = i['rect'].move([-(i['cols'] -1 ) * i['rect'].width, i['rect'].height])
                    # Continue a row
                    if xx > 0:
                        # Move the rectangle
                        i['rect'] = i['rect'].move([i['rect'].width, 0])
                    
                    # Bind BG to bottom if only one vertical image.        
                    if i['rows'] == 1: i['rect'].y = size[1] - i['rect'].h
                    
                    screen.blit(i['image'],i['rect'])
            i['rect'].x = 0
            i['rect'].y = 0

    def calcMap(self, size):
        self.tiles = []

        self.ani_framerate = float(self.themeparser.getInt("tiles", "animation_framerate"))

        x = 0
        for i in self.map:
            self.tiles.append( {
                'name'          :   self.themeparser.get(i, "name"),
                'type'          :   self.themeparser.get(i, "type"),
                'tile'          :   self.themeparser.getInt(i, "tile"),
                'animation'     :   self.themeparser.getInt(i, "animation"),
                'collide'       :   self.themeparser.getBool(i, "collide"),
                'ani_collide'   :   self.themeparser.getBool(i, "animate_on_collide"),
                'value'         :   self.themeparser.get(i, "value"),
                'collide_sfx'   :   self.themeparser.get(i, "collide_sfx"),
                'x'             :   ((x % self.mapwidth) * self.tilesize[0]),
                'y'             :   (math.floor(x / self.mapwidth) * self.tilesize[1]),
                'orientation'   :   self.themeparser.get(i, "orientation")
            })

            x += 1


    def updateTiles(self, screen, scroll, size, chomp, sound):

        """
        Draws all tiles to the screen.

        @param pygame.display screen - Screen object used to render items to the screen.
        @param array scroll - X and Y offset of current map scroll.
        @param array size - Width and Height of screen.
        @param pygame.sprite chomp - Pygame sprite object, player character.
        @param object sound - Sound Object for playing sfx.
        """

        # Animation clock
        self.animation = pygame.time.get_ticks()

        # Draw the level
        x = 0
        i = 0
        for i in self.tiles:


            if i['tile']:
                tile = i['tile'] - 1

                # Tiles with animation
                if i['animation']:
                    if not i['collide'] or not i['ani_collide']:
                        tile = tile + (math.floor(self.animation / (1000 / self.ani_framerate) ) % (i['animation'] - tile))
                    else:
                        for y in range(len(self.collide_animation)):
                            if self.collide_animation[y][0] == x and self.collide_animation[y][1] > math.floor( ((self.animation - self.collide_animation[y][3]) / (1000 / self.ani_framerate) ) / self.collide_animation[y][1]):
                                tile = tile + math.floor( ((self.animation - self.collide_animation[y][3]) / (1000 / self.ani_framerate) ) / self.collide_animation[y][1])
                                self.collide_animation[y][2] += 1

                tile_frame_x = tile % (self.tile_image_size[0] / self.tilesize[0])
                tile_frame_y = math.floor(tile / (self.tile_image_size[0] / self.tilesize[0]))

                if not i['orientation']: i['orientation'] = "original"
                screen.blit(self.tile_table[int(tile_frame_x)][int(tile_frame_y)][i['orientation']], (i['x'] + scroll[0], i['y'] + scroll[1] ) )

            # Collision with a tile
            if i['collide']:
                col = self.collision(chomp.colliderect,x)
                tilename = i['name']

                # If a collision happens...
                if col:

                    # If an animation was supposed to play when the collision happened...
                    if i['animation'] and i['ani_collide']:

                        # Check to make sure this animation isn't already queued..
                        add_to_collide = 1
                        for y in range(len(self.collide_animation)):

                            # If queued already reset the animation frame back to 0.
                            if self.collide_animation[y][0] == x:
                                if math.floor( ((self.animation - self.collide_animation[y][3]) / (1000 / self.ani_framerate) ) / self.collide_animation[y][1]) >= self.collide_animation[y][1]: 
                                    self.collide_animation[y][2] = 0
                                    self.collide_animation[y][3] = self.animation
                                add_to_collide = 0
                                break

                        # If not queued add it to the queue..
                        if add_to_collide:
                            self.collide_animation.append( [x, i['animation'] - tile, 0, self.animation] )


                    # If player hits a pusher...push!
                    if i['type'] == "pusher":
                    
                        if i['value']:
                            value = i['value'].split(",")
                        else: value = [0,0]
                        
                        # Wait till first frame of animation
                        if i['ani_collide'] and i['animation']:
                            for y in range(len(self.collide_animation)):
                                if self.collide_animation[y][0] == x:

                                    # Play collision SFX if provided.
                                    if i['collide_sfx']:
                                        sound.playSfx("sfx/" + i['collide_sfx'], 0)
                                            
                        # Play collision SFX if provided[This one plays when there is no collide animation].
                        elif i['collide_sfx']:
                            sound.playSfx("sfx/" + i['collide_sfx'], 0)                                            

                        # Do the pushing.
                        if value[1]: 
                            if (value[1] * -1) > 0 and not chomp.falling < -5: chomp.falling = int(value[1]) * -1
                        if value[0] and abs(chomp.speed) < abs(int(value[0])): chomp.speed = int(value[0])                            
                            
                    # If player hits the end of the level...
                    elif i['type'] == "goal":
                        self.state = 1     # Set level state to win.

                    # Any other collision should just be treated like a wall or floor collision...
                    else:
                        tilerect = pygame.Rect(i['x'],i['y'],self.tilesize[0],self.tilesize[1])
                        offset = [chomp.colliderect.x - tilerect.x, chomp.colliderect.y - tilerect.y]

                        # Check for horizontal collision...
                        if abs(offset[1]) <  self.tilesize[1] / 2:
                            if offset[0] >  self.tilesize[0] / 2: chomp.pos[0] = tilerect.x + self.tilesize[0]
                            elif offset[0] <=  self.tilesize[0] / 2: chomp.pos[0] = tilerect.x - self.tilesize[0]
                            chomp.speed = 0

                        # Check for vertical collision.
                        if abs(offset[0]) < self.tilesize[0] / 2:
                            if offset[1] > 0:
                                chomp.pos[1] = tilerect.y + self.tilesize[1]
                                if chomp.falling > 0: chomp.falling = 0
                            elif offset[1] <= 0:
                                chomp.pos[1] = tilerect.y -  self.tilesize[1] + 1
                                if chomp.falling > 0: chomp.falling = 0
                                # Disable chomp's ability to move on the ground
                                chomp.moveok = 0


            x += 1

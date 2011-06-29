import pygame, math, sys, os, iniget, dialog, imagehelper

# Image Helper Object
imghelp = imagehelper.imageHelper()

# Attempt to load Android modules.
try:
    import android, android_mixer
except ImportError:
    android = None
    
TILE_SIZE = [32,32]    

class Menu(object):
    def __init__(self, screen, sound, clock):

        # Dialog
        self.dialog = dialog.Dialog(screen)
        
        # Scroll Arrows
        scrollarrows = pygame.image.load("gfx/scroll_arrows.png").convert_alpha()
        image_width, image_height = scrollarrows.get_size()
        tile_image_size = [image_width,image_height]
        self.scrollarrows = imghelp.makeTiles(scrollarrows, TILE_SIZE)    
        
        # Load font
        self.font = pygame.font.Font("font/volter.ttf",18)
        self.titlefont = pygame.font.Font("font/volter2.ttf",28)
        
        # Load background
        self.background = pygame.image.load("gfx/menu_bg.png").convert()
        self.bg_rect = self.background.get_rect()  
        self.bgoffset = 0  
        
        # Get Sound Object
        self.sound = sound  
        
        # Get Screen Object
        self.screen = screen
        
        # Get Clock Object
        self.clock = clock
    
    def show(self):
        done = 0
        menu_end_state = 0
        
        # self.screen size
        size = self.screen.get_size()

        # Set Title self.screen Message
        self.font_data = [ "Tap to Start", 0, [0,0] ]
        if not android: self.font_data[0] = "Press Any Key to Start"
        self.font_data[1] = self.font.size(self.font_data[0])
                           
        # Load Title Logo
        self.title_logo_a = pygame.image.load("gfx/title_logo_layer1.png").convert_alpha()
        self.title_logo_b = pygame.image.load("gfx/title_logo_layer2.png").convert_alpha()

        # Size stuff to fit self.screen
        self.resizeTitle(size)
                
        title_logo_pos_a = self.tl_rect_a.x
        title_logo_pos_b = self.tl_rect_b.x
        title_logo_offset_a = self.tl_rect_a.x - size[0]
        title_logo_offset_b = self.tl_rect_a.x + size[0]
 
        # Play Menu Music
        self.sound.playSfx("sfx/danosongs.com-helium-hues.ogg", -1, 1)
        
        while not done:
            # Set frame rate to 30.
            self.clock.tick(30)
            events = pygame.event.get()

            # Android events
            if android:
                if android.check_pause():
                    android.wait_for_resume()


            rState = 2
            for event in events: # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop
                    rState = -1 # Set game state to -1(Quit)

                elif event.type == pygame.VIDEORESIZE:
                    self.resizeTitle(event.size)

                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    menu_end_state = 1
                    title_logo_pos_a = self.tl_rect_a.x - size[0]
                    title_logo_pos_b = self.tl_rect_b.x + size[0]       
                    title_logo_offset_a = self.tl_rect_a.x 
                    title_logo_offset_b = self.tl_rect_a.x              


            self.renderBg(size)
            
            # Title Logo offset
            if (title_logo_offset_a < title_logo_pos_a and not menu_end_state) or (title_logo_offset_a > title_logo_pos_a and menu_end_state):
                if menu_end_state: title_logo_offset_a -= 32
                else: title_logo_offset_a += 32
                
                self.tl_rect_a.x = title_logo_offset_a

            if (title_logo_offset_b > title_logo_pos_b and not menu_end_state) or (title_logo_offset_b < title_logo_pos_b and menu_end_state):
                if menu_end_state: title_logo_offset_b += 32
                else: title_logo_offset_b -= 32
                
                self.tl_rect_b.x = title_logo_offset_b
            elif menu_end_state: done = 1
                        
            
            # Title Logo
            self.screen.blit(self.title_logo_sized_b, self.tl_rect_b)
            self.screen.blit(self.title_logo_sized_a, self.tl_rect_a)     
            
            # Start Text
            
            self.screen.blit( self.font.render(self.font_data[0], 0, [0,0,0]), (self.font_data[2][0] + 2, self.font_data[2][1] + 2) )
            self.screen.blit( self.font.render(self.font_data[0], 0, [255,255,255]), (self.font_data[2][0], self.font_data[2][1]) )
            
            
            # Go ahead and update the self.screen with what we've drawn.
            pygame.display.flip()
        
        return rState
            
    def resizeTitle(self, size):
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        tl_rect_big = self.title_logo_a.get_rect()

        self.bgrows = 2
        self.bgcols = 2
        if size[1] > self.bg_rect.h: self.bgrows = int(math.ceil(size[1] / self.bg_rect.h) * 2) + 1
        if size[0] > self.bg_rect.w: self.bgcols = int(math.ceil(size[0] / self.bg_rect.w) * 2) + 1
        self.bg_rect.x = 0
        self.bg_rect.y = 0

        # Resize title logo, we're counting on the aspect ratio being 1:1.
        if size[0] > size[1]:
            self.title_logo_sized_a = pygame.transform.smoothscale(self.title_logo_a, (size[1], size[1]))
            self.title_logo_sized_b = pygame.transform.smoothscale(self.title_logo_b, (size[1], size[1]))
        else:
            self.title_logo_sized_a = pygame.transform.smoothscale(self.title_logo_a, (size[0], size[0]))
            self.title_logo_sized_b = pygame.transform.smoothscale(self.title_logo_b, (size[0], size[0]))

        self.tl_rect_a = self.title_logo_sized_a.get_rect()
        self.tl_rect_a.x = (size[0] / 2) - (self.tl_rect_a.w / 2)
        self.tl_rect_a.y = (size[1] / 2) - (self.tl_rect_a.h / 2)   
        
        self.tl_rect_b = self.title_logo_sized_b.get_rect()
        self.tl_rect_b.x = self.tl_rect_a.x
        self.tl_rect_b.y = self.tl_rect_a.y
        
        # Move Title Font...
        self.font_data[2] = [ (size[0] / 2) - (self.font_data[1][0] / 2), size[1] - (self.font_data[1][1] * 1.5) ]
        
    def renderBg(self, size):
        # Background
        self.bg_rect.x -= self.bg_rect.w - self.bgoffset
        self.bg_rect.y -= self.bg_rect.h - self.bgoffset
        
        for yy in xrange(self.bgrows):
            for xx in xrange(self.bgcols):
                # Start a new row
                if xx == 0 and yy > 0:
                    # Move the rectangle
                    self.bg_rect = self.bg_rect.move([-(self.bgcols -1 ) * self.bg_rect.w, self.bg_rect.h])
                # Continue a row
                if xx > 0:
                    # Move the rectangle
                    self.bg_rect = self.bg_rect.move([self.bg_rect.w, 0])
                
                self.screen.blit(self.background, self.bg_rect)
                
        self.bg_rect.x = 0
        self.bg_rect.y = 0     

        # Menu offset...makes the animation happen.
        self.bgoffset -= .5
        if self.bgoffset < -20: self.bgoffset = 0           

    def mapSelect(self):
        done = 0
           
        # self.screen size
        size = self.screen.get_size()
        
        # Vars to Use
        bgoffset = 0
        map_list_scroll = 0
        map_selected = 0
        
        # Static Vars
        LIST_SPACING = 32
        LIST_START_POS = 92
        
        # Map Select Arrow
        maparrow = pygame.image.load("gfx/map_select_arrow.png").convert_alpha()
        
        # Load Map List
        mapFiles = os.listdir("./map")
        mapList = []
        
        for i in mapFiles:
            ext = i.split(".")
            if ext[len(ext) - 1] == "map":
                ini = iniget.iniGet("./map/" + i)
                mapList.append([i, ini.get("pack", "name")])
                
        returnVal = -1
        
        # Get Sizes of Buttons...
        btnsize = self.dialog.getButtonSize("Next")
        btnsize2 = self.dialog.getButtonSize("Back")
        
        # Update BG Size
        self.resizeTitle(size)
        
        # Play Menu Music
        self.sound.playSfx("sfx/danosongs.com-helium-hues.ogg", -1, 1)
        
        while not done:
            # Set frame rate to 30.
            self.clock.tick(30)
            events = pygame.event.get()

            # Android events
            if android:
                if android.check_pause():
                    android.wait_for_resume()

            for event in events: # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE:
                    self.resizeTitle(event.size)
                    size = event.size
                    map_list_scroll = 0
                    map_selected = 0                    

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x = 0
                    for i in mapList:
                        fontSize = self.font.size(i[1])
                        rect = pygame.Rect(64, x * LIST_SPACING + LIST_START_POS - (map_list_scroll * LIST_SPACING), fontSize[0], fontSize[1])
                        if rect.collidepoint(event.pos[0], event.pos[1]):
                            map_selected = x
                        x += 1 
                        
                    if scroll_down_collide and scroll_down:
                        map_list_scroll += 1  
                        if map_list_scroll > cut_off: map_list_scroll = cut_off

                    if scroll_up_collide and map_list_scroll > 0:
                        map_list_scroll -= 1
 
                   
            # Render the background
            self.renderBg(size)
            
            # Title Text
            
            self.screen.blit( self.titlefont.render("Map Select", 0, [0,0,0]), (34,34) )
            self.screen.blit( self.titlefont.render("Map Select", 0, [255,179,0]), (32,32) )
            
            # Map List
            
            x = 0
            scroll_down = 0
            max_text_width = 0
            cut_off = 0
            for i in mapList:
                pos = [64, x * LIST_SPACING + LIST_START_POS - (map_list_scroll * LIST_SPACING) ]
                if self.font.size(i[1])[0] > max_text_width: max_text_width = self.font.size(i[1])[0]                
                if not pos[1] > size[1] - 64 and not pos[1] < 64:                    
                    self.screen.blit( self.font.render(i[1], 0, [0,0,0]), (pos[0] + 2, pos[1] + 2) )
                    self.screen.blit( self.font.render(i[1], 0, [255,255,255]), (pos[0], pos[1]) )
                else: 
                    scroll_down = 1
                    cut_off += 1
                x += 1
                
            # Render scroll down arrow
            if scroll_down and not map_list_scroll >= cut_off:
                pos = [max_text_width + 78, size[1] - 92]
                rect = pygame.Rect(pos[0], pos[1], TILE_SIZE[0], TILE_SIZE[1])
                mouse = pygame.mouse.get_pos()
                if not rect.collidepoint(mouse[0], mouse[1]):
                    self.screen.blit( self.scrollarrows[0][0], (pos[0], pos[1]) )
                    scroll_down_collide = 0
                else: 
                    self.screen.blit( self.scrollarrows[1][0], (pos[0], pos[1]) )
                    scroll_down_collide = 1
            else: scroll_down_collide = 0
                                
            # Render scroll up arrow
            if map_list_scroll > 0:
                pos = [max_text_width + 78, 64]
                rect = pygame.Rect(pos[0], pos[1], TILE_SIZE[0], TILE_SIZE[1])
                mouse = pygame.mouse.get_pos()
                if not rect.collidepoint(mouse[0], mouse[1]):
                    self.screen.blit( self.scrollarrows[0][1], (pos[0], pos[1]) )
                    scroll_up_collide = 0
                else: 
                    self.screen.blit( self.scrollarrows[1][1], (pos[0], pos[1]) )
                    scroll_up_collide = 1
            else: scroll_up_collide = 0
            
                        
            # Map Selected Arrow
            if map_selected < map_list_scroll: map_selected = map_list_scroll
            self.screen.blit(maparrow, ( 32, LIST_START_POS + (LIST_SPACING * map_selected) - (LIST_SPACING * map_list_scroll)   ) )
            
 
            # If next clicked load selected level
            if self.dialog.makeButton("Play", [ size[0] - btnsize[0] - (LIST_SPACING * 1.5) , size[1] - (LIST_SPACING * 1.5) ], size, events):
                returnVal = mapList[map_selected][0]
                done = 1

            # If back clicked
            #if self.dialog.makeButton("Back", [ size[0] - btnsize2[0] - btnsize[0] - (LIST_SPACING * 1.5) , size[1] - (LIST_SPACING * 1.5) ], size, self.screen, events):
            #    returnVal = 0
            #    done = 1
            if self.dialog.makeButton("Quit", [ size[0] - btnsize2[0] - btnsize[0] - (LIST_SPACING * 1.5) , size[1] - (LIST_SPACING * 1.5) ], size, events):
                pygame.quit()
                sys.exit()
            
            
            # Dialog Box
            self.dialog.drawBox(size, events)
                           
            # Go ahead and update the self.screen with what we've drawn.
            pygame.display.flip()     
                       
        return returnVal
    
    #def stageSelect(self):
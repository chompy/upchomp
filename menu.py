import pygame, math, os, iniget, dialog

try:
    import android, android_mixer
except ImportError:
    android = None

class Menu(object):
    def __init__(self):

        # Dialog
        self.dialog = dialog.Dialog()
    
        # Load font
        self.font = pygame.font.Font("font/volter.ttf",18)
        self.titlefont = pygame.font.Font("font/volter2.ttf",28)
        
        # Load background
        self.background = pygame.image.load("gfx/menu_bg.png").convert()
        self.bg_rect = self.background.get_rect()  
        self.bgoffset = 0     
          
    def show(self, screen, clock):
        done = 0
        menu_end_state = 0
        
        # Screen size
        size = screen.get_size()

        # Set Title Screen Message
        self.font_data = [ "Tap to Start", 0, [0,0] ]
        if not android: self.font_data[0] = "Press Any Key to Start"
        self.font_data[1] = self.font.size(self.font_data[0])
                           
        # Load Title Logo
        self.title_logo_a = pygame.image.load("gfx/title_logo_layer1.png").convert_alpha()
        self.title_logo_b = pygame.image.load("gfx/title_logo_layer2.png").convert_alpha()

        # Size stuff to fit screen
        self.resizeTitle(size, screen)
                
        title_logo_pos_a = self.tl_rect_a.x
        title_logo_pos_b = self.tl_rect_b.x
        title_logo_offset_a = self.tl_rect_a.x - size[0]
        title_logo_offset_b = self.tl_rect_a.x + size[0]
 
        while not done:
            # Set frame rate to 30.
            clock.tick(30)
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
                    self.resizeTitle(event.size, screen)

                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    menu_end_state = 1
                    title_logo_pos_a = self.tl_rect_a.x - size[0]
                    title_logo_pos_b = self.tl_rect_b.x + size[0]       
                    title_logo_offset_a = self.tl_rect_a.x 
                    title_logo_offset_b = self.tl_rect_a.x              


            self.renderBg(size, screen)
            
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
            screen.blit(self.title_logo_sized_b, self.tl_rect_b)
            screen.blit(self.title_logo_sized_a, self.tl_rect_a)     
            
            # Start Text
            
            screen.blit( self.font.render(self.font_data[0], 0, [0,0,0]), (self.font_data[2][0] + 2, self.font_data[2][1] + 2) )
            screen.blit( self.font.render(self.font_data[0], 0, [255,255,255]), (self.font_data[2][0], self.font_data[2][1]) )
            
            
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
        
        return rState
            
    def resizeTitle(self, size, screen):
        screen = pygame.display.set_mode(size, pygame.RESIZABLE)
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
        
    def renderBg(self, size, screen):
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
                
                screen.blit(self.background, self.bg_rect)
                
        self.bg_rect.x = 0
        self.bg_rect.y = 0     

        # Menu offset...makes the animation happen.
        self.bgoffset -= .5
        if self.bgoffset < -20: self.bgoffset = 0           

    def mapSelect(self, screen, clock):
        done = 0
           
        # Screen size
        size = screen.get_size()
        
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
        
        while not done:
            # Set frame rate to 30.
            clock.tick(30)
            events = pygame.event.get()

            # Android events
            if android:
                if android.check_pause():
                    android.wait_for_resume()

            for event in events: # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE:
                    self.resizeTitle(event.size, screen)
                    size = event.size

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x = 0
                    for i in mapList:
                        fontSize = self.font.size(i[1])
                        rect = pygame.Rect(64, x * LIST_SPACING + LIST_START_POS, fontSize[0], fontSize[1])
                        if rect.collidepoint(event.pos[0], event.pos[1]):
                            map_selected = x
                        x += 1   
                   
            # Render the background
            
            self.renderBg(size, screen)
            
            # Title Text
            
            screen.blit( self.titlefont.render("Map Select", 0, [0,0,0]), (34,34) )
            screen.blit( self.titlefont.render("Map Select", 0, [255,179,0]), (32,32) )
            
            # Map List
            
            x = 0
            for i in mapList:
                screen.blit( self.font.render(i[1], 0, [0,0,0]), (66, x * LIST_SPACING + LIST_START_POS + 2) )
                screen.blit( self.font.render(i[1], 0, [255,255,255]), (64, x * LIST_SPACING + LIST_START_POS) )
                x += 1
            
            # Map Selected Arrow
            screen.blit(maparrow, ( 32, LIST_START_POS + (LIST_SPACING * map_selected) - (LIST_SPACING * map_list_scroll)   ) )
            
 
            # If next clicked load selected level
            if self.dialog.makeButton("Next", [ size[0] - btnsize[0] - (LIST_SPACING * 1.5) , size[1] - (LIST_SPACING * 1.5) ], size, screen, events):
                returnVal = mapList[map_selected][0]
                done = 1

            # If back clicked
            if self.dialog.makeButton("Back", [ size[0] - btnsize2[0] - btnsize[0] - (LIST_SPACING * 1.5) , size[1] - (LIST_SPACING * 1.5) ], size, screen, events):
                returnVal = 0
                done = 1
                        
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()     
            
        return returnVal
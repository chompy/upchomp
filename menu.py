import pygame, math

try:
    import android, android_mixer
except ImportError:
    android = None

class Menu(object):
    def __init__(self):

        # Load font
        self.font = pygame.font.Font("font/volter.ttf",18)
          
    def show(self, screen, clock):
        done = 0
        menu_end_state = 0
        
        # Screen size
        size = screen.get_size()

        # Load background
        self.background = pygame.image.load("gfx/menu_bg.png").convert()
        self.bg_rect = self.background.get_rect()

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
 

        bgoffset = 0
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


            # Background
            self.bg_rect.x -= self.bg_rect.w - bgoffset
            self.bg_rect.y -= self.bg_rect.h - bgoffset
            
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
            bgoffset -= .5
            if bgoffset < -20: bgoffset = 0

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
            
    def resizeTitle(self, size, screen,):
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
        

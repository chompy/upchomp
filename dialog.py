import pygame, math, imagehelper

# Image Helper Object
imghelp = imagehelper.imageHelper()

# Constants
TILE_SIZE = [32,32]

class Dialog(object):
    
    def __init__(self, screen, sound):
    
        # Load the dialog tiles...             
        image = pygame.image.load("gfx/dialog_box.png").convert_alpha()
        image_width, image_height = image.get_size()
        self.tile_image_size = [image_width,image_height]
        self.tile_table = imghelp.makeTiles(image, TILE_SIZE)
                  
        # Load font
        self.font = pygame.font.Font("font/volter.ttf",18)
        self.text = ""   
        self.title_color = [255, 179, 0]  
        self.text_color = [255, 255, 255]  
        
        # Box vars
        self.showbox = 0
        self.buttonstate = { 'close_over' : 0 }
        
        # Get Screen Object
        self.screen = screen
        
        # Get Sound Object
        self.sound = sound
                
    def setMessageBox(self, size, message, title="", buttons=[]):

        self.text = message
        self.title = title
        self.button = buttons
        
        # Set buttons state
        for i in range(len(self.button)):
            self.buttonstate[i] = 0            
        
        # Amount to push text if there is a title...
        self.text_push = 1
        if self.title: self.text_push = 1.5
        
        self.showbox = 1
        
        self.calculateSize(size)


    def closeMessageBox(self):
        self.showbox = 0
        
    def calculateSize(self,size):
        
        # Variables to save calculations to...
        self.text_lines = []

        max_box_size = [size[0] - (TILE_SIZE[0] * 5), size[1] - (TILE_SIZE[1] * 4)]
        
        # Determine text size, handle wordwrapping, etc
        text_arr = self.text.split(" ")
        text_str = ""
        box_text_size = [0,0]
        
        self.final_text = []
        
        # Get text size, determine how many lines we need...
        if self.font.size(self.text) > max_box_size[0]:
            for i in range(0, len(text_arr)):
                text_str = text_str + " " + text_arr[i]  
                 
                if i < len(text_arr) - 1:
                    text_size = self.font.size(text_str + text_arr[i + 1])                    
                                       
                    if text_size[0] > max_box_size[0]:
                        self.final_text.append(text_str[1:])
                        
                        # Get the width of the widest line.
                        if self.font.size(text_str[1:])[0] > box_text_size[0]: box_text_size[0] = self.font.size(text_str[1:])[0]
                        
                        text_str = ""
                else: 
                    if self.font.size(text_str[1:])[0] > box_text_size[0]: box_text_size[0] = self.font.size(text_str[1:])[0]
                    self.final_text.append(text_str[1:])
               
        box_text_size[1] = len(self.final_text) * self.font.get_linesize()     

        # Size of box with text and padding.
        if self.button: btn_space_add = 2
        else: btn_space_add = 0
                
        self.boxsize = [box_text_size[0] + TILE_SIZE[0], box_text_size[1] + (TILE_SIZE[1] * self.text_push) + (TILE_SIZE[1] * btn_space_add)]
        self.boxrange = [math.floor(self.boxsize[0] / TILE_SIZE[0]) + 2, math.floor(self.boxsize[1] / TILE_SIZE[1]) + 1]   
               
        # Get Button Size
        button_width = 0
        for i in range(len(self.button)):
            button_text_size = self.font.size(self.button[i][0])
            button_tile_width = int(math.floor(button_text_size[0] / TILE_SIZE[0])) + 3
            button_width += button_tile_width * TILE_SIZE[0]
            
        if button_width > self.boxsize[0]: 
            self.boxsize[0] = button_width
            self.boxrange[0] = math.floor(button_width / TILE_SIZE[0]) + 2
                            
    def drawBox(self, size, events):
        if not self.showbox: return 0
        
        for y in range(0, int(self.boxrange[1])):
            for x in range(0, int(self.boxrange[0])):
                # Determine which block to use...
                pos = [ ((size[0] / 2) - (self.boxsize[0] / 2)) + (x * TILE_SIZE[0]) - TILE_SIZE[0] , ((size[1] - self.boxsize[1]) / 2) + (y * TILE_SIZE[1])  ]
                
                # Top left corner.
                if y == 0 and x == 0:
                    self.screen.blit(self.tile_table[0][0], (pos[0],pos[1]) )
                # Top Middle
                elif y == 0 and x > 0 and x < self.boxrange[0] - 1:
                    self.screen.blit(self.tile_table[1][0], (pos[0],pos[1]) )
                # Top Right corner
                elif y == 0 and x == self.boxrange[0] - 1:
                    close_btn = pygame.Rect(pos[0],pos[1], TILE_SIZE[0], TILE_SIZE[1])
                    if not self.buttonstate['close_over']:
                        self.screen.blit(self.tile_table[2][0], (pos[0],pos[1]) )
                    else:
                        self.screen.blit(self.tile_table[3][2], (pos[0],pos[1]) )
                        
                # Bottom left corner.
                elif y == self.boxrange[1] - 1 and x == 0:
                    self.screen.blit(self.tile_table[0][2], (pos[0],pos[1]) )
                # Bottom Middle
                elif y == self.boxrange[1] - 1 and x > 0 and x < self.boxrange[0] - 1:
                    self.screen.blit(self.tile_table[1][2], (pos[0],pos[1]) )
                # Bottom Right corner
                elif y == self.boxrange[1] - 1 and x == self.boxrange[0] - 1:
                    self.screen.blit(self.tile_table[2][2], (pos[0],pos[1]) )
                # Center left corner.
                elif y < self.boxrange[1] - 1 and x == 0:
                    self.screen.blit(self.tile_table[0][1], (pos[0],pos[1]) )
                # Center Right corner
                elif y < self.boxrange[1] - 1 and x == self.boxrange[0] - 1:
                    self.screen.blit(self.tile_table[2][1], (pos[0],pos[1]) )                    
                # Center Middle
                else:
                    self.screen.blit(self.tile_table[1][1], (pos[0],pos[1]) )    
                    
        # Display Text
        if self.title:
            #self.font.set_bold(1)
            self.font.set_underline(1)
            self.screen.blit(self.font.render(self.title, 0, self.title_color), ( ((size[0] - self.boxsize[0]) / 2), ((size[1] - self.boxsize[1]) / 2) + TILE_SIZE[1] / 2 ))
        
        self.font.set_bold(0)
        self.font.set_underline(0)
        for i in range(len(self.final_text)):
            self.screen.blit(self.font.render(self.final_text[i], 0, self.text_color), ( ((size[0] - self.boxsize[0]) / 2), ((size[1] - self.boxsize[1]) / 2) + (i * self.font.get_linesize()) + TILE_SIZE[1] * self.text_push))
                   
        # Display Buttons
        button_start_x = 0
        button_positions = []
        for i in range(len(self.button)):
            button_text_size = self.font.size(self.button[i][0])
            button_tile_width = int(math.floor(button_text_size[0] / TILE_SIZE[0])) + 2
            
            for x in range(0, button_tile_width):
                pos = [button_start_x + ((size[0] - self.boxsize[0]) / 2) + (x * TILE_SIZE[0]) , ((size[1] - self.boxsize[1]) / 2) + ((self.text_push / 1.5) * TILE_SIZE[1]) + (self.font.get_linesize() * len(self.final_text)) + TILE_SIZE[1] ]
               
                if x == 0:
                    button_positions.append(pos) # Button position array for button rect
                    self.screen.blit(self.tile_table[3][self.buttonstate[i]], (pos[0],pos[1]) )
                elif x > 0 and x < button_tile_width - 1:
                    self.screen.blit(self.tile_table[4][self.buttonstate[i]], (pos[0],pos[1]) )     
                elif x == button_tile_width - 1:                           
                    self.screen.blit(self.tile_table[5][self.buttonstate[i]], (pos[0],pos[1]) )     
                   
            # Display Button Text
            #self.font.set_bold(1)                   
            self.screen.blit(self.font.render(self.button[i][0],0,self.title_color), ( button_start_x + ((size[0] - self.boxsize[0]) / 2) + (TILE_SIZE[0] / 2) + (button_tile_width / 2), ((size[1] - self.boxsize[1]) / 2) + ((self.text_push / 1.5) * TILE_SIZE[1]) + (len(self.final_text) * self.font.get_linesize())  + TILE_SIZE[1] + (TILE_SIZE[1] / 2) - (self.font.get_linesize() / 2) ))
            
            button_start_x = (int(math.floor(button_text_size[0] / TILE_SIZE[0])) + 2) * TILE_SIZE[0]
               
        # Button events
        for event in events:
            self.buttonstate['close_over'] = 0
            for i in range(len(self.buttonstate)):
                self.buttonstate[i] = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_btn.collidepoint(event.pos[0], event.pos[1]):
                    self.sound.playSfx("sfx/button.wav",0)
                    self.closeMessageBox()                    
                    return -1 
                for i in range(len(self.button)):
                    button_text_size = self.font.size(self.button[i][0])
                    button_tile_width = int(math.floor(button_text_size[0] / TILE_SIZE[0])) + 2
                    button_rect = pygame.Rect(button_positions[i][0], button_positions[i][1], button_tile_width * TILE_SIZE[0], TILE_SIZE[1])

                    # If button click initiate passed function
                    if button_rect.collidepoint(event.pos[0], event.pos[1]):
                        self.sound.playSfx("sfx/button.wav",0)
                        self.button[i][1]()
                        self.closeMessageBox() 
                                            
            elif event.type == pygame.MOUSEMOTION:
                # Change rollover state when mousing over the buttons
                if close_btn.collidepoint(event.pos[0], event.pos[1]): 
                    self.buttonstate['close_over'] = 1
                for i in range(len(self.button)):
                    button_text_size = self.font.size(self.button[i][0])
                    button_tile_width = int(math.floor(button_text_size[0] / TILE_SIZE[0])) + 2
                    button_rect = pygame.Rect(button_positions[i][0], button_positions[i][1], button_tile_width * TILE_SIZE[0], TILE_SIZE[1])

                    if button_rect.collidepoint(event.pos[0], event.pos[1]):
                        self.buttonstate[i] = 1
                        
            # If self.screen size changes
            elif event.type == pygame.VIDEORESIZE:
                self.calculateSize(event.size)
                               
        return 1
        
    def makeButton(self, text, btnpos, size, events):

        """
        Makes a button that can be placed anywhere.
        """
    
        button_text_size = self.font.size(text)
        button_tile_width = int(math.floor(button_text_size[0] / TILE_SIZE[0])) + 2
        rect = pygame.Rect(btnpos[0], btnpos[1], button_tile_width * TILE_SIZE[0], TILE_SIZE[1])
        
        btn_state = 0
        btn_click = 0
        
        # Get mouse pos to see if roll over
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos[0], mouse_pos[1]): 
            btn_state = 1
                       
            # See if mouse button was clicked
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    btn_click = 1
                    self.sound.playSfx("sfx/button.wav",0)
        
        for x in range(0, button_tile_width):
            pos = [btnpos[0] + (x * TILE_SIZE[0]) + (TILE_SIZE[0] / 2), btnpos[1]]
           
            if x == 0:
                self.screen.blit(self.tile_table[3][btn_state], (pos[0],pos[1]) )
            elif x > 0 and x < button_tile_width - 1:
                self.screen.blit(self.tile_table[4][btn_state], (pos[0],pos[1]) )     
            elif x == button_tile_width - 1:                           
                self.screen.blit(self.tile_table[5][btn_state], (pos[0],pos[1]) )     
               
        # Display Button Text
        #self.font.set_bold(1)                   
        self.screen.blit(self.font.render(text, 0, self.title_color), ( btnpos[0] + TILE_SIZE[0] + (button_tile_width / 2), btnpos[1] + ((TILE_SIZE[1] / 2) - (self.font.get_linesize() / 2)) ))
        
        return btn_click
        
    def getButtonSize(self, text):
        button_text_size = self.font.size(text)
        button_tile_width = int(math.floor(button_text_size[0] / TILE_SIZE[0])) + 2
        return [button_tile_width * TILE_SIZE[0], TILE_SIZE[1]]
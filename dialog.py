import pygame, math

TILE_SIZE = [32,32]

class Dialog(object):
    
    def __init__(self):
    
        # Load the dialog tiles...             
        image = pygame.image.load("gfx/dialog_box.png").convert_alpha()
        image_width, image_height = image.get_size()
        self.tile_image_size = [image_width,image_height]
        self.tile_table = []
        
        for tile_x in range(0, image_width/TILE_SIZE[0]):
            line = []
            self.tile_table.append(line)
            for tile_y in range(0, image_height/TILE_SIZE[1]):
                rect = (tile_x*TILE_SIZE[0], tile_y*TILE_SIZE[1], TILE_SIZE[0], TILE_SIZE[1])
                line.append(image.subsurface(rect))
          
        # Load font
        self.font = pygame.font.Font("font/volter.ttf",18)
        self.text = ""   
        self.title_color = [255, 179, 0]  
        self.text_color = [255, 255, 255]  
        
        # Box vars
        self.showbox = 0
        self.buttonstate = { 'close_over' : 0 }
                
    def setMessageBox(self,size,message,title="",buttons=[]):
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


        max_box_size = [size[0] - (TILE_SIZE[0] * 4), size[1] - (TILE_SIZE[1] * 4)]
        
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
                        if self.font.size(text_str)[0] > box_text_size[0]: box_text_size[0] = self.font.size(text_str)[0]
                        
                        text_str = ""
                else: self.final_text.append(text_str[1:])
               
        box_text_size[1] = len(self.final_text) * self.font.get_linesize()     

        # Size of box with text and padding.
        self.boxsize = [box_text_size[0] + TILE_SIZE[0], box_text_size[1] + TILE_SIZE[1] * self.text_push]   
        
        if self.button: btn_space_add = 1
             
        self.boxrange = [math.floor(self.boxsize[0] / TILE_SIZE[0]) + 1, math.floor(self.boxsize[1] / TILE_SIZE[1]) + 1 + btn_space_add]

                            
    def drawBox(self,screen,size):
        if not self.showbox: return 0
        
        for y in range(0, int(self.boxrange[1])):
            for x in range(0, int(self.boxrange[0])):
                # Determine which block to use...
                pos = [ ((size[0] - self.boxsize[0]) / 2) + (x * TILE_SIZE[0]) - (TILE_SIZE[0] / 2) , ((size[1] - self.boxsize[1]) / 2) + (y * TILE_SIZE[1])  ]
                
                # Top left corner.
                if y == 0 and x == 0:
                    screen.blit(self.tile_table[0][0], (pos[0],pos[1]) )
                # Top Middle
                elif y == 0 and x > 0 and x < self.boxrange[0] - 1:
                    screen.blit(self.tile_table[1][0], (pos[0],pos[1]) )
                # Top Right corner
                elif y == 0 and x == self.boxrange[0] - 1:
                    close_btn = pygame.Rect(pos[0],pos[1], TILE_SIZE[0], TILE_SIZE[1])
                    if not self.buttonstate['close_over']:
                        screen.blit(self.tile_table[2][0], (pos[0],pos[1]) )
                    else:
                        screen.blit(self.tile_table[3][2], (pos[0],pos[1]) )
                        
                # Bottom left corner.
                elif y == self.boxrange[1] - 1 and x == 0:
                    screen.blit(self.tile_table[0][2], (pos[0],pos[1]) )
                # Bottom Middle
                elif y == self.boxrange[1] - 1 and x > 0 and x < self.boxrange[0] - 1:
                    screen.blit(self.tile_table[1][2], (pos[0],pos[1]) )
                # Bottom Right corner
                elif y == self.boxrange[1] - 1 and x == self.boxrange[0] - 1:
                    screen.blit(self.tile_table[2][2], (pos[0],pos[1]) )
                # Center left corner.
                elif y < self.boxrange[1] - 1 and x == 0:
                    screen.blit(self.tile_table[0][1], (pos[0],pos[1]) )
                # Center Right corner
                elif y < self.boxrange[1] - 1 and x == self.boxrange[0] - 1:
                    screen.blit(self.tile_table[2][1], (pos[0],pos[1]) )                    
                # Center Middle
                else:
                    screen.blit(self.tile_table[1][1], (pos[0],pos[1]) )    
                    
        # Display Text
        if self.title:
            self.font.set_bold(1)
            self.font.set_underline(1)
            screen.blit(self.font.render(self.title, 1, self.title_color), ( ((size[0] - self.boxsize[0]) / 2) + (TILE_SIZE[0] / 2), ((size[1] - self.boxsize[1]) / 2) + TILE_SIZE[1] / 2 ))
        
        self.font.set_bold(0)
        self.font.set_underline(0)
        for i in range(len(self.final_text)):
            screen.blit(self.font.render(self.final_text[i], 1, self.text_color), ( ((size[0] - self.boxsize[0]) / 2) + (TILE_SIZE[0] / 2), ((size[1] - self.boxsize[1]) / 2) + (i * self.font.get_linesize()) + TILE_SIZE[1] * self.text_push))

       
        # Display Buttons
        button_start_x = 0

        for i in range(len(self.button)):
            button_text_size = self.font.size(self.button[i][0])
            button_tile_width = int(math.floor(button_text_size[0] / TILE_SIZE[0])) + 2
                        
            for x in range(0, button_tile_width):
                pos = [button_start_x + ((size[0] - self.boxsize[0]) / 2) + (x * TILE_SIZE[0]) + (TILE_SIZE[0] / 2), (len(self.final_text) + 2 + (self.text_push / 1.5)) * TILE_SIZE[1] ]
                if x == 0:
                    screen.blit(self.tile_table[3][self.buttonstate[i]], (pos[0],pos[1]) )
                elif x > 0 and x < button_tile_width - 1:
                    screen.blit(self.tile_table[4][self.buttonstate[i]], (pos[0],pos[1]) )     
                elif x == button_tile_width - 1:                           
                    screen.blit(self.tile_table[5][self.buttonstate[i]], (pos[0],pos[1]) )     
                   
            # Display Button Text
            self.font.set_bold(1)                   
            screen.blit(self.font.render(self.button[i][0],1,self.title_color), ( button_start_x + ((size[0] - self.boxsize[0]) / 2) + TILE_SIZE[0] + (button_tile_width / 2), (len(self.final_text) + 2 + (self.text_push / 1.5)) * TILE_SIZE[1]  + (TILE_SIZE[1] / 2) - (self.font.get_linesize() / 2) ))
            
            button_start_x = (int(math.floor(button_text_size[0] / TILE_SIZE[0])) + 2) * TILE_SIZE[0]
               
        # Close event
        for event in pygame.event.get():
            self.buttonstate['close_over'] = 0
            for i in range(len(self.buttonstate)):
                self.buttonstate[i] = 0
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if close_btn.collidepoint(event.pos[0], event.pos[1]):
                    self.closeMessageBox() 
                    
            elif event.type == pygame.MOUSEMOTION:
                if close_btn.collidepoint(event.pos[0], event.pos[1]): 
                    self.buttonstate['close_over'] = 1
                for i in range(len(self.button)):
                    button_text_size = self.font.size(self.button[i][0])
                    button_tile_width = int(math.floor(button_text_size[0] / TILE_SIZE[0])) + 2
                    button_rect = pygame.Rect(0, i * TILE_SIZE[1], button_tile_width * TILE_SIZE[0], TILE_SIZE[1])

                    if button_rect.collidepoint(event.pos[0], event.pos[1]):
                        self.buttonstate[i] = 1
                    
            
        return 1
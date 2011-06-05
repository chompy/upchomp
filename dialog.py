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
                
    def setMessageBox(self,message,title=""):
        self.text = message
        self.title = title
        
        # Amount to push text if there is a title...
        self.text_push = 1
        if self.title: self.text_push = 1.5
        
        self.showbox = 1

    def closeMessageBox(self):
        self.showbox = 0
                        
    def drawBox(self,screen,size):
        if not self.showbox: return 0
        
        max_box_size = [size[0] - (TILE_SIZE[0] * 4), size[1] - (TILE_SIZE[1] * 4)]
        
        # Determine text size, handle wordwrapping, etc
        text_arr = self.text.split(" ")
        text_str = ""
        box_text_size = [0,0]
        
        final_text = []
        
        if self.font.size(self.text) > max_box_size[0]:
            for i in range(0, len(text_arr)):
                text_str = text_str + " " + text_arr[i]  
                 
                if i < len(text_arr) - 1:
                    text_size = self.font.size(text_str + text_arr[i + 1])
                    
                    # Get the width of the widest line.
                    if text_size[0] > box_text_size[0]: box_text_size[0] = text_size[0]
                                       
                    if text_size[0] > max_box_size[0]:
                        final_text.append(text_str[1:])
                        text_str = ""
                else: final_text.append(text_str[1:])
                
        box_text_size[1] = len(final_text) * self.font.get_linesize()     

        boxsize = [box_text_size[0] + TILE_SIZE[0], box_text_size[1] + TILE_SIZE[1] * self.text_push]        
        boxrange = [math.floor(boxsize[0] / TILE_SIZE[0]) + 1, math.floor(boxsize[1] / TILE_SIZE[1]) + 1]
        for y in range(0, int(boxrange[1])):
            for x in range(0, int(boxrange[0])):
                # Determine which block to use...
                pos = [ ((size[0] - boxsize[0]) / 2) + (x * TILE_SIZE[0]) , ((size[1] - boxsize[1]) / 2) + (y * TILE_SIZE[1])  ]
                
                # Top left corner.
                if y == 0 and x == 0:
                    screen.blit(self.tile_table[0][0], (pos[0],pos[1]) )
                # Top Middle
                elif y == 0 and x > 0 and x < boxrange[0] - 1:
                    screen.blit(self.tile_table[1][0], (pos[0],pos[1]) )
                # Top Right corner
                elif y == 0 and x == boxrange[0] - 1:
                    close_btn = pygame.Rect(pos[0],pos[1], TILE_SIZE[0], TILE_SIZE[1])
                    if not self.buttonstate['close_over']:
                        screen.blit(self.tile_table[2][0], (pos[0],pos[1]) )
                    else:
                        screen.blit(self.tile_table[3][1], (pos[0],pos[1]) )
                        
                # Bottom left corner.
                elif y == boxrange[1] - 1 and x == 0:
                    screen.blit(self.tile_table[0][2], (pos[0],pos[1]) )
                # Bottom Middle
                elif y == boxrange[1] - 1 and x > 0 and x < boxrange[0] - 1:
                    screen.blit(self.tile_table[1][2], (pos[0],pos[1]) )
                # Bottom Right corner
                elif y == boxrange[1] - 1 and x == boxrange[0] - 1:
                    screen.blit(self.tile_table[2][2], (pos[0],pos[1]) )
                # Center left corner.
                elif y < boxrange[1] - 1 and x == 0:
                    screen.blit(self.tile_table[0][1], (pos[0],pos[1]) )
                # Center Right corner
                elif y < boxrange[1] - 1 and x == boxrange[0] - 1:
                    screen.blit(self.tile_table[2][1], (pos[0],pos[1]) )                    
                # Center Middle
                else:
                    screen.blit(self.tile_table[1][1], (pos[0],pos[1]) )
                    
        # Display Text
        if self.title:
            self.font.set_bold(1)
            self.font.set_underline(1)
            screen.blit(self.font.render(self.title, 1, self.title_color), ( ((size[0] - boxsize[0]) / 2) + (TILE_SIZE[0] / 2), ((size[1] - boxsize[1]) / 2) + TILE_SIZE[1] / 2 ))
        
        self.font.set_bold(0)
        self.font.set_underline(0)
        for i in range(len(final_text)):
            screen.blit(self.font.render(final_text[i], 1, self.text_color), ( ((size[0] - boxsize[0]) / 2) + (TILE_SIZE[0] / 2), ((size[1] - boxsize[1]) / 2) + (i * self.font.get_linesize()) + TILE_SIZE[1] * self.text_push))

            
        # Close event
        for event in pygame.event.get():
            self.buttonstate['close_over'] = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_btn.collidepoint(event.pos[0], event.pos[1]):
                    self.closeMessageBox() 
            elif event.type == pygame.MOUSEMOTION:
                if close_btn.collidepoint(event.pos[0], event.pos[1]): 
                    self.buttonstate['close_over'] = 1
                    
            
        return 1
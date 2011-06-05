
import pygame, math, chompy, gamemap, dialog

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)

class Game(object):

    def __init__(self):
 
        pygame.init()

        # Screen/Dialog stuff
        size=[800,480]
        self.screen=pygame.display.set_mode(size)
        pygame.display.set_caption("UpChomp")
 
        # Used to manage how fast the screen updates
        self.clock=pygame.time.Clock()

        # Sprites
        self.all_sprites_list = pygame.sprite.RenderPlain()

        # Init da Chomp
        self.chomp = chompy.Chompy()
        self.all_sprites_list.add(self.chomp)

        

        # Load a level...
        self.startLevel()
        
    def startLevel(self):
       
        # Screen size
        size = self.screen.get_size()
        
        # Init da level
        self.level = gamemap.Gamemap("map1.map")

        # Place character in level
        pos = self.level.parser.get("level","startpos").split(",")
        self.chomp.pos[0] = int(pos[0]) * self.level.tilesize[0]
        self.chomp.pos[1] = int(pos[1]) * self.level.tilesize[1]
        self.chomp.colliderect.x = self.chomp.pos[0]
        self.chomp.colliderect.y = self.chomp.pos[1]        
        scroll = [(size[0] / 2) - self.chomp.pos[0] , (size[1] / 2) - self.chomp.pos[1] ]       
                        
        # If player is moving...
        move = 0
        
        # Load Dialog box
        dlogbox = dialog.Dialog()
        dlogbox.setMessageBox(size,"The first level! Should be easy, just play and win!","Test Level 1", [['Play!',dlogbox.closeMessageBox],['Quit',pygame.quit]] )
        
        #Loop until the user clicks the close button.
        done=False
                    
        # -------- Main Program Loop -----------
        while done==False:
        
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop
                
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    move = event.pos[0]
        
                elif event.type == pygame.MOUSEBUTTONUP: 
                    move = 0
                    
                elif event.type == pygame.MOUSEMOTION and move:
                    move = event.pos[0]
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == 292: pygame.display.toggle_fullscreen()
         
             
            lscroll = scroll
            scroll = [(size[0] / 2) - self.chomp.pos[0] , (size[1] / 2) - self.chomp.pos[1] ]        
        
            
            # Draw the background
            self.screen.fill(white) 
            self.level.drawBackground(self.screen,scroll)
          
            # Draw tiles and handle tile collision with player
            self.level.updateTiles(self.screen,scroll,self.clock,self.chomp)
                  
            # Limit to 30 frames per second
            self.clock.tick(30)
               
            # If a dialog box isn't up...
            if not dlogbox.drawBox(self.screen,size):
                # Draw Sprites
                self.all_sprites_list.draw(self.screen)  
                # Update Chomp Movement
                self.chomp.update(scroll,move,size)       
                
            
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
             
        # Be IDLE friendly. If you forget this line, the program will 'hang'
        # on exit.
        pygame.quit ()
 
Game()
import pygame, math, chompy, gamemap, dialog, hud, transition, sys

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)

class Game(object):

    def __init__(self):
    
        """Inits the game."""
 
        pygame.init()

        # Screen/Dialog stuff
        size=[800,480]
        self.screen=pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.set_caption("UpChomp")
 
        # Used to manage how fast the screen updates
        self.clock=pygame.time.Clock()

        # Sprites
        self.all_sprites_list = pygame.sprite.RenderPlain()

        # Init da Chomp
        self.chomp = chompy.Chompy()
        self.all_sprites_list.add(self.chomp)   

        # Make a dialog object.
        self.dlogbox = dialog.Dialog()
        
        # Setup Hud
        self.hud = hud.Hud()
        
        # Setup Transition
        self.transition = transition.Transition()
        
        # Load a level...
        self.startLevel()
        
    def levelTransition(self):
        size = self.screen.get_size()
        self.transition.verticalSwipe(size)
        self.dlogbox.closeMessageBox()
                
        
    def startLevel(self):
    
        """Loads a level and begins gameplay."""
        
        # Reset Chompy
        self.chomp.reset()
        
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
        
        # Level time
        start_time = pygame.time.get_ticks()
        time = 0
        
        # Load Dialog box
        self.dlogbox.setMessageBox(size,self.level.parser.get("level","desc"), self.level.parser.get("level","name"), [['Play!',self.dlogbox.closeMessageBox],['Quit',sys.exit]] )
        
        #Loop until the user clicks the close button.
        self.done=False
                    
        # -------- Main Program Loop -----------
        while self.done==False:
            events = pygame.event.get()
            for event in events: # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.done=True # Flag that we are done so we exit this loop
                
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    move = event.pos[0]
        
                elif event.type == pygame.MOUSEBUTTONUP: 
                    move = 0
                    
                elif event.type == pygame.MOUSEMOTION and move:
                    move = event.pos[0]
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == 292: pygame.display.toggle_fullscreen()
                elif event.type == pygame.VIDEORESIZE:
                    self.screen=pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    size = event.size
                    
            lscroll = scroll
            scroll = [(size[0] / 2) - self.chomp.pos[0] , (size[1] / 2) - self.chomp.pos[1] ]        
        
            
            # Draw the background
            self.screen.fill(white) 
            self.level.drawBackground(self.screen,scroll)
          
            # Draw tiles and handle tile collision with player
            self.level.updateTiles(self.screen,scroll,self.clock,self.chomp)
                  
            # Limit to 30 frames per second
            self.clock.tick(30)
            
            # Update time
            time = pygame.time.get_ticks() - start_time
            
            # If a dialog box isn't up...
            if not self.dlogbox.drawBox(self.screen,size,events):
                # Draw Sprites
                self.all_sprites_list.draw(self.screen)  
                # Update Chomp Movement...only when level is playable(i.e. not beaten or lost)
                if not self.level.state: self.chomp.update(scroll,move,size)       
                # Update Hud
                self.hud.update(self.screen,time)
                # Check level state
                if self.level.state == 1:
                    self.chomp.speed = 0
                    self.chomp.falling = 0
                    if self.transition.type == 0: self.dlogbox.setMessageBox(size,"SCORE: 4000 / TIME: " + str(round( time / 1000.0,2 )) , "Pwned", [['Retry',self.levelTransition],['Next Level',sys.exit]] )
                    
            # If there is a transition playing
            transition_status = self.transition.update(self.screen)
            if transition_status:
                if transition_status < 1:
                    self.transition.type = 0
                    start_time = pygame.time.get_ticks()
                    time = 0
                if transition_status and transition_status < 2 and self.level.state: self.startLevel()          
            
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
             
        # Be IDLE friendly. If you forget this line, the program will 'hang'
        # on exit.
        pygame.quit ()
 
Game()
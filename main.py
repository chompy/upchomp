import pygame, math, chompy, sound, gamemap, dialog, hud, transition, sys, iniget

try:
    import android, android_mixer
    #print "[OS] Running on Android."
except ImportError:
    #print "[OS] Running on PC."
    android = None

settings = iniget.iniGet("settings.ini")

# Define some colors
white    = ( 255, 255, 255)

class Game(object):

    def __init__(self):
    
        """Inits the game."""
 
        pygame.init()
        
        # Set size here so Android can overwrite it.
        size=[420,320]

        # Do some android stuff
        if android:
          android.init()
          
          # Map back key to to escape
          android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
          
          # Get display size and set game size to it
          disp_info = pygame.display.Info()
          size = [disp_info.current_w, disp_info.current_h]
          
          # Activate accelerometer
          if settings.getBool("android","accelerometer_enable"): android.accelerometer_enable(1)
        
        # Screen/Dialog stuff
        self.screen=pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.set_caption("UpChomp")


        # Used to manage how fast the screen updates
        self.clock=pygame.time.Clock()

        # Sprites
        self.all_sprites_list = pygame.sprite.RenderPlain()
        
        # Init da Chomp
        self.chomp = chompy.Chompy()
        self.all_sprites_list.add(self.chomp)   
        
        # Initalize Sound
        self.sound = sound.Sound()

        # Make a dialog object.
        self.dlogbox = dialog.Dialog()
        
        # Setup Hud
        self.hud = hud.Hud()
        
        # Setup Transition
        self.transition = transition.Transition()

        # Game State: 0-Playing, 1-Main Menu, 2-Pack Select
        self.state = 1
        
        # Init Game Map
        self.level = gamemap.Gamemap()
        
        # Frame rate
        self.frames = 1
        
        # Set Current Map
        self.map_file = ""
                
        # Enter game loop
        self.gameLoop()
        
    def gameLoop(self):
    
        # Options for each game state
        options = {
            0: self.startLevel,      # Playing
            1: self.menu,       # Main Menu
            2: self.packSelect       # Map Pack Select
        }
    
        done = False
        while not done:
            # State -1 means quit.
            if self.state == -1: done = True
            
            # Try to load a function for the current state
            try: options[self.state]()
            # If unable to find a function quit with an error.
            except KeyError: 
                #print "[ERROR] Not a valid game state. Exiting..."
                done = True
            
        # Exit Game
        pygame.quit()
        
    def menu(self):
        done = 0
        
        # Screen size
        size = self.screen.get_size()
        
        # Load background        
        background = pygame.image.load("gfx/menu_bg.png").convert()
        title_logo = pygame.image.load("gfx/title_logo.png").convert_alpha()        
        bg_rect = background.get_rect()
        
        tl_rect_big = title_logo.get_rect()
        
        new_size = [tl_rect_big.w / (tl_rect_big.h / size[1]) , size[1] ]                
        title_logo_sized = pygame.transform.smoothscale(title_logo, (new_size[0], new_size[1]))
        
        tl_rect = title_logo_sized.get_rect()
        if size[1] > bg_rect.h: bgrows = int(math.ceil(size[1] / bg_rect.h) * 2)
        if size[0] > bg_rect.w: bgcols = int(math.ceil(size[0] / bg_rect.w) * 2)
        
        tl_rect.x = (size[0] / 2) - (tl_rect.w / 2)
        tl_rect.y = (size[1] / 2) - (tl_rect.h / 2)
   
        bgoffset = 0
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
                    self.state = -1 # Set game state to -1(Quit)

                elif event.type == pygame.VIDEORESIZE:
                    self.screen=pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    size = event.size

                    if size[1] > bg_rect.h: bgrows = int(math.ceil(size[1] / bg_rect.h) * 2)
                    if size[0] > bg_rect.w: bgcols = int(math.ceil(size[0] / bg_rect.w) * 2)
                    bg_rect.x = 0
                    bg_rect.y = 0
                    bgoffset = 0
                   
                    new_size = [tl_rect_big.w / (tl_rect_big.h / size[1]) , size[1] ]                
                    title_logo_sized = pygame.transform.smoothscale(title_logo, (new_size[0], new_size[1]))       
                    
                    tl_rect = title_logo_sized.get_rect()
                    tl_rect.x = (size[0] / 2) - (tl_rect.w / 2)
                    tl_rect.y = (size[1] / 2) - (tl_rect.h / 2)
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    done = 1
                    self.state = 2
                   
           
            # Background       
            bg_rect.x -= bg_rect.w 
            bg_rect.y -= bg_rect.h
            for yy in xrange(bgrows):
                for xx in xrange(bgcols):
                    # Start a new row
                    if xx == 0 and yy > 0:
                        # Move the rectangle
                        bg_rect = bg_rect.move([-(bgcols -1 ) * bg_rect.w, bg_rect.h])
                    # Continue a row
                    if xx > 0:
                        # Move the rectangle
                        bg_rect = bg_rect.move([bg_rect.w, 0])
                    self.screen.blit(background, bg_rect)
            bg_rect.x = 0 + bgoffset
            bg_rect.y = 0 + bgoffset
            bgoffset -= 1
            if bgoffset > 10: bgoffset = 0
            
            # Title Logo
            self.screen.blit(title_logo_sized, tl_rect)
               
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()             
        
    def packSelect(self):
        self.map_file = "map2.map"
        self.state = 0
        
    def nextLevel(self):
        self.level.current_map += 1
        self.levelTransition()
                        
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

        # Load Level
        self.level.loadLevel(self.map_file)  
        self.level.state = 0
        
        # Place character in level
        pos = self.level.parser.get(self.level.packMaps[self.level.current_map],"startpos").split(",")
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
        
        # Load skills into the Hud
        self.hud.loadSkills(size, self.level.parser.get(self.level.packMaps[self.level.current_map],"skills").split(","))
        
        # Load Dialog box
        self.dlogbox.setMessageBox(size,self.level.parser.get(self.level.packMaps[self.level.current_map],"desc"), self.level.parser.get(self.level.packMaps[self.level.current_map],"name"), [['Play!',self.dlogbox.closeMessageBox],['Quit',sys.exit]] )
        
        #Loop until the user clicks the close button.
        done=False

        # Stop all sounds
        self.sound.stopAllSfx()

        pygame.event.set_allowed((pygame.KEYDOWN, pygame.QUIT, pygame.MOUSEMOTION, pygame.VIDEORESIZE, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP))                    
        # -------- Main Program Loop -----------
        while not done:

          # Set frame rate to 30.
          self.clock.tick(30)       
      
          # Plus one frame
          self.frames += 1
          
          events = pygame.event.get()
          for event in events: # User did something
              if event.type == pygame.QUIT: # If user clicked close
                  done=True # Flag that we are done so we exit this loop
                  self.state = -1 # Set game state to -1(Quit)
              
              elif event.type == pygame.MOUSEBUTTONDOWN: 
                  move = (event.pos[0] - (size[0] / 2.0)) / (size[0] / 8.0)
      
              elif event.type == pygame.MOUSEBUTTONUP: 
                  move = 0
                  
              elif event.type == pygame.MOUSEMOTION and move:
                  move = (event.pos[0] - (size[0] / 2.0)) / (size[0] / 8.0)
              
              elif event.type == pygame.KEYDOWN:
                  # Move with keyboard
                  if event.key == pygame.K_LEFT: move = -4
                  elif event.key == pygame.K_RIGHT: move = 4
                  
                  # Toogle Fullscreen
                  elif event.key == 292: pygame.display.toggle_fullscreen()
                  
              elif event.type == pygame.KEYUP:
                  # Move with keyboard
                  if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: move = 0                               
                  
              elif event.type == pygame.VIDEORESIZE:
                  self.screen=pygame.display.set_mode(event.size, pygame.RESIZABLE)
                  size = event.size
                  self.hud.loadSkills(size)
                  
          # Android events
          if android:
            if android.check_pause():
              android.wait_for_resume()
              
            accel = android.accelerometer_reading()
            if abs(accel[1]) > .5:
                move = accel[1] * 1.4

              
          lscroll = scroll
          scroll = [(size[0] / 2) - self.chomp.pos[0] , (size[1] / 2) - self.chomp.pos[1] ]        
         
          # Draw the background
          self.screen.fill(white) 
          self.level.drawBackground(self.screen,scroll)
        
          # Draw tiles and handle tile collision with player
          self.level.updateTiles(self.screen,scroll,size,(self.frames / ((pygame.time.get_ticks() / 1000) + 1) ) ,self.chomp, self.sound)
                
          
          # Update time
          time = pygame.time.get_ticks() - start_time
          
          # Android Sound Loops
          if android: self.sound.update()
          
          # If a dialog box isn't up...
          if not self.dlogbox.drawBox(self.screen,size,events):
              # Draw Sprites
              self.all_sprites_list.draw(self.screen)  
              # Update Chomp Movement...only when level is playable(i.e. not beaten or lost)
              if not self.level.state: self.chomp.update(scroll, self.screen, move, size, self.sound)       
              
              # If Chompy can't move it's game over...
              if not self.chomp.moveok and self.chomp.speed == 0: 
                if self.chomp.stopclock < 0: self.chomp.stopclock = 30
              else: self.chomp.stopclock = -1

              if self.chomp.stopclock == 0:
                self.level.state = 2
              
              # If Chompy falls below the level...
              if self.chomp.colliderect.y > self.level.mapheight * self.level.tilesize[1]:
                self.level.state = 2
                
              # Game over level state...
              if self.level.state == 2:
                self.chomp.speed = .1
                self.chomp.falling = .1
                self.chomp.moveok = 1
                if self.transition.type == 0: 
                  self.dlogbox.setMessageBox(size,"Chompy didn't make it...", "Oh No!!", [['Retry',self.levelTransition],['Quit',sys.exit]] )
                
              # Update Hud
              self.hud.update(self.screen,size,time,self.frames,move)
              self.hud.checkSkillActivation(events, size, self.chomp, self.sound)
              # Check level state
              if self.level.state == 1:
                  self.chomp.speed = 0
                  self.chomp.falling = 0
                  if self.transition.type == 0: 
                    self.dlogbox.setMessageBox(size,"SCORE: 4000 / TIME: " + str(round( time / 1000.0,2 )) , "Pwned", [['Retry',self.levelTransition],['Next Level',self.nextLevel]] )
          
          # Reset time as long as dialog box is up
          else:
              start_time = pygame.time.get_ticks()
              time = 0
          
                  
          # If there is a transition playing
          transition_status = self.transition.update(self.screen)
          if transition_status:
              if transition_status < 1:
                  self.transition.type = 0
              if transition_status and transition_status < 2 and self.level.state: done = True  
          
          # Go ahead and update the screen with what we've drawn.
          pygame.display.flip()
 
Game()

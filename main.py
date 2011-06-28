import pygame, math, menu, chompy, sound, gamemap, dialog, hud, transition, sys, iniget, traceback

try:
    import android, android_mixer
    print "[OS] Running on Android."
except ImportError:
    print "[OS] Running on PC."
    android = None

settings = iniget.iniGet("settings.ini")
error_log = open('error.log', 'w')

# Define some colors
white    = ( 255, 255, 255)

class Game(object):

    def __init__(self):

        """Inits the game."""

        pygame.init()

        # Set size here so Android can overwrite it.
        size=[640,480]

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

        # Init Menu
        self.menu = menu.Menu()
        
        # Initalize Sound
        self.sound = sound.Sound()

        # Make a dialog object.
        self.dlogbox = dialog.Dialog()

        # Setup Hud
        self.hud = hud.Hud()

        # Setup Transition
        self.transition = transition.Transition()

        # Game State: 0-Playing, 1-Main Menu, 2-Pack Select, 3 - Load New Level
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
            1: self.displayMenu,     # Main Menu
            2: self.mapSelect        # Map Pack Select
        }

        done = False

        while not done:
            # State -1 means quit.
            if self.state == -1: done = True
            
            # State 3 is just reloading state 0.
            if self.state == 3: self.state = 0
            
            # Stop all sounds
            self.sound.stopAllSfx()

            # Try to load a function for the current state
            try: options[self.state]()
            # If unable to find a function quit with an error.
            except KeyError:
                #print "[ERROR] Not a valid game state. Exiting..."
                done = True

        # Exit Game
        pygame.quit()

    def displayMenu(self):
        self.state = self.menu.show(self.screen, self.clock)
        
    def mapSelect(self):
        self.level.current_map = 0
        self.map_file = self.menu.mapSelect(self.screen, self.clock)  
        if self.map_file == 0: self.setState(1)
        elif self.map_file == -1: self.setState(-1)
        else: self.setState(0)

    def nextLevel(self):
        self.level.current_map += 1
        self.levelTransition()

    def levelTransition(self):
        size = self.screen.get_size()
        self.transition.verticalSwipe(size)
        self.dlogbox.closeMessageBox()
        
    def setState(self, state = 2):
        self.state = state
        
    def startLevel(self):

        """Loads a level and begins gameplay."""

        # Reset Chompy
        self.chomp.reset()

        # Screen size
        size = self.screen.get_size()

        # Load Level
        try:
            self.level.loadLevel(self.map_file)
            self.level.state = 0
        except:
            traceback.print_exc(5, error_log)
            self.menu.dialog.setMessageBox(size, "There was an error with loading this map.", "Error", [['OK',self.menu.dialog.closeMessageBox]] )  
            self.state = 2
            return 0

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
        self.dlogbox.setMessageBox(size, self.level.parser.get(self.level.packMaps[self.level.current_map],"desc"), self.level.parser.get(self.level.packMaps[self.level.current_map],"name"), [['Play!',self.dlogbox.closeMessageBox],['Map Select', self.setState]] )

        # Stop all sounds
        self.sound.stopAllSfx()              

        pygame.event.set_allowed((pygame.KEYDOWN, pygame.QUIT, pygame.MOUSEMOTION, pygame.VIDEORESIZE, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP))
        
        # -------- Main Program Loop -----------
        while self.state == 0:

            # Set frame rate to 30.
            self.clock.tick(30)

            # Plus one frame
            self.frames += 1

            events = pygame.event.get()
            for event in events: # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.setState(-1) # Set game state to -1(Quit)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    move = (event.pos[0] - (size[0] / 2.0)) / (size[0] / 8.0)

                elif event.type == pygame.MOUSEBUTTONUP:
                    move = 0

                elif event.type == pygame.MOUSEMOTION and move:
                    move = (event.pos[0] - (size[0] / 2.0)) / (size[0] / 8.0)

                elif event.type == pygame.KEYDOWN:
                    # Move with keyboard
                    if event.key == pygame.K_LEFT: move = -2.5
                    elif event.key == pygame.K_RIGHT: move = 2.5

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
            self.level.drawBackground(self.screen, scroll, size)

            # Draw tiles and handle tile collision with player
            self.level.updateTiles(self.screen,scroll,size,(self.frames / ((pygame.time.get_ticks() / 1000) + 1) ) ,self.chomp, self.sound)

            # Update time
            time = pygame.time.get_ticks() - start_time

            # Android Sound Loops
            if android: self.sound.update()

            # If a dialog box isn't up...
            dbox = self.dlogbox.drawBox(self.screen, size, events)
            if not dbox:
                # Update Chomp Movement...only when level is playable(i.e. not beaten or lost)
                if not self.level.state: self.chomp.update(scroll, self.screen, move, size, self.sound)
                # Draw Sprites
                self.all_sprites_list.draw(self.screen)
                
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
                        self.dlogbox.setMessageBox(size,"Chompy didn't make it...", "Oh No!!", [['Retry',self.levelTransition],['Map Select', self.setState]] )

                # Update Hud
                self.hud.update(self.screen,size,time)
                self.hud.checkSkillActivation(events, size, self.chomp, self.sound)
                # Check level state
                if self.level.state == 1:
                    self.chomp.speed = 0
                    self.chomp.falling = 0
                    if self.transition.type == 0:
                        self.dlogbox.setMessageBox(size,"TIME: " + str(round( time / 1000.0,2 )) , "Pwned", [['Retry',self.levelTransition],['Next Level',self.nextLevel]] )

            # If closed by clicking X return to map select.
            elif dbox == -1: 
                self.setState(2)
            # Reset time as long as dialog box is up
            else:
                start_time = pygame.time.get_ticks()
                time = 0

            # If there is a transition playing
            transition_status = self.transition.update(self.screen)
            if transition_status:
                if transition_status < 1:
                    self.transition.type = 0
                if transition_status and transition_status < 2 and self.level.state: self.setState(3)

            # If the back button was clicked in the hud...
            if self.hud.doMapSelect:
                self.setState(2)
                self.hud.doMapSelect = 0
                
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

Game()

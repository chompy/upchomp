import pygame, math, imagehelper

# Image Helper Object
imghelp = imagehelper.imageHelper()

# Constants
SPACING = 24
SHADOW_OFFSET = 2
SKILL_TILE_SIZE = [32,32]

class Hud(object):

    def __init__(self, screen, sound):
    
        """ Inits the Hud """
    
        # Load font
        self.font = pygame.font.Font("font/volter2.ttf",18)

        self.object_color = [255, 179, 0]
        self.value_color = [255, 255, 255]
        self.dropshadow_color = [0,0,0]

        # Set skill tiles [All hard coded for now.]
        self.skilltiles = {
            'up'        : [0,0],
            'heli'      : [1,0]
        }

        image = pygame.image.load("gfx/skills.png").convert_alpha()
        image_width, image_height = image.get_size()
        self.tile_image_size = [image_width,image_height]
        self.tile_table = imghelp.makeTiles(image, SKILL_TILE_SIZE)
        
        # Get Ready, Go, message.
        self.ready = [pygame.image.load("gfx/get_ready.png").convert_alpha(), pygame.image.load("gfx/go.png").convert_alpha()]
        self.ready_time = 0
        
        # Go back to map select if this var is true...
        self.doMapSelect = 0
        
        # Get Screen object
        self.screen = screen
        
        # Get Sound Object
        self.sound = sound

    def loadSkills(self, size, skills = 0):
        
        """
        Loads up skills on the hud.
        
        @param array size - Size of self.screen.
        @param array skills - Array containing names of all the skills to be used.
        """
    
        # If skills is provided then load them in, otherwise we're just resizing the self.screen.      
        if not skills or skills[0] == '': skills = 0
        
        if skills:
            self.skills = {
                'up'        : 0,
                'heli'      : 0
            }
            self.skill_data = []
            for i in skills:
                self.skills[i] += 1

            x = 0        
            self.skill_data = []
        
            for i in self.skills:
                if self.skills[i]:
                    self.skill_data.append([
                      i,
                      [math.floor(SKILL_TILE_SIZE[0] / 2) + x * (SKILL_TILE_SIZE[0] * 2.5), size[1] - math.floor(SKILL_TILE_SIZE[1] * 1.5)],
                      pygame.Rect(math.floor(SKILL_TILE_SIZE[0] / 2) + x * (SKILL_TILE_SIZE[0] * 2), size[1] - math.floor(SKILL_TILE_SIZE[1] * 1.5), SKILL_TILE_SIZE[0] * 2, SKILL_TILE_SIZE[1])
                    ])
                    x += 1
        else:
            self.skill_data = 0
       

    def update(self, size, time):
    
        """
        Updates the hud on the self.screen.
        
        @param pygame.self.screen self.screen - Pygame self.screen object.
        @param array size - Size of self.screen.
        @param int time - Ticks the level as been running.
        """

        # Time and Score
        #self.screen.blit(self.font.render("SCORE:",0,self.dropshadow_color), (SPACING + SHADOW_OFFSET,SPACING + SHADOW_OFFSET) )
        #self.screen.blit(self.font.render("SCORE:",0,self.object_color), (SPACING,SPACING) )

        #self.screen.blit(self.font.render("999999999",0,self.dropshadow_color), (SPACING + SHADOW_OFFSET,(SPACING * 2) + SHADOW_OFFSET) )
        #self.screen.blit(self.font.render("999999999",0,self.value_color), (SPACING,SPACING * 2) )

        self.screen.blit(self.font.render("TIME:",0,self.dropshadow_color), (SPACING + SHADOW_OFFSET,(SPACING) + SHADOW_OFFSET) )
        self.screen.blit(self.font.render("TIME:",0,self.object_color), (SPACING,SPACING) )

        self.screen.blit(self.font.render(str(round(time / 1000.0,2)) ,0,self.dropshadow_color), (SPACING + SHADOW_OFFSET,(SPACING * 2) + SHADOW_OFFSET) )
        self.screen.blit(self.font.render(str(round(time / 1000.0,2)),0,self.value_color), (SPACING,SPACING * 2) )

        #msg = "FPS: " + str(frames / (pygame.time.get_ticks() / 1000) )
        #self.screen.blit(self.font.render(msg,0,self.value_color), (size[0] - self.font.size(msg)[0] - (SPACING / 2) ,SPACING * 1.5) )

        # Skills
        x = 0
        if self.skill_data:
            for i in self.skill_data:
                if self.skills[i[0]] > 0:
                    pos = i[1]
                    # Render skill icon
                    self.screen.blit(self.tile_table[self.skilltiles[i[0]][0]][self.skilltiles[i[0]][1]], (pos[0],pos[1]) )
                    # Render skill amount text
                    self.screen.blit(self.font.render("x" + str(self.skills[i[0]]) ,0,self.dropshadow_color), (  pos[0] + SKILL_TILE_SIZE[0] + SHADOW_OFFSET , pos[1] + SHADOW_OFFSET) )
                    self.screen.blit(self.font.render("x" + str(self.skills[i[0]]) ,0,self.object_color), (  pos[0] + SKILL_TILE_SIZE[0] , pos[1]) )
    
                    x += 1

        # Quit button
        self.screen.blit(self.tile_table[2][2], ( size[0] - math.floor(SKILL_TILE_SIZE[0] * 1.5), size[1] - math.floor(SKILL_TILE_SIZE[1] * 1.5)) )


    def checkSkillActivation(self, events, size, chomp):

        for event in events:

            # Activate skills with keyboard
            if event.type == pygame.KEYDOWN:
                # skills
                if self.skill_data:
                    for i in range(len(self.skill_data)):
                        key = pygame.key.name(event.key)
                        try:
                            if int(key) == i + 1:
                                if self.skills[ self.skill_data[i][0] ] > 0:
                                    self.skills[ self.skill_data[i][0] ] -= 1
                                    chomp.activateSkill( self.skill_data[i][0] )
                        except ValueError:
                            break
                            
                if event.key == pygame.K_ESCAPE:
                    self.doMapSelect = 1
                    self.sound.playSfx("sfx/button.wav", 0)                                                

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Back Button button
                button_rect = pygame.Rect(size[0] - math.floor(SKILL_TILE_SIZE[0] * 1.5), size[1] - math.floor(SKILL_TILE_SIZE[1] * 1.5), SKILL_TILE_SIZE[0], SKILL_TILE_SIZE[1])
                if button_rect.collidepoint(event.pos[0], event.pos[1]):
                    self.doMapSelect = 1
                    self.sound.playSfx("sfx/button.wav", 0)

                # Other buttons
                if self.skill_data:
                    for i in self.skill_data:
                        button_rect = i[2]
                        if button_rect.collidepoint(event.pos[0], event.pos[1]):
                            if self.skills[i[0]] > 0:
                                self.skills[i[0]] -= 1
                                chomp.activateSkill(i[0])

                                
    def getReady(self, size):
        
        """Displays 'Get Ready', 'Go!' message."""
        rect = pygame.Rect(0, 0, size[0], size[1])
        ready_rect = self.ready[0].get_rect()
        ready_rect = ready_rect.fit(rect)
        
        if pygame.time.get_ticks() - self.ready_time < 2000:
            self.screen.blit( pygame.transform.scale(self.ready[0], (ready_rect.w, ready_rect.h)), ( (size[0] / 2) - (ready_rect.w / 2), (size[1] / 2) - (ready_rect.h / 2)))
            return 1
        elif pygame.time.get_ticks() - self.ready_time >= 2000 and pygame.time.get_ticks() - self.ready_time < 3000:
            self.screen.blit( pygame.transform.scale(self.ready[1], (ready_rect.w, ready_rect.h)), ( (size[0] / 2) - (ready_rect.w / 2), (size[1] / 2) - (ready_rect.h / 2)))               
            return 1
        else:
            return 0
        
import pygame, math, imagehelper

# Image Helper Object
imghelp = imagehelper.imageHelper()

# Constants
SPACING = 24
SHADOW_OFFSET = 2
SKILL_TILE_SIZE = [32,32]

class Hud(object):

    def __init__(self):
    
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
        
        # Go back to map select if this var is true...
        self.doMapSelect = 0

    def loadSkills(self, size, skills = 0):
        
        """
        Loads up skills on the hud.
        
        @param array size - Size of screen.
        @param array skills - Array containing names of all the skills to be used.
        """
    
        # If skills is provided then load them in, otherwise we're just resizing the screen.      
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
                self.skill_data.append([
                  i,
                  [math.floor(SKILL_TILE_SIZE[0] / 2) + x * (SKILL_TILE_SIZE[0] * 2.5), size[1] - math.floor(SKILL_TILE_SIZE[1] * 1.5)],
                  pygame.Rect(math.floor(SKILL_TILE_SIZE[0] / 2) + x * (SKILL_TILE_SIZE[0] * 2), size[1] - math.floor(SKILL_TILE_SIZE[1] * 1.5), SKILL_TILE_SIZE[0] * 2, SKILL_TILE_SIZE[1])
                ])
                x += 1
        else:
            self.skill_data = 0
       

    def update(self, screen, size, time):
    
        """
        Updates the hud on the screen.
        
        @param pygame.screen screen - Pygame screen object.
        @param array size - Size of screen.
        @param int time - Ticks the level as been running.
        """

        # Time and Score
        screen.blit(self.font.render("SCORE:",0,self.dropshadow_color), (SPACING + SHADOW_OFFSET,SPACING + SHADOW_OFFSET) )
        screen.blit(self.font.render("SCORE:",0,self.object_color), (SPACING,SPACING) )

        screen.blit(self.font.render("999999999",0,self.dropshadow_color), (SPACING + SHADOW_OFFSET,(SPACING * 2) + SHADOW_OFFSET) )
        screen.blit(self.font.render("999999999",0,self.value_color), (SPACING,SPACING * 2) )

        screen.blit(self.font.render("TIME:",0,self.dropshadow_color), (SPACING + SHADOW_OFFSET,(SPACING * 3.5) + SHADOW_OFFSET) )
        screen.blit(self.font.render("TIME:",0,self.object_color), (SPACING,SPACING * 3.5) )

        screen.blit(self.font.render(str(round(time / 1000.0,2)) ,0,self.dropshadow_color), (SPACING + SHADOW_OFFSET,(SPACING * 4.5) + SHADOW_OFFSET) )
        screen.blit(self.font.render(str(round(time / 1000.0,2)),0,self.value_color), (SPACING,SPACING * 4.5) )

        #msg = "FPS: " + str(frames / (pygame.time.get_ticks() / 1000) )
        #screen.blit(self.font.render(msg,0,self.value_color), (size[0] - self.font.size(msg)[0] - (SPACING / 2) ,SPACING * 1.5) )

        # Skills
        x = 0
        if self.skill_data:
            for i in self.skill_data:
                if self.skills[i[0]] > 0:
                    pos = i[1]
                    # Render skill icon
                    screen.blit(self.tile_table[self.skilltiles[i[0]][0]][self.skilltiles[i[0]][1]], (pos[0],pos[1]) )
                    # Render skill amount text
                    screen.blit(self.font.render("x" + str(self.skills[i[0]]) ,0,self.dropshadow_color), (  pos[0] + SKILL_TILE_SIZE[0] + SHADOW_OFFSET , pos[1] + SHADOW_OFFSET) )
                    screen.blit(self.font.render("x" + str(self.skills[i[0]]) ,0,self.object_color), (  pos[0] + SKILL_TILE_SIZE[0] , pos[1]) )
    
                    x += 1

        # Quit button
        screen.blit(self.tile_table[2][2], ( size[0] - math.floor(SKILL_TILE_SIZE[0] * 1.5), size[1] - math.floor(SKILL_TILE_SIZE[1] * 1.5)) )


    def checkSkillActivation(self, events, size, chomp, sound = ""):

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
                                    chomp.activateSkill( self.skill_data[i][0], sound )
                        except ValueError:
                            break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Back Button button
                button_rect = pygame.Rect(size[0] - math.floor(SKILL_TILE_SIZE[0] * 1.5), size[1] - math.floor(SKILL_TILE_SIZE[1] * 1.5), SKILL_TILE_SIZE[0], SKILL_TILE_SIZE[1])
                if button_rect.collidepoint(event.pos[0], event.pos[1]):
                    self.doMapSelect = 1

                # Other buttons
                if self.skill_data:
                    for i in self.skill_data:
                        button_rect = i[2]
                        if button_rect.collidepoint(event.pos[0], event.pos[1]):
                            if self.skills[i[0]] > 0:
                                self.skills[i[0]] -= 1
                                chomp.activateSkill(i[0], sound)

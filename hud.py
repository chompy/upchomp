import pygame, math
SPACING = 24
SHADOW_OFFSET = 2
SKILL_TILE_SIZE = [32,32]

class Hud(object):

    def __init__(self):
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
        self.tile_table = []
        for tile_x in range(0, image_width/SKILL_TILE_SIZE[0]):
            line = []
            self.tile_table.append(line)
            for tile_y in range(0, image_height/SKILL_TILE_SIZE[1]):
                rect = (tile_x*SKILL_TILE_SIZE[0], tile_y*SKILL_TILE_SIZE[1], SKILL_TILE_SIZE[0], SKILL_TILE_SIZE[1])
                line.append(image.subsurface(rect))      
        
    def loadSkills(self,skills):
        self.skills = {
            'up'        : 0,
            'heli'      : 0
        }
        
        for i in skills:
            self.skills[i] += 1
            
        
        
    def update(self,screen,size,time,):  
        
        # Time and Score     
        screen.blit(self.font.render("SCORE:",0,self.dropshadow_color), (SPACING + SHADOW_OFFSET,SPACING + SHADOW_OFFSET) )
        screen.blit(self.font.render("SCORE:",0,self.object_color), (SPACING,SPACING) )        

        screen.blit(self.font.render("999999999",0,self.dropshadow_color), (SPACING + SHADOW_OFFSET,(SPACING * 2) + SHADOW_OFFSET) )
        screen.blit(self.font.render("999999999",0,self.value_color), (SPACING,SPACING * 2) ) 
        
        screen.blit(self.font.render("TIME:",0,self.dropshadow_color), (SPACING + SHADOW_OFFSET,(SPACING * 3.5) + SHADOW_OFFSET) )
        screen.blit(self.font.render("TIME:",0,self.object_color), (SPACING,SPACING * 3.5) )        

        screen.blit(self.font.render(str(round(time / 1000.0,2)) ,0,self.dropshadow_color), (SPACING + SHADOW_OFFSET,(SPACING * 4.5) + SHADOW_OFFSET) )
        screen.blit(self.font.render(str(round(time / 1000.0,2)),0,self.value_color), (SPACING,SPACING * 4.5) )                
        
        # Skills
        x = 0
        for i in self.skills:
            if self.skills[i] > 0:
                pos = [math.floor(SKILL_TILE_SIZE[0] / 2) + x * (SKILL_TILE_SIZE[0] * 2), size[1] - math.floor(SKILL_TILE_SIZE[1] * 1.5)]
                # Render skill icon
                screen.blit(self.tile_table[self.skilltiles[i][0]][self.skilltiles[i][1]], (pos[0],pos[1]) )
                # Render skill amount text
                screen.blit(self.font.render("x" + str(self.skills[i]) ,0,self.dropshadow_color), (  pos[0] + SKILL_TILE_SIZE[0] + SHADOW_OFFSET , pos[1] + SHADOW_OFFSET) )                
                screen.blit(self.font.render("x" + str(self.skills[i]) ,0,self.object_color), (  pos[0] + SKILL_TILE_SIZE[0] , pos[1]) )        
                                
                x += 1   
                
                
    def checkSkillActivation(self,events):
        for event in events:
            for i in range(len(self.buttonstate)):
                self.buttonstate[i] = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_btn.collidepoint(event.pos[0], event.pos[1]):
                    self.closeMessageBox() 
                for i in range(len(self.button)):
                    button_text_size = self.font.size(self.button[i][0])
                    button_tile_width = int(math.floor(button_text_size[0] / TILE_SIZE[0])) + 2
                    button_rect = pygame.Rect(button_positions[i][0], button_positions[i][1], button_tile_width * TILE_SIZE[0], TILE_SIZE[1])
        
                    # If button click initiate passed function
                    if button_rect.collidepoint(event.pos[0], event.pos[1]):
                        self.button[i][1]()
                        self.closeMessageBox()     
                        

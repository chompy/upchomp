import pygame
SPACING = 24
SHADOW_OFFSET = 2

class Hud(object):

    def __init__(self):
        # Load font
        
        self.font = pygame.font.Font("font/volter2.ttf",18)
        
        self.object_color = [255, 179, 0]  
        self.value_color = [255, 255, 255]
        self.dropshadow_color = [0,0,0]
        
    def update(self,screen,time):       
        screen.blit(self.font.render("SCORE:",0,self.dropshadow_color), (SPACING + SHADOW_OFFSET,SPACING + SHADOW_OFFSET) )
        screen.blit(self.font.render("SCORE:",0,self.object_color), (SPACING,SPACING) )        

        screen.blit(self.font.render("999999999",0,self.dropshadow_color), (SPACING + SHADOW_OFFSET,(SPACING * 2) + SHADOW_OFFSET) )
        screen.blit(self.font.render("999999999",0,self.value_color), (SPACING,SPACING * 2) ) 
        
        screen.blit(self.font.render("TIME:",0,self.dropshadow_color), (SPACING + SHADOW_OFFSET,(SPACING * 3.5) + SHADOW_OFFSET) )
        screen.blit(self.font.render("TIME:",0,self.object_color), (SPACING,SPACING * 3.5) )        

        screen.blit(self.font.render(str(round(time / 1000.0,2)) ,0,self.dropshadow_color), (SPACING + SHADOW_OFFSET,(SPACING * 4.5) + SHADOW_OFFSET) )
        screen.blit(self.font.render(str(round(time / 1000.0,2)),0,self.value_color), (SPACING,SPACING * 4.5) )                   
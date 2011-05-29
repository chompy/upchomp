
import pygame, math, chompy, gamemap
 
# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
 
# Level
level = [
			1, 1, 1, 1, 1, 1,
			2, 0, 0, 0, 0, 2,
			2, 0, 0, 0, 0, 2,
			2, 0, 0, 0, 1, 2,
			2, 0, 0, 1, 0, 2,
			2, 0, 1, 0, 0, 2,			
			1, 1, 1, 1, 1, 1 
		]
level_x = 6
level_y = 7

pygame.init()
  
# Set the height and width of the screen
size=[700,500]
screen=pygame.display.set_mode(size)
 
pygame.display.set_caption("ChompGaem")
 
#Loop until the user clicks the close button.
done=False
 
# Used to manage how fast the screen updates
clock=pygame.time.Clock()

# Sprites
all_sprites_list = pygame.sprite.RenderPlain()
 
# Init da Chomp
chomp = chompy.Chompy()
all_sprites_list.add(chomp)

# Init da level
loadlevel = gamemap.Gamemap("gfx/woodtiles.png", 32,32)
print loadlevel.tile_table


# -------- Main Program Loop -----------
while done==False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
 
    # Set the screen background
    screen.fill(white)
 
    pos = pygame.mouse.get_pos()
    chomp.rect.x=pos[0] - (chomp.rect.w / 2)
    chomp.rect.y=pos[1] - (chomp.rect.h / 2)  

    # Draw the level
    x = 0
    i = 0 
    for i in level:
        if not i == 0:
            screen.blit(loadlevel.tile_table[i - 1][0], ( ((x % level_x) * 32), math.floor(x / level_x) * 32))
        x += 1
    
    # Limit to 20 frames per second
    clock.tick(20)

   	# Draw Sprites
    all_sprites_list.draw(screen)
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit ()
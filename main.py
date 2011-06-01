
import pygame, math, chompy, gamemap
 
# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
 
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
loadlevel = gamemap.Gamemap("map1.map")

# Map scroll
scroll = [(size[0] / 2) - ((loadlevel.mapwidth * loadlevel.tilesize[0]) / 2),(size[1] / 2) - (( math.floor(len(loadlevel.map) / loadlevel.mapwidth) * loadlevel.tilesize[1]) / 2)]

pos = [64 + scroll[0],64 + scroll[1]]
# Gravity releated stuff
GRAVITY = -9.81
grav_rate = GRAVITY / 20
falling = 0

# -------- Main Program Loop -----------
while done==False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: falling = -10
            elif event.key == pygame.K_DOWN: pos[1] += 8
            if event.key == pygame.K_LEFT: pos[0] -= 8
            elif event.key == pygame.K_RIGHT: pos[0] += 8
 
    # Draw the background
    screen.fill(white) 

    if loadlevel.themeparser.get("images","background"):
        for yy in xrange(loadlevel.bgrows):
            for xx in xrange(loadlevel.bgcolumns):
                # Start a new row
                if xx == 0 and yy > 0:
                    # Move the rectangle
                    loadlevel.bg_rect = loadlevel.bg_rect.move([-(loadlevel.bgcolumns -1 ) * loadlevel.bg_rect.width, loadlevel.bg_rect.height])
                # Continue a row
                if xx > 0:
                    # Move the rectangle
                    loadlevel.bg_rect = loadlevel.bg_rect.move([loadlevel.bg_rect.width, 0])
                screen.blit(loadlevel.background,loadlevel.bg_rect)
        loadlevel.bg_rect.x = 0
        loadlevel.bg_rect.y = 0


    oldpos = [chomp.rect.x,chomp.rect.y]
    
    # Gravity
    falling += grav_rate * -1
    if falling > GRAVITY * -1: falling = GRAVITY * -1
    pos[1] += falling
    
    chomp.rect.x=pos[0]
    chomp.rect.y=pos[1]

    # Draw the level
    x = 0
    i = 0 
    for i in loadlevel.map:
        # Render Tiles
        if loadlevel.themeparser.get(i, "tile"):
            
            tile = loadlevel.themeparser.get(i, "tile")
            tile = tile.split(",")
            
            screen.blit(loadlevel.tile_table[int(tile[0])][int(tile[1])], ( ((x % loadlevel.mapwidth) * loadlevel.tilesize[0]) + scroll[0], (math.floor(x / loadlevel.mapwidth) * loadlevel.tilesize[1] + scroll[1])) )
            
        # Collision with a tile
        if loadlevel.themeparser.getboolean(i,"collide"):
            col = loadlevel.collision(chomp,x,scroll)
            
            if col:
                dir_x = pos[0] - oldpos[0]
                dir_y = pos[1] - oldpos[1]
                if dir_x > 0: dir_x = 1
                else: dir_x = -1
                if dir_y > 0: dir_y = 1
                else: dir_y = -1                
                chomp.rect.x = pos[0] = oldpos[0]
                chomp.rect.y = pos[1] = oldpos[1] - dir_y              
                falling = 0
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

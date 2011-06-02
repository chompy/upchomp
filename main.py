
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
 

# Init da level
loadlevel = gamemap.Gamemap("map1.map")

# Map scroll
scroll = [(size[0] / 2) - ((loadlevel.mapwidth * loadlevel.tilesize[0]) / 2),(size[1] / 2) - (( math.floor(len(loadlevel.map) / loadlevel.mapwidth) * loadlevel.tilesize[1]) / 2)]
lscroll = scroll

# Init da Chomp
chomp = chompy.Chompy()
all_sprites_list.add(chomp)

pos = loadlevel.parser.get("level","startpos").split(",")
pos[0] = int(pos[0]) * loadlevel.tilesize[0]
pos[1] = int(pos[1]) * loadlevel.tilesize[1]
chomp.colliderect.x = pos[0]
chomp.colliderect.y = pos[1]

speed = 0.0
max_speed = 16
move = 0

# Gravity releated stuff
GRAVITY = -9.81
grav_rate = GRAVITY / 20
falling = 0

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
            if event.key == 273: pos[1] -= 64
        
    if move:
            
        if move > size[0] / 2:
            pos[0] += math.floor(speed)
            if speed < max_speed: speed += float(max_speed) / 32.0
        else:
            pos[0] += math.floor(speed)
            if speed > max_speed * -1: speed -= float(max_speed) / 32.0
    else: 
        pos[0] += math.floor(speed)
        if speed > 0: speed -= float(max_speed) / 16.0
        elif speed < 0: speed += float(max_speed) / 16.0
        elif abs(speed) < 1: speed = 0
 
    lscroll = scroll
    scroll = [(size[0] / 2) - pos[0] , (size[1] / 2) - pos[1] ]        
   
    # Draw the background
    screen.fill(white) 
  
    if loadlevel.themeparser.get("images","background"):
        loadlevel.bg_rect.x -= loadlevel.bg_rect.w + (scroll[0] / 8)
        loadlevel.bg_rect.y -= loadlevel.bg_rect.h + (scroll[1] / 8)
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
 
    
    # Gravity
    falling += grav_rate * -1
    if falling > GRAVITY * -1: falling = GRAVITY * -1
    pos[1] += falling
        
    # Draw the level
    x = 0
    i = 0 
    for i in loadlevel.map:
        # Render Tiles
        if loadlevel.themeparser.get(i, "tile"):
            
            tile = loadlevel.themeparser.get(i, "tile")
            tile = tile.split(",")
            tile_x = ((x % loadlevel.mapwidth) * loadlevel.tilesize[0])
            tile_y = (math.floor(x / loadlevel.mapwidth) * loadlevel.tilesize[1])
            screen.blit(loadlevel.tile_table[int(tile[0])][int(tile[1])], (tile_x + scroll[0], tile_y + scroll[1] ) )

            
        # Collision with a tile
        if loadlevel.themeparser.getboolean(i,"collide"):
            col = loadlevel.collision(chomp.colliderect,x)
            tilename = loadlevel.themeparser.get(i, "name")
            if col:
                if tilename == "spring":
                    falling = loadlevel.themeparser.getint(i, "value") * -1
                else:
                    tilerect = pygame.Rect(tile_x,tile_y,loadlevel.tilesize[0],loadlevel.tilesize[1])  
                    offset = [chomp.colliderect.x - tilerect.x, chomp.colliderect.y - tilerect.y]
                    print offset
                    
                    if abs(offset[1]) <  loadlevel.tilesize[1] / 2:
                        if offset[0] >  loadlevel.tilesize[0] / 2: pos[0] = tilerect.x + loadlevel.tilesize[0]
                        elif offset[0] <=  loadlevel.tilesize[0] / 2: pos[0] = tilerect.x - loadlevel.tilesize[0]
                        speed = 0
                        
                    if abs(offset[0]) < loadlevel.tilesize[0] / 2:
                        if offset[1] > 0: pos[1] = tilerect.y + loadlevel.tilesize[1]
                        elif offset[1] <= 0: pos[1] = tilerect.y -  loadlevel.tilesize[1]
                        falling = 0                
                   
        x += 1
  
    
    # Update position to account for scrolling

    chomp.colliderect.x = pos[0]
    chomp.colliderect.y = pos[1]
       
    chomp.rect.x=pos[0] + scroll[0]
    chomp.rect.y=pos[1] + scroll[1]
          
    # Limit to 20 frames per second
    clock.tick(20)

   	# Draw Sprites
    all_sprites_list.draw(screen)
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit ()

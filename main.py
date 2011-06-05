
import pygame, math, chompy, gamemap, dialog
 
# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
 
pygame.init()
  

size=[800,600]
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
chomp.pos[0] = int(pos[0]) * loadlevel.tilesize[0]
chomp.pos[1] = int(pos[1]) * loadlevel.tilesize[1]
chomp.colliderect.x = chomp.pos[0]
chomp.colliderect.y = chomp.pos[1]


move = 0


dialog = dialog.Dialog()
dialog.setMessageBox(size,"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus commodo ornare semper. Pellentesque libero massa, luctus vitae fermentum vitae, venenatis ac nunc. Proin a ipsum est. Sed nunc velit, faucibus a molestie eget, elementum quis velit. Nunc odio ante, vehicula eget scelerisque a, tincidunt nec ante. Praesent nisi risus, tristique id ultricies vel, tincidunt sed tortor. Phasellus hendrerit nisl at urna fringilla ultrices. Praesent dignissim mauris at velit pellentesque aliquam. Aliquam ut purus ac lorem gravida elementum ac in lectus. Duis hendrerit justo semper felis mollis sit amet fermentum ipsum pulvinar.","Test Level 1", [['Quit >>> >>',pygame.quit],['Long Ass Button',pygame.quit]] )

chomp.update(scroll,move,size)
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
            if event.key == 292: pygame.display.toggle_fullscreen()
 
     
    lscroll = scroll
    scroll = [(size[0] / 2) - chomp.pos[0] , (size[1] / 2) - chomp.pos[1] ]        

    
    # Draw the background
    screen.fill(white) 
    loadlevel.drawBackground(screen,scroll)
  
    # Draw tiles and handle tile collision with player
    loadlevel.updateTiles(screen,scroll,clock,chomp)
          
    # Limit to 30 frames per second
    clock.tick(30)

   	# Draw Sprites
    all_sprites_list.draw(screen)

    # Chomp Movement
    if not dialog.drawBox(screen,size):
        chomp.update(scroll,move,size)    
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit ()

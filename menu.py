"""
    UpChomp - A momentum game staring Chompy
    Copyright (C) 2011 Nathan Ogden
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pygame, math, sys, os, iniget, dialog, imagehelper, time, hashlib

# Image Helper Object
imghelp = imagehelper.imageHelper()

# Attempt to load Android modules.
try:
    import android, android_mixer
except ImportError:
    android = None
    
TILE_SIZE = [32,32]    

class Menu(object):
    def __init__(self, screen, sound, clock, save):
    
        """
        Inits the menu object for handling the title screen
        and map pack select.
        
        @param pygame.screen screen - Pygame screen object.
        @param object sound - Sound handler object.
        @param pygame.time - Pygame time object.
        @param object save - Ini Object for saving game data.
        """    

        # Dialog
        self.dialog = dialog.Dialog(screen, sound)
        
        # Scroll Arrows
        scrollarrows = pygame.image.load("gfx/scroll_arrows.png").convert_alpha()
        image_width, image_height = scrollarrows.get_size()
        tile_image_size = [image_width,image_height]
        self.scrollarrows_vertical = imghelp.makeTiles(scrollarrows, TILE_SIZE)    
        self.scrollarrows_horizontal = imghelp.makeTiles(scrollarrows, TILE_SIZE) 

        # Scroll Arrows [Rotate 90 degrees]
        for x in range(len(self.scrollarrows_horizontal)):
            for y in range(len(self.scrollarrows_horizontal[x])):
                self.scrollarrows_horizontal[x][y] = pygame.transform.rotate(self.scrollarrows_horizontal[x][y], 90)        
                
        # Load font
        self.font = pygame.font.Font("font/volter.ttf",18)
        self.titlefont = pygame.font.Font("font/volter2.ttf",28)
        
        # Load background
        self.background = pygame.image.load("gfx/menu_bg.png").convert()
        self.bg_rect = self.background.get_rect()  
        self.bgoffset = 0  
        
        # Check mark image
        self.checkmark = pygame.image.load("gfx/packcomplete.png").convert_alpha()
        
        # High Rank Image
        self.highrank = pygame.image.load("gfx/toprank.png").convert_alpha()
        
        # Get Sound Object
        self.sound = sound  
        
        # Get Screen Object
        self.screen = screen
        
        # Get Clock Object
        self.clock = clock
        
        # Load Save Ini
        self.save = save
    
    def titleScreen(self):
    
        """
        Title screen state, renders title screen.
        """
    
        done = 0
        menu_end_state = 0
        
        # self.screen size
        size = self.screen.get_size()

        # Set Title self.screen Message
        self.font_data = [ "Tap to Start", 0, [0,0] ]
        if not android: self.font_data[0] = "Press Any Key to Start"
        self.font_data[1] = self.font.size(self.font_data[0])
                           
        # Load Title Logo
        self.title_logo_a = pygame.image.load("gfx/title_logo_layer1.png").convert_alpha()
        self.title_logo_b = pygame.image.load("gfx/title_logo_layer2.png").convert_alpha()

        # Size stuff to fit self.screen
        self.resizeTitle(size)
                
        title_logo_pos_a = self.tl_rect_a.x
        title_logo_pos_b = self.tl_rect_b.x
        title_logo_offset_a = self.tl_rect_a.x - size[0]
        title_logo_offset_b = self.tl_rect_a.x + size[0]
 
        # Play Menu Music
        self.sound.playSfx("sfx/danosongs.com-helium-hues.ogg", -1, 1)
        
        while not done:
            # Set frame rate to 30.
            self.clock.tick(30)
            events = pygame.event.get()

            # Android events
            if android:
                if android.check_pause():
                    android.wait_for_resume()


            rState = 2
            for event in events: # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop
                    rState = -1 # Set game state to -1(Quit)

                elif event.type == pygame.VIDEORESIZE:
                    self.resizeTitle(event.size)

                elif (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN) and not ((title_logo_offset_a < title_logo_pos_a and not menu_end_state) or (title_logo_offset_a > title_logo_pos_a and menu_end_state)) :
                    menu_end_state = 1
                    title_logo_pos_a = self.tl_rect_a.x - size[0]
                    title_logo_pos_b = self.tl_rect_b.x + size[0]       
                    title_logo_offset_a = self.tl_rect_a.x 
                    title_logo_offset_b = self.tl_rect_a.x   
                    self.sound.playSfx("sfx/button.wav",0)           


            self.renderBg(size)
            
            # Title Logo offset
            if (title_logo_offset_a < title_logo_pos_a and not menu_end_state) or (title_logo_offset_a > title_logo_pos_a and menu_end_state):
                if menu_end_state: title_logo_offset_a -= 32
                else: title_logo_offset_a += 32
                
                self.tl_rect_a.x = title_logo_offset_a

            if (title_logo_offset_b > title_logo_pos_b and not menu_end_state) or (title_logo_offset_b < title_logo_pos_b and menu_end_state):
                if menu_end_state: title_logo_offset_b += 32
                else: title_logo_offset_b -= 32
                
                self.tl_rect_b.x = title_logo_offset_b
            elif menu_end_state: done = 1
                        
            
            # Title Logo
            self.screen.blit(self.title_logo_sized_b, self.tl_rect_b)
            self.screen.blit(self.title_logo_sized_a, self.tl_rect_a)     
            
            # Start Text
            
            self.screen.blit( self.font.render(self.font_data[0], 0, [0,0,0]), (self.font_data[2][0] + 2, self.font_data[2][1] + 2) )
            self.screen.blit( self.font.render(self.font_data[0], 0, [255,255,255]), (self.font_data[2][0], self.font_data[2][1]) )
            
            
            # Go ahead and update the self.screen with what we've drawn.
            pygame.display.flip()
        
        return rState
            
    def resizeTitle(self, size):
    
        """
        Resizes title screen logo.
        
        @param array size - Width and height of game window.
        """
    
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        tl_rect_big = self.title_logo_a.get_rect()

        self.bgrows = 2
        self.bgcols = 2
        if size[1] > self.bg_rect.h: self.bgrows = int(math.ceil(size[1] / self.bg_rect.h) * 2) + 1
        if size[0] > self.bg_rect.w: self.bgcols = int(math.ceil(size[0] / self.bg_rect.w) * 2) + 1
        self.bg_rect.x = 0
        self.bg_rect.y = 0

        # Resize title logo, we're counting on the aspect ratio being 1:1.
        if size[0] > size[1]:
            self.title_logo_sized_a = pygame.transform.smoothscale(self.title_logo_a, (size[1], size[1]))
            self.title_logo_sized_b = pygame.transform.smoothscale(self.title_logo_b, (size[1], size[1]))
        else:
            self.title_logo_sized_a = pygame.transform.smoothscale(self.title_logo_a, (size[0], size[0]))
            self.title_logo_sized_b = pygame.transform.smoothscale(self.title_logo_b, (size[0], size[0]))

        self.tl_rect_a = self.title_logo_sized_a.get_rect()
        self.tl_rect_a.x = (size[0] / 2) - (self.tl_rect_a.w / 2)
        self.tl_rect_a.y = (size[1] / 2) - (self.tl_rect_a.h / 2)   
        
        self.tl_rect_b = self.title_logo_sized_b.get_rect()
        self.tl_rect_b.x = self.tl_rect_a.x
        self.tl_rect_b.y = self.tl_rect_a.y
        
        # Move Title Font...
        self.font_data[2] = [ (size[0] / 2) - (self.font_data[1][0] / 2), size[1] - (self.font_data[1][1] * 1.5) ]
        
    def renderBg(self, size):
        
        """
        Renders the menu background.
        
        @param array size - Width and height of game window.
        """
    
        # Background
        self.bg_rect.x -= self.bg_rect.w - self.bgoffset
        self.bg_rect.y -= self.bg_rect.h - self.bgoffset
        
        for yy in xrange(self.bgrows):
            for xx in xrange(self.bgcols):
                # Start a new row
                if xx == 0 and yy > 0:
                    # Move the rectangle
                    self.bg_rect = self.bg_rect.move([-(self.bgcols -1 ) * self.bg_rect.w, self.bg_rect.h])
                # Continue a row
                if xx > 0:
                    # Move the rectangle
                    self.bg_rect = self.bg_rect.move([self.bg_rect.w, 0])
                
                self.screen.blit(self.background, self.bg_rect)
                
        self.bg_rect.x = 0
        self.bg_rect.y = 0     

        # Menu offset...makes the animation happen.
        self.bgoffset -= .5
        if self.bgoffset < -20: self.bgoffset = 0           

    def mapSelect(self):
        
        """
        Map pack select state.
        
        @return int - Next game state.
        """
    
        done = 0
           
        # self.screen size
        size = self.screen.get_size()
        
        # Vars to Use
        bgoffset = 0
        map_list_scroll = 0
        map_selected = 0
        stage_selected = 0
        
        # Static Vars
        LIST_SPACING = 32
        LIST_START_POS = 92
        
        # Map Select Arrow
        maparrow = pygame.image.load("gfx/map_select_arrow.png").convert_alpha()
        
        # Load Map List
        mapFiles = os.listdir("./map")
        mapList = []
        
        for i in mapFiles:
            ext = i.split(".")
            if ext[len(ext) - 1] == "map":
                ini = iniget.iniGet("./map/" + i)
                totalmaps = len(ini.get("pack","order").split(","))
                maphash = hashlib.sha224(open("map/" + i).read()).hexdigest()
                
                highrank = 1
                for x in ini.get("pack","order").split(","):
                    record = self.save.getFloat(maphash, x)
                    ranktime = ini.getFloat(x, "arank")
                    if not record <= ranktime: highrank = 0
                
                if self.save.getInt(maphash, "progress") == totalmaps: complete = 1
                else: complete = 0
                                  
                mapList.append([i, ini.get("pack", "name"), complete, highrank])
                
        returnVal = -1
        
        # Get Sizes of Buttons...
        btnsize = self.dialog.getButtonSize("Next")
        btnsize2 = self.dialog.getButtonSize("Back")
        mouse = [0, 0]
        
        # Update BG Size
        self.resizeTitle(size)
        
        # Play Menu Music
        self.sound.playSfx("sfx/danosongs.com-helium-hues.ogg", -1, 1)
        
        while not done:
            # Set frame rate to 30.
            self.clock.tick(30)
            events = pygame.event.get()

            # Android events
            if android:
                if android.check_pause():
                    android.wait_for_resume()

            mouse_click = [0, 0]
            for event in events: # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE:
                    self.resizeTitle(event.size)
                    size = event.size
                    map_list_scroll = 0
                    map_selected = 0                    
                    
                elif event.type == pygame.MOUSEMOTION:
                    mouse = event.pos

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = event.pos
                    x = 0
                    for i in mapList:
                        fontSize = self.font.size(i[1])
                        rect = pygame.Rect(64, x * LIST_SPACING + LIST_START_POS - (map_list_scroll * LIST_SPACING), fontSize[0], fontSize[1])
                        if rect.collidepoint(event.pos[0], event.pos[1]):
                            map_selected = x
                            self.sound.playSfx("sfx/beep.wav", 0)
                        x += 1 
                        
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        map_selected -= 1
                        self.sound.playSfx("sfx/beep.wav", 0)
                        if map_selected < 0: map_selected = 0
                        if scroll_down and map_selected < map_list_scroll: map_list_scroll = map_selected
                    elif event.key == pygame.K_DOWN:
                        map_selected += 1
                        self.sound.playSfx("sfx/beep.wav", 0)
                        if map_selected > len(mapList) - 1: map_selected = len(mapList) - 1                       
                        if scroll_down and map_selected > map_list_scroll: map_list_scroll = map_selected

                   
            # Render the background
            self.renderBg(size)
            
            # Title Text
            
            self.screen.blit( self.titlefont.render("Pack Select", 0, [0,0,0]), (34,34) )
            self.screen.blit( self.titlefont.render("Pack Select", 0, [255,179,0]), (32,32) )
            
            # Map List
            
            x = 0
            scroll_down = 0
            max_text_width = 0
            cut_off = 0
            for i in mapList:
                pos = [64, x * LIST_SPACING + LIST_START_POS - (map_list_scroll * LIST_SPACING) ]
                if self.font.size(i[1])[0] > max_text_width: max_text_width = self.font.size(i[1])[0]                
                if not pos[1] > size[1] - 64 and not pos[1] < 64:                    
                    self.screen.blit( self.font.render(i[1], 0, [0,0,0]), (pos[0] + 2, pos[1] + 2) )
                    self.screen.blit( self.font.render(i[1], 0, [255,255,255]), (pos[0], pos[1]) )
                    
                    # If map pack completed, display emblem
                    if i[2]:
                        textsize = self.font.size(i[1])
                        self.screen.blit( self.checkmark, (pos[0] + textsize[0] + (TILE_SIZE[0] / 4), pos[1]) )
                        
                        # If all maps completed with high rank, display emblem
                        if i[3]:
                            self.screen.blit( self.highrank, (pos[0] + textsize[0] + 16 + (TILE_SIZE[0] / 2), pos[1]) )
                       
                        
                else: 
                    scroll_down = 1
                    cut_off += 1
                x += 1
                
            # Render scroll down arrow
            if scroll_down and not map_list_scroll >= cut_off:
                pos = [max_text_width + 78, size[1] - 92]
                rect = pygame.Rect(pos[0], pos[1], TILE_SIZE[0], TILE_SIZE[1])
                if not rect.collidepoint(mouse[0], mouse[1]):
                    self.screen.blit( self.scrollarrows_vertical[0][0], (pos[0], pos[1]) )
                else: 
                    self.screen.blit( self.scrollarrows_vertical[1][0], (pos[0], pos[1]) )
                    if rect.collidepoint(mouse_click[0], mouse_click[1]):
                        map_list_scroll += 1  
                        if map_list_scroll > cut_off: map_list_scroll = cut_off
                                
            # Render scroll up arrow
            if map_list_scroll > 0:
                pos = [max_text_width + 78, 64]
                rect = pygame.Rect(pos[0], pos[1], TILE_SIZE[0], TILE_SIZE[1])
                if not rect.collidepoint(mouse[0], mouse[1]):
                    self.screen.blit( self.scrollarrows_vertical[0][1], (pos[0], pos[1]) )
                else: 
                    self.screen.blit( self.scrollarrows_vertical[1][1], (pos[0], pos[1]) )
                    if rect.collidepoint(mouse_click[0], mouse_click[1]) and map_list_scroll > 0:
                        map_list_scroll -= 1
                        
            # Map Selected Arrow
            if map_selected < map_list_scroll: map_selected = map_list_scroll
            self.screen.blit(maparrow, ( 32, LIST_START_POS + (LIST_SPACING * map_selected) - (LIST_SPACING * map_list_scroll)   ) )
 
            # Dialog Box
            if not self.dialog.drawBox(size, events):
                       
                # If next clicked load selected level
                if self.dialog.makeButton("Play", [ size[0] - btnsize[0] - (LIST_SPACING * 1.5) , size[1] - (LIST_SPACING * 1.5) ], size, events, 1):
                    stage_selected = self.stageSelect(mapList[map_selected][0])
    
                    if stage_selected > 0:
                        returnVal = mapList[map_selected][0]
                        done = 1
                    else:
                        size = self.screen.get_size()
                        self.resizeTitle(size)
    
                elif not stage_selected and self.dialog.makeButton("Quit", [ size[0] - btnsize2[0] - btnsize[0] - (LIST_SPACING * 1.5) , size[1] - (LIST_SPACING * 1.5) ], size, events, 0):
                    pygame.quit()
                    sys.exit()
                    
                else: stage_selected = 0          
                                       
            # Go ahead and update the self.screen with what we've drawn.
            pygame.display.flip()     
        return [returnVal, stage_selected - 1]
    
    def stageSelect(self, mappack):
    
        """
        Map pack stage select state.
        
        @param string mappack - Map pack file.
        @return int - Selected stage.
        """
        
        selected_stage = 0
        current_selection = 0
        
        # self.screen size
        size = self.screen.get_size()

        # Get Sizes of Buttons...
        btnsize = self.dialog.getButtonSize("Play")
        btnsize2 = self.dialog.getButtonSize("Back")  
 
        scroll_right_collide = 0
        scroll_left_collide = 0
        mouse = [0, 0]
        
        # Static Vars
        LIST_SPACING = 32
        LIST_START_POS = 92         
                                
        # Get map pack info
        pack = iniget.iniGet("map/" + mappack)
        maplist = pack.get("pack","order").split(",")
        
        maphash = hashlib.sha224(open("map/"+mappack).read()).hexdigest()
        current_selection = self.save.getInt(maphash, "progress")
        progress = current_selection
       
        map = []
        for i in maplist:
            cmap = pack.get(i, "map").replace(" ", "").split("\n")
            
            width = 0
            height = len(cmap)
            
            tiles = []
            for x in cmap:
                if len(x) > width: width = len(x)
                for y in range(len(x)):
                    tiles.append(x[y])    
                    
            theme = iniget.iniGet("tile/" + pack.get(i, "theme") + ".ini")
            tile_draw = []
            for x in tiles:
                if theme.getBool(x, "collide") and not theme.get(x, "type"):
                    # Floor/Wall Block
                    tile_draw.append(1)
                elif theme.get(x, "type") == "goal":
                    # Goal Block
                    tile_draw.append(2)
                else:
                    # Air
                    tile_draw.append(0)                                    
        
            map.append({
                'tiles'     :   tile_draw,
                'name'      :   pack.get(i, "name"),
                'startpos'  :   pack.get(i, "startpos").split(","),
                'width'     :   width,
                'height'    :   height,
                'record'    :   self.save.getFloat(maphash, i),
                'toprank'   :   pack.getFloat(i, "arank")
            })

        # Upon completing the last map the current selection will become one higher, fix it!
        if current_selection > len(map) - 1: current_selection = len(map) - 1
            
        draw_map = 1  
        
        while not selected_stage:
           # Set frame rate to 30.
            self.clock.tick(30)
            events = pygame.event.get()

            # Android events
            if android:
                if android.check_pause():
                    android.wait_for_resume()

            mouse_click = [0, 0]                    
            for event in events: # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.VIDEORESIZE:
                    self.resizeTitle(event.size)
                    size = event.size
                    draw_map = 1
                    
                elif event.type == pygame.MOUSEMOTION:
                    mouse = event.pos                
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = event.pos
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        current_selection += 1
                        if current_selection > len(map) - 1: current_selection = len(map) - 1
                        
                        # Can't go past maps you haven't completed.
                        if current_selection > progress: current_selection = progress
                        draw_map = 1
                    elif event.key == pygame.K_DOWN:
                        current_selection -= 1
                        if current_selection < 0: current_selection = 0
                        draw_map = 1
                
            if draw_map:
                map_render_size = 20
                map_w, map_h = [9999, 9999]
                
                while map_w > size[0] - (TILE_SIZE[0] * 4) or map_h > size[1] - 256:
                    map_render_size -= 1
                    if map_render_size <= 1: break
                    map_w = map[current_selection]['width'] * map_render_size + (map_render_size * 2)
                    map_h = map[current_selection]['height'] * map_render_size + (map_render_size * 2)                 
                
                map_surface = pygame.Surface((map_w, map_h))
                    
                x = 0
                y = 0            
                     
                for i in map[current_selection]['tiles']:
                    
                    # Draw Floor/Wall
                    if i == 1:
                        pygame.draw.rect(map_surface, [255, 255, 255], pygame.Rect((x * map_render_size) + map_render_size, (y * map_render_size) + map_render_size, map_render_size, map_render_size))
                    # Draw Goal
                    elif i == 2:
                        pygame.draw.rect(map_surface, [0, 0, 255], pygame.Rect((x * map_render_size) + map_render_size, (y * map_render_size) + map_render_size, map_render_size, map_render_size))
                    # Draw Start Pos                
                    elif x == int(map[current_selection]['startpos'][0]) and y == int(map[current_selection]['startpos'][1]):
                        pygame.draw.rect(map_surface, [255, 0, 0], pygame.Rect((x * map_render_size) + map_render_size, (y * map_render_size) + map_render_size, map_render_size, map_render_size))    
                    
                    x += 1
                    if x >= map[current_selection]['width']:
                        x = 0
                        y += 1  
                        
                draw_map = 0                            
                                                                         
            # Render the background
            self.renderBg(size)
            
            # Title Text            
            self.screen.blit( self.titlefont.render("Stage Select", 0, [0,0,0]), (34,34) )
            self.screen.blit( self.titlefont.render("Stage Select", 0, [255,179,0]), (32,32) )
            
            # Render Map Preview                    
            self.screen.blit(map_surface, ( (size[0] / 2) - ((((map[current_selection]['width'] * map_render_size) / 2) + (map_render_size)  ) ) , (size[1] / 2) - ((map[current_selection]['height'] * map_render_size) / 2)))
            
            # Render Map Name
            mapnamesize = self.font.size(map[current_selection]['name'])
            map_title_pos = [(size[0] / 2) - (mapnamesize[0] / 2), (size[1] / 2) - ((map[current_selection]['height'] * map_render_size) / 2) - mapnamesize[1] * 1.5 ]
            self.screen.blit( self.font.render(map[current_selection]['name'], 0, [0,0,0]), ( map_title_pos[0] + 1, map_title_pos[1] + 1 ) )
            self.screen.blit( self.font.render(map[current_selection]['name'], 0, [255,179,0]), ( map_title_pos[0], map_title_pos[1]))
            
            # Render Stats
            if map[current_selection]['record']:
                timesize = self.font.size("Best Time: " + str(map[current_selection]['record']))
                timepos = [(size[0] / 2) - (timesize[0] / 2), (size[1] / 2) - ((map[current_selection]['height'] * map_render_size) / 2) + map_h + 16 ]
                self.screen.blit( self.font.render("Best Time: " + str(map[current_selection]['record']), 0, [0,0,0]), ( timepos[0] + 1, timepos[1] + 1 ))
                self.screen.blit( self.font.render("Best Time: " + str(map[current_selection]['record']), 0, [255,179,0]), ( timepos[0], timepos[1]))          
                
                if map[current_selection]['record'] <= map[current_selection]['toprank']:
                    self.screen.blit(self.highrank, (timepos[0] + timesize[0] + (TILE_SIZE[0] / 4), timepos[1] ) )
            
            # Buttons                           
            if self.dialog.makeButton("Back", [ size[0] - btnsize2[0] - btnsize[0] - (LIST_SPACING * 1.5) , size[1] - (LIST_SPACING * 1.5) ], size, events, 0):
                selected_stage = -1

            elif self.dialog.makeButton("Play", [ size[0] - btnsize[0] - (LIST_SPACING * 1.5)  , size[1] - (LIST_SPACING * 1.5) ], size, events, 1):
                selected_stage = current_selection + 1

            # Render scroll right arrow
            if current_selection < len(map) - 1 and current_selection < progress:
                pos = [size[0] - (TILE_SIZE[0] * 2), (size[1] / 2) - (TILE_SIZE[1] / 2) ]
                rect = pygame.Rect(pos[0] - TILE_SIZE[0], pos[1] - TILE_SIZE[1], TILE_SIZE[0] * 4, TILE_SIZE[1] * 4)
                
                if not rect.collidepoint(mouse[0], mouse[1]):
                    self.screen.blit( self.scrollarrows_horizontal[0][0], (pos[0], pos[1]) )
                else: 
                    self.screen.blit( self.scrollarrows_horizontal[1][0], (pos[0], pos[1]) )
                    if rect.collidepoint(mouse_click[0], mouse_click[1]):
                        if current_selection < len(map) - 1:
                            current_selection += 1
                            draw_map = 1
          
            # Render scroll left arrow
            if current_selection > 0:
                pos = [TILE_SIZE[0], (size[1] / 2) - (TILE_SIZE[1] / 2)]
                rect = pygame.Rect(pos[0] - TILE_SIZE[0], pos[1] - TILE_SIZE[1], TILE_SIZE[0] * 4, TILE_SIZE[1] * 4)

                if not rect.collidepoint(mouse[0], mouse[1]):
                    self.screen.blit( self.scrollarrows_horizontal[0][1], (pos[0], pos[1]) )
                else: 
                    self.screen.blit( self.scrollarrows_horizontal[1][1], (pos[0], pos[1]) )
                    if rect.collidepoint(mouse_click[0], mouse_click[1]):
                        if current_selection > 0:
                            current_selection -= 1                            
                            draw_map = 1
                                                              
                                        
            # Go ahead and update the self.screen with what we've drawn.
            pygame.display.flip()                
            
        return selected_stage            

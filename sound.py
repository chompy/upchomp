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

try:
    import android_mixer as mixer
except ImportError:
    import pygame.mixer as mixer

class Sound(object):
    def __init__(self):
    
        """ Inits the sound handler object. """
    
        # Init pygame mixer.
        mixer.init()
        self.sfx = {
            0:  ['', mixer.Channel(1), 0, 0, 0],
            1:  ['', mixer.Channel(2), 0, 0, 0],
            2:  ['', mixer.Channel(3), 0, 0, 0],
            3:  ['', mixer.Channel(4), 0, 0, 0]
        }
        
    def update(self):
    
        """
        Check for sounds that need to loop, if they've stopped
        playing restart them. Android needs this, PCs shouldn't.
        """
    
        for i in range(len(self.sfx)):
            if not self.sfx[i][1].get_busy():
                if self.sfx[i][3] > 0 or self.sfx[i][3] == -1:
                    self.sfx[i][1].stop()
                    self.sfx[i][1].play(self.sfx[i][2], self.sfx[i][3])
                if self.sfx[i][3] > 0: self.sfx[i][3] -= 1            
          
                
    def playSfx(self, file, loop, isMusic = 0):
    
        """
        Plays a sound.
        
        @param string file - File name of SFX.
        @param int loop - How many times to repeat sound, -1 for infinite.
        @param bool isMusic - If true mark this sound as music.
        """
    
        is_playing = 0

        for i in range(len(self.sfx)):
            if self.sfx[i][1].get_busy():
                if self.sfx[i][0] == file: is_playing = 1
                elif not file == self.sfx[i][0] and self.sfx[i][4] and isMusic: 
                    self.sfx[i][1].stop()
                    self.sfx[i][0] = ""
                    self.sfx[i][4] = 0
                    
            else: 
                self.sfx[i][0] = ""                     
                self.sfx[i][4] = 0
                

        if not is_playing:
            for i in range(len(self.sfx)):
                if not self.sfx[i][1].get_busy():
                    self.sfx[i][0] = file
                    self.sfx[i][2] = mixer.Sound(file)
                    self.sfx[i][3] = loop
                    self.sfx[i][4] = isMusic
                    self.sfx[i][1].play(self.sfx[i][2], loop)
                    break

    def stopSfx(self, channel):
    
        """
        Stops sound on a specific channel from playing.
        
        @param int channel - Channel to stop.
        """
    
        self.sfx[channel][1].stop()

    def stopAllSfx(self, exceptMusic = 1, onlyLoops = 0):
    
        """
        Stops all sounds.
        
        @param bool exceptMusic - If true doesn't stop sounds marked as music.
        @param bool onlyLoops - If true only stops sounds that are looping.
        """
    
        for i in range(len(self.sfx)):
            if self.sfx[i][1].get_busy() and ((self.sfx[i][4] and not exceptMusic) or (exceptMusic and not self.sfx[i][4])):
                if (onlyLoops and self.sfx[i][3]) or not onlyLoops:
                    self.sfx[i][1].stop()
                    self.sfx[i][0] = ""
                    self.sfx[i][3] = 0

    def stopSfxFile(self, file):
        
        """
        Stops a specific sound file from play.
        
        @param string file - Sound file.
        """
        
        for i in range(len(self.sfx)):
            if self.sfx[i][0] == file:
                self.sfx[i][0] = ""
                self.sfx[i][3] = 0
                self.sfx[i][1].stop()

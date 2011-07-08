try:
    import android_mixer as mixer
except ImportError:
    import pygame.mixer as mixer

class Sound(object):
    def __init__(self):
        mixer.init()
        self.sfx = {
            0:  ['', mixer.Channel(1), 0, 0, 0],
            1:  ['', mixer.Channel(2), 0, 0, 0],
            2:  ['', mixer.Channel(3), 0, 0, 0],
            3:  ['', mixer.Channel(4), 0, 0, 0]
        }
        
    def update(self):
        for i in range(len(self.sfx)):
            if not self.sfx[i][1].get_busy():
                if self.sfx[i][3] > 0 or self.sfx[i][3] == -1:
                    self.sfx[i][1].stop()
                    self.sfx[i][1].play(self.sfx[i][2], self.sfx[i][3])
                if self.sfx[i][3] > 0: self.sfx[i][3] -= 1            
          
                
    def playSfx(self, file, loop, isMusic = 0):
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
        self.sfx[channel][1].stop()

    def stopAllSfx(self, exceptMusic = 1, onlyLoops = 0):
        for i in range(len(self.sfx)):
            if self.sfx[i][1].get_busy() and ((self.sfx[i][4] and not exceptMusic) or (exceptMusic and not self.sfx[i][4])):
                if (onlyLoops and self.sfx[i][3]) or not onlyLoops:
                    self.sfx[i][1].stop()
                    self.sfx[i][0] = ""
                    self.sfx[i][3] = 0

    def stopSfxFile(self, file):
        for i in range(len(self.sfx)):
            if self.sfx[i][0] == file:
                self.sfx[i][0] = ""
                self.sfx[i][3] = 0
                self.sfx[i][1].stop()

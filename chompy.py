import pygame, math, imagehelper

# Image Helper Object
imghelp = imagehelper.imageHelper()

# Constants
GRAVITY = -9.81
grav_rate = GRAVITY / 20
max_speed = 6.0
speed_rate = max_speed / 10

TILE_SIZE = [32,32]

class Chompy(pygame.sprite.Sprite):
    def __init__(self, screen, sound):

        """Load a Chompy sprite."""
        
        self.screen = screen
        self.sound = sound

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("gfx/chompy.png").convert_alpha()
        self.image2 = self.image
        
        # Heli Skill tiles
        self.heli = pygame.image.load("gfx/heli.png").convert_alpha()
        self.heli_tiles = imghelp.makeTiles(self.heli, TILE_SIZE)

        self.progress = pygame.Surface((TILE_SIZE[0], 1))

        self.rect = self.image.get_rect()
        self.colliderect = pygame.Rect(self.rect.x, self.rect.x, self.rect.w, self.rect.h)

        self.moveok = 1
        self.stopclock = -1

        self.skills = {
            'heli'    : 0,
            'up'      : 0
        }

    def reset(self):

        """Resets Chompy back to his default state."""

        self.speed = 0.0
        self.falling = 0
        self.pos = [self.rect.x, self.rect.y]
        self.moveok = 1

        self.skills = {
            'heli'    : 0,
            'up'      : 0
        }


    def activateSkill(self, name):
        """
        Activates a Chompy skill!

        @param string name - Name of skill to activate.
        @return bool - True if skill was activated.
        """

        if name == "heli":
            self.skills['heli'] = 90
            self.progress_max = 90
            self.falling = -1

            if self.sound: self.sound.playSfx("sfx/heli.wav", -1)
            return 1
        elif name == "up":
            if self.sound: self.sound.playSfx("sfx/up.wav", 0)
            self.falling = -10
        else:
            return 0

    def update(self, scroll, move, size):

        """
        Updates Chompy's position.

        @param array scroll Screen scroll position.
        @param double move Direction player is attempt to make Chompy move in.
        @param array size Current screen size.
        """

        # Skills

        # Heli
        if self.skills['heli'] > 0:
            self.skills['heli'] -= 1
            ani = pygame.time.get_ticks() % 4

            self.screen.blit(self.heli_tiles[ani][0], (self.rect.x, self.rect.y - TILE_SIZE[1]))

            if self.falling > 0: self.falling = 0

        if self.skills['heli'] == 1: self.sound.stopSfxFile("sfx/heli.wav")

        # Start the clock when Chompy is not moving...if it hits 0 game over.
        if self.stopclock > 0:
            self.stopclock -= 1

        # Gravity [Ignore gravity when Heli skill is activate or Chompy is jumping]
        if not self.skills['heli'] or self.falling < 0:
            self.falling += (grav_rate) * -1
            if self.falling > GRAVITY * -1: self.falling = (GRAVITY * -1)
            self.pos[1] += self.falling

        # Movement
        if move and self.moveok:
            if move > 4: move = 4
            elif move < -4: move = -4

            if move > 0 and move < .5: move = .5
            elif move < 0 and move > -.5: move = -.5

            self.pos[0] += math.floor(self.speed)
            if move > 0 and self.speed < max_speed: self.speed += speed_rate
            if move < 0 and self.speed > max_speed * -1: self.speed -= speed_rate
 
        else:
            self.pos[0] += math.floor(self.speed)
            if abs(self.speed) < 1: self.speed = 0
            elif self.speed > 0: self.speed -= speed_rate / 4
            elif self.speed < 0: self.speed += speed_rate / 4

            
        # If Chompy goes up into the air reenable movement.
        if self.falling < 0 or self.falling > 1: self.moveok = 1

        # Update position
        self.colliderect.x = self.pos[0]
        self.colliderect.y = self.pos[1]

        self.rect.x= self.pos[0] + scroll[0]
        self.rect.y= self.pos[1] + scroll[1]

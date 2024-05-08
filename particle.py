import pygame as pg
import os,math
import mathFuncs.imgFuncs as imgF

#Game build associated with level generator
buildId = "id157.2"

class Particle(pg.sprite.Sprite):
    def __init__(self,xpos,ypos,animation,direction,gamePath):
        self.xpos = xpos
        self.ypos = ypos
        self.xoffset = 0
        self.yoffset = 0
        self.timeAlive = 0
        self.frame = 0
        self.type = animation
        self.direction = direction
        self.img = ''
        self.gamePath = gamePath
    def update(self):
        self.timeAlive += 1        
        if self.type == 'run':
            self.frame = math.floor(self.timeAlive/8)+1
            self.xoffset = -13*self.direction
            self.yoffset = -24
            if self.frame > 2:
                del (self)
                return True #del self
            self.img = pg.image.load(os.path.join(self.gamePath,"Images","Particles",str(self.type) + str(self.frame) + '.png'))
            self.img = imgF.img2x(self.img)
        return False
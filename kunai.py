import pygame as pg
import math
import os

import sensor

class Kunai(pg.sprite.Sprite):
    def __init__(self,xpos,ypos,xv,yv):
        self.xpos = xpos
        self.ypos = ypos
        self.xv = xv
        self.yv = yv
        self.gravity = 0.1
        self.stuck = False
        self.timeAlive = 0
        self.timeHoming = 0
        self.baseImage = pg.image.load(os.path.join(gamePath,"Images", "UI", "pixelkunai.png"))
        self.baseImage = pg.transform.scale2x(self.baseImage)
        self.kunaiSens = sensor.Sensor(self,level,levelSub,width)
        self.direction = 0
    def update(self):
        global kunais
        self.timeAlive += 1
        self.direction = cosTowardMouse(self.xv,self.yv)[2]
        self.image = pg.transform.rotate(self.baseImage,-math.degrees(self.direction))
        self.yv += self.gravity
        if not self.stuck:
            self.xpos += self.xv
            self.ypos += self.yv
        if any(self.kunaiSens.detect(int(math.sin(i)*10),int(math.cos(i)*10))[0]==1 for i in range(-3,3,1)):
            #hit a wall
            self.stuck = True
            self.gravity = 0
        else:
            self.stuck = False
            self.gravity = 0.1
        if getDist(self.xpos,self.ypos,pl.xpos,pl.ypos)<300 and self.timeAlive>60:
            if self.timeHoming < 90:
                self.timeHoming += 1
            self.stuck = False
            self.xv = (self.xpos-pl.xpos)/-(18-(self.timeHoming/5))
            self.yv = (self.ypos-pl.ypos+50)/-(18-(self.timeHoming/5))
            if getDist(self.xpos,self.ypos,pl.xpos,pl.ypos)<60:
                kunais+=1
                spawnedKunai.pop(spawnedKunai.index(self))
                del(self)
        else:
            self.timeHoming = 0
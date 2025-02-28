import pygame as pg
import sensor, os, math
import mathFuncs.distFuncs as distF

#Kunai (throwing knife)
class Kunai(pg.sprite.Sprite):
    def __init__(self,xpos,ypos,xv,yv,gamePath,level,levelSub,width):
        self.xpos = xpos
        self.ypos = ypos
        self.xv = xv
        self.yv = yv
        self.gravity = 0.1125
        self.stuck = False
        self.timeAlive = 0
        self.timeHoming = 0
        self.baseImage = pg.transform.scale2x(pg.image.load(os.path.join(gamePath,"Images", "UI", "pixelkunai.png")))
        self.kunaiSens = sensor.Sensor(self,level,levelSub,width)
        self.direction = 0
    def update(self,plx,ply):
        self.timeAlive += 1
        self.direction = distF.cos(self.xv,self.yv)[2]
        self.image = pg.transform.rotate(self.baseImage,-math.degrees(self.direction))
        self.yv += self.gravity
        if not self.stuck:
            self.xpos += self.xv
            self.ypos += self.yv
        if any(self.kunaiSens.detect(int(math.sin(i)*12)+6,int(math.cos(i)*12)+10)[0]==1 for i in range(-3,3,1)):
            #hit a wall
            self.stuck = True
            self.gravity = 0
        else:
            #else fly through the air with low gravity
            self.stuck = False
        if distF.getDist(self.xpos,self.ypos,plx,ply)<300 and self.timeAlive>60:
            if self.timeHoming < 90:
                self.timeHoming += 1
            self.stuck = False

            #Retracts kunai to you when you get close. Effect gets stronger over 90 calls so its guarenteed to come back
            self.xv = (self.xpos-plx)/-(18-(self.timeHoming/5))
            self.yv = (self.ypos-ply+50)/-(18-(self.timeHoming/5)) #pl ypos + 50 so it goes to your head instead of feet

            #Delete instance if kunai is right next to you
            if distF.getDist(self.xpos,self.ypos,plx,ply)<60:
                del (self)
                return False
        else:
            self.timeHoming = 0
        return True
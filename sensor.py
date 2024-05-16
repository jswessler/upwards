import pygame as pg

buildId = 'id166.1'

class Sensor(pg.sprite.Sprite):
    def __init__(self,orig,level,levelSub,width): #Sensors are reset on loading a new level so its okay to put lvl data here
        self.orig = orig
        self.lvl = level
        self.lvls = levelSub
        self.wid = width
    
    def detect(self,x,y):
        xp = self.orig.xpos+x+self.orig.xv
        yp = self.orig.ypos+y+self.orig.yv
        block = (int(yp/32)*self.wid)+int(xp/32) #Find block in the level data (x*lvl width + y)
        ret = self.lvl[block] #Block type
        subtype = self.lvls[block] #Block subtype
        circ = [self.orig.xpos+x,self.orig.ypos+y] #Circle to draw when shown
        return [ret,block,subtype,circ]
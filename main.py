import pygame as pg
import math
from time import process_time
import numpy as np
from pygame import gfxdraw
import random
import os
import cv2
import time

import heart

import heartrate
#heartrate.trace(browser=True)

path = os.getcwd() #Path to game directory
idealFps = 60 #Target FPS for the game to aim for
buildIdentifier = "7/28/23-2" #Build Identifier

class Player(pg.sprite.Sprite):
    def __init__(self):
        self.xpos = WID/2
        self.ypos = HEI/2
        self.xv = 0
        self.yv = 0
        self.energy = 100
        self.facing = 0
        self.gravity = 1
        self.jCounter = 0
        self.abilities = [4,15,0,2,2] #Jump, Extended Jump, Double Jump, Dive, Jump Dive
        self.wallClimb = False
        self.onGround = True
        self.counter=0
        self.img = ''
        self.imgPos = [0,0]
        self.dFacing = 1
        self.animation = 'falling'
        self.nextAni = 'none'
        self.aniFrame=1
        self.aniTimer = 0
        self.aniiTimer = 0
        self.dt = 0

        #Collision Boxes. bottom, top, right, left
        #This list is in that order
        self.col = [12,-100,25,-25]
    
    def animations(self):
        if self.aniTimer>=0:
            self.aniTimer-=60/targetFps
        self.aniiTimer-=60/targetFps


        #Tumble Landing
        
        #Normal Landing
        if self.animation=='landed':
            if self.aniTimer<0:
                self.animation = 'none'
            self.img = pg.image.load(os.path.join(path,"Images","Aria","land.png"))
            self.img = pg.transform.scale_by(self.img,2)
            if self.dFacing==-1:
                self.img = pg.transform.flip(self.img,True,False)
            self.imgPos = [-36,-94]
        
        #Hard Landing
        elif self.animation=='hardlanded':
            if self.aniTimer<0:
                self.animation = 'none'
            if self.aniTimer>11:
                self.img = pg.image.load(os.path.join(path,"Images","Aria","hardland1.png"))
            elif self.aniTimer>7:
                self.img = pg.image.load(os.path.join(path,"Images","Aria","hardland2.png"))
            else:
                self.img = pg.image.load(os.path.join(path,"Images","Aria","hardland3.png"))
            self.img = pg.transform.scale_by(self.img,2)
            if self.dFacing==-1:
                self.img = pg.transform.flip(self.img,True,False)
            if self.aniTimer>11:
                self.imgPos = [-34,-94]
            elif self.aniTimer>7:
                self.imgPos = [-32,-66]
            else:
                self.imgPos = [-26,-94]

        #Phone Call



        #Ground Animations

        elif self.onGround:
            
            #Run
            if self.animation=='run' or abs(self.xv)>0.4:
                if self.aniTimer<0:
                    self.aniFrame+=1
                    if self.aniFrame==18:
                        self.aniFrame=1
                    self.aniTimer = int(4.25-abs(self.xv))
                self.img = pg.image.load(os.path.join(path,"Images","Aria","run" + str(self.aniFrame) + ".png"))
                self.img = pg.transform.scale_by(self.img,2)
                if self.dFacing==-1:
                    self.img = pg.transform.flip(self.img,True,False)
                self.imgPos = [-36,-94]
            
            #Idle
            elif self.animation=='none':
                if self.counter%60<16:
                    self.img = pg.image.load(os.path.join(path,"Images","Aria","idle1.png"))
                elif self.counter%60<31:
                    self.img = pg.image.load(os.path.join(path,"Images","Aria","idle2.png"))
                elif self.counter%60<47:
                    self.img = pg.image.load(os.path.join(path,"Images","Aria","idle3.png"))
                else:
                    self.img = pg.image.load(os.path.join(path,"Images","Aria","idle4.png"))
                self.img = pg.transform.scale_by(self.img,2)
                if self.dFacing==-1:
                    self.img = pg.transform.flip(self.img,True,False)
                self.imgPos = [-26,-100]
        


        #Air Animations

        else:
        #Hover
            if self.animation=='hover':
                self.nextAni='low'
                self.animation='none'
                if self.aniTimer<0:
                    self.aniFrame+=1
                    self.aniTimer=6
                if self.aniFrame>6:
                    self.aniFrame=1
                if self.energy>30:
                    if abs(self.xv)<0.5:
                        self.img = pg.image.load(os.path.join(path,"Images","Aria","hovern" + str(self.aniFrame) + ".png"))
                    else:
                        self.img = pg.image.load(os.path.join(path,"Images","Aria","hoverr" + str(self.aniFrame) + ".png"))
                else:
                    if abs(self.xv)<1:
                        self.img = pg.image.load(os.path.join(path,"Images","Aria","hovernl" + str(self.aniFrame) + ".png"))
                    else:
                        self.img = pg.image.load(os.path.join(path,"Images","Aria","hoverrl" + str(self.aniFrame) + ".png"))
                self.img = pg.transform.scale_by(self.img,2)
                if self.dFacing==-1:
                    self.img = pg.transform.flip(self.img,True,False)
                self.imgPos = [-26,-102]
            #Air Transitions

            elif self.yv>-0.5 and (self.nextAni=='high' or self.nextAni=='low') and not self.onGround: #If we have a queued animation
                if self.aniiTimer<0:
                    self.aniiTimer=13 

                #High Transition after Jump
                if self.nextAni=='high':
                    if self.aniiTimer<=0:
                        self.nextAni='none'
                        self.animation='falling'
                    #After 3 frames, go to standard falling animation
                    self.img = pg.image.load(os.path.join(path,"Images","Aria","jumptrans" + str(int((18-self.aniiTimer)/5)) + ".png"))
                    self.img = pg.transform.scale_by(self.img,2)
                    if self.dFacing==-1:
                        self.img = pg.transform.flip(self.img,True,False)
                    self.imgPos = [-26,-100]
                
                #Mid Transition after double jump
                elif self.nextAni=='mid':
                    if self.aniiTimer<=0:
                        self.nextAni='none'
                        self.animation='falling'
                    self.img = pg.image.load(os.path.join(path,"Images","Aria","lowtrans2.png"))
                    self.img = pg.transform.scale_by(self.img,2)
                    if self.dFacing==-1:
                        self.img = pg.transform.flip(self.img,True,False)
                    self.imgPos = [-26,-100]

                #Low transition after hover or dive jump
                elif self.nextAni=='low':
                    if self.aniiTimer<=0:
                        self.nextAni='none'
                        self.animation='falling'
                    self.img = pg.image.load(os.path.join(path,"Images","Aria","lowtrans" + str(int((18-self.aniiTimer)/5)) + ".png"))
                    self.img = pg.transform.scale_by(self.img,2)
                    if self.dFacing==-1:
                        self.img = pg.transform.flip(self.img,True,False)
                    self.imgPos = [-26,-100]
            else:
            
            #Air Animations ------

            #Walljump

            #Wallslide

            #Double Jump
                if self.nextAni=='djump':
                    self.animation='falling'
                    if self.aniTimer<0:
                        self.aniFrame+=1
                        self.aniTimer=3
                    if self.aniFrame>4:
                        self.nextAni='mid'
                    self.img = pg.image.load(os.path.join(path,"Images","Aria","djump" + str(min(3,self.aniFrame)) + ".png"))
                    self.img = pg.transform.scale_by(self.img,2)
                    if self.dFacing==-1:
                        self.img = pg.transform.flip(self.img,True,False)
                    self.imgPos = [-76,-116]
                
                #Djump transition (up)
                elif self.animation=='djumpup':
                    if self.aniTimer<0:
                        self.aniFrame+=1
                        self.aniTimer=3
                    if self.aniFrame>3:
                        self.aniFrame=1
                    if self.aniFrame==3:
                        self.nextAni='djump'
                        self.animation='none'
                    self.img = pg.image.load(os.path.join(path,"Images","Aria","djumpup" + str(min(2,self.aniFrame)) + ".png"))
                    self.img = pg.transform.scale_by(self.img,2)
                    if self.dFacing==-1:
                        self.img = pg.transform.flip(self.img,True,False)
                    self.imgPos = [-36,-94]
                
                #Djump transition (down)
                elif self.animation=='djumpdown':
                    if self.aniTimer<0:
                        self.aniFrame+=1
                        self.aniTimer=3
                    if self.aniFrame>2:
                        self.aniFrame=1
                    if self.aniFrame==2:
                        self.nextAni='djump'
                        self.animation='none'
                    self.img = pg.image.load(os.path.join(path,"Images","Aria","djumpdown" + str(min(2,self.aniFrame)) + ".png"))
                    self.img = pg.transform.scale_by(self.img,2)
                    if self.dFacing==-1:
                        self.img = pg.transform.flip(self.img,True,False)
                    self.imgPos = [-26,-116]
                    


                #Jump
                elif self.animation=='jump':
                    self.nextAni='high'
                    self.aniTimer=6
                    if self.counter%30<16:
                        self.img = pg.image.load(os.path.join(path,"Images","Aria","jumpup1.png"))
                    else:
                        self.img = pg.image.load(os.path.join(path,"Images","Aria","jumpup2.png"))
                    self.img = pg.transform.scale_by(self.img,2)
                    if self.dFacing==-1:
                        self.img = pg.transform.flip(self.img,True,False)
                    self.imgPos = [-26,-100]
                


                #Dive

                #Hover
                    

            #Falling Animations

                elif self.nextAni=='fastfall':
                    if self.aniTimer<0:
                        self.aniFrame+=1
                        self.aniTimer=(20-(2*self.yv))
                    if self.aniFrame>4:
                        self.aniFrame=1
                    self.img = pg.image.load(os.path.join(path,"Images","Aria","flail" + str(self.aniFrame) + ".png"))
                    self.img = pg.transform.scale_by(self.img,2)
                    if self.dFacing==-1:
                        self.img = pg.transform.flip(self.img,True,False)
                    self.imgPos = [-26,-116]

                elif self.nextAni=='fftrans':
                    if self.aniTimer<0:
                        self.nextAni='fastfall'
                    self.img = pg.image.load(os.path.join(path,"Images","Aria","fftrans.png"))
                    self.img = pg.transform.scale_by(self.img,2)
                    if self.dFacing==-1:
                        self.img = pg.transform.flip(self.img,True,False)
                    self.imgPos = [-26,-116]

                #Falling
                elif self.animation=='falling':
                    if self.aniTimer<0:
                        self.aniFrame+=1
                        self.aniTimer=5
                    if self.aniFrame>4:
                        self.aniFrame=1
                    if self.yv>4.25:
                        self.nextAni='fftrans'
                        self.animation='none'
                        self.aniTimer=9
                    self.img = pg.image.load(os.path.join(path,"Images","Aria","falling" + str(self.aniFrame) + ".png"))
                    self.img = pg.transform.scale_by(self.img,2)
                    if self.dFacing==-1:
                        self.img = pg.transform.flip(self.img,True,False)
                    self.imgPos = [-26,-116]

    #Run Every Frame
    def update(self,keys):
        self.counter+=60/targetFps
        self.dt+=240/targetFps

        for i in range(-96,16,32):
            for j in range(-12,12,12):
                det,bl,st = se.detect(j,i,True)
                playerCollisionDetection(det,bl,st)

        #For complicated reasons physics targets 240fps.
        #If we're running below 240fps then we do multiple physics steps per frame
        #We don't allow running above 240fps
        
        while self.dt>0:


            if self.jCounter>0:
                self.jCounter-=0.25
            
            eRegen = 0.175
            for heart in health:
                if heart.type==3:
                    eRegen*=1.25
                    self.energy+=0.025



            #Object Collision Detection

            #Ground Collision
            if any(se.detect(i,self.col[0],True)[0]==1 for i in range(-17,16,6)):
            
                if self.onGround==False:
                    self.ypos+=1
                    self.energy+=4
                    if 0.5<self.yv<4.5:
                        self.animation = 'landed'
                        self.aniTimer = 1+int(self.yv*2.5)
                    elif self.yv>4.5:
                        self.aniTimer = 20
                        self.animation = 'hardlanded'
                        if self.yv>7.75:
                            dealDmg(3)
                        elif self.yv>6.5:
                            dealDmg(2)
                        elif self.yv>5.75:
                            dealDmg(1)
                        
                self.onGround = True
                if self.animation=='hardlanded':
                    self.xv*=0.5
                self.yv = 0
                self.gravity = 0
                self.abilities[0] = 1
                self.abilities[1] = 15
                self.abilities[2] = 4
                self.abilities[3] = 2
                self.abilities[4] = 2
                self.energy+=eRegen
            else:
                self.onGround = False
                self.gravity = 1
                    

                #Up detection (only run when not on ground)
                if any(se.detect(i,self.col[1],True)[0]==1 for i in range(-22,23,11)): #Up
                    self.yv = 0
                    self.ypos+=1
                    self.jCounter=0
            
            #Right & Left Detection
            self.onWall=0
            if any(se.detect(self.col[2],i,True)[0]==1 for i in range(-90,20,10)): #Right
                self.onWall = 1
                self.xv = 0
            if any(se.detect(self.col[3],i,True)[0]==1 for i in range(-90,20,10)): #Left
                self.onWall = -1
                self.xv = 0

            #Energy Cap
            if self.energy>100:
                self.energy=100



            if keys[pg.K_SPACE] or keys[pg.K_UP]:

                #Main Single Jump
                if self.abilities[0]>0:
                    self.jCounter=(12-(3*self.abilities[0]))
                    self.abilities[0]-=0.25
                    self.yv-=(0.375+(0.0125*abs(self.xv)))
                    self.animation = 'jump'


                #Jump Extension
                if not self.onGround and self.abilities[0]<=0 and self.abilities[1]>0 and self.energy>0.175:
                    self.yv-=0.032
                    self.energy-=0.175
                    self.abilities[1]-=0.25


                #Hover
                if self.yv>0 and self.energy>0.1 and self.animation!='djumpdown':
                    self.yv-=0.015
                    self.yv*=0.97
                    self.jCounter=1
                    self.energy-=(0.06+(0.0125*abs(self.xv)))

                    self.animation = 'hover'

                
                #Double Jump
                if 0<self.abilities[2]<4 and not self.onGround and not self.wallClimb and self.abilities[0]<=0 and self.abilities[3]==2 and self.energy>0.8 and not self.wallClimb:
                    if self.yv>0:
                        self.yv*=0.25
                    self.yv-=0.325
                    self.abilities[2]-=0.25
                    self.energy-=0.8
                    self.jCounter=(8+(2*(7-self.abilities[2])))
                    self.aniFrame=1
                    if self.animation!='djumpdown' and self.animation!='djumpup':
                        if self.yv>0:
                            self.animation = 'djumpdown'
                        else:
                            self.animation = 'djumpup'


                #Jump out of dive
                if self.abilities[4]>0 and not self.onGround and self.abilities[0]<=0 and self.abilities[3]!=2 and self.energy>1:
                    self.yv*=0.925
                    self.yv-=0.45
                    self.xv*=0.95
                    self.abilities[4]-=0.25
                    self.abilities[3]=0
                    self.energy-=1
                    self.jCounter=4

                    self.animation = 'hover'

            #Logic when not pressing space    
            else:
                if 0<self.abilities[0]<4 and not self.onGround: #Lose your single jump if you let go of space
                    self.abilities[0]=0
                    self.abilities[1]=0
                if self.abilities[0]<=0 and self.abilities[2]==4: #Lose your double jump
                    self.abilities[2]=3
                    self.abilities[1]=0
                if 0<self.abilities[2]<3:
                    self.abilities[2]=0
                
                #Hop off of wall by letting go
                if self.wallClimb:
                    self.wallClimb = False

                #Slight hover at the end of jumps
                if self.yv>-1 and self.jCounter>0:
                    self.energy-=0.02
                    self.gravity = 0.45

            #Wall slide 
                if all(se.detect(self.facing*26,i,True)[0]==1 for i in range(-70,10,30)) and not self.onGround and self.facing!=0:
                    self.jCounter=6
                    self.wallClimb = True

                    #self.animation = 'wallslide'

            #Wall Jump
                if self.wallClimb and self.energy>6 and (((keys[pg.K_a] or keys[pg.K_LEFT]) and self.onWall==1) or ((keys[pg.K_d] or keys[pg.K_RIGHT]) and self.onWall==-1) or (keys[pg.K_SPACE] or keys[pg.K_UP])):
                    self.yv*=0.25
                    self.yv-=3.75
                    self.jCounter=16
                    self.xv = -self.facing*3
                    self.energy-=6
                    self.wallClimb = False
                    self.abilities[3]=2
                    self.abilities[4]=1
                    self.animation= 'jump'

            #Dive
            if keys[pg.K_LCTRL]:
                if self.abilities[3]==2 and self.abilities[0]<=0 and self.energy>10:
                    if self.xv>=0:
                        self.xv = 4.125
                    else:
                        self.xv = -4.125
                    self.yv-=1.5
                    self.abilities[2]=0
                    self.abilities[3]=1
                    self.energy-=10

                    self.animation = 'jump'


                #Dive Float
                elif self.abilities[3]==1 and not keys[pg.K_SPACE] and not keys[pg.K_UP] and self.energy>0.15:
                    self.xv*=1.013
                    self.yv*=0.9975
                    self.energy-=0.15

                    #self.animation = 'dive'
            
            #Directional Inputs
            self.facing = 0

            #On the ground, you have a lot more traction
            if self.onGround:
                if keys[pg.K_a] or keys[pg.K_LEFT] and self.onWall!=-1:
                    self.xv-=0.1225
                    self.facing = -1
                    self.animation='run'
                if keys[pg.K_d] or keys[pg.K_RIGHT] and self.onWall!=1:
                    self.xv+=0.1225
                    self.facing = 1
                    self.animation='run'
                self.xv*=0.96

            #In the air you have a lot less traction
            else:
                if keys[pg.K_a] or keys[pg.K_LEFT] and self.onWall!=-1:
                    self.xv-=0.02
                    self.facing = -1
                if keys[pg.K_d] or keys[pg.K_RIGHT] and self.onWall!=1:
                    self.xv+=0.02
                    self.facing = 1
                self.xv*=0.9915
            
            if self.xv>2.05:
                self.xv-=0.04
            if self.xv<-2.05:
                self.xv+=0.04
            
            #Forfeit floatiness with S or down arrow
            if keys[pg.K_s] or keys[pg.K_DOWN]:
                self.jCounter=0

            #Stop if you're going very slow & change animation
            self.yv+=self.gravity*0.03025
            if abs(self.xv)<0.4 and self.onGround and self.animation!='landed' and self.animation!='hardlanded':
                self.animation='none'
                self.saveAni='none'
            if abs(self.xv)<0.1 and self.onGround:
                self.xv*=self.xv
            if self.onWall==-1:
                self.xv = max(0,self.xv)
                if self.onGround:
                    self.animation='none'
            if self.onWall==1:
                self.xv = min(0,self.xv)
                if self.onGround:
                    self.animation='none'
            if self.animation=='run' and not self.onGround:
                self.animation='falling'
            
            #Set display facing, used for animations
            if self.facing!=0:
                self.dFacing = self.facing
            
            #Caps on vertical speed
            if not -3.5<self.yv<8.5:
                self.yv*=0.96
            
            #Updating x & y pos
            self.xpos+=self.xv
            self.ypos+=self.yv
            self.dt-=1
        pl.animations()

class Sensor(pg.sprite.Sprite):
    def __init__(self,orig):
        self.orig = orig
    
    def detect(self,x,y,show=False):
        global camerax,cameray
        xp = self.orig.xpos+x+self.orig.xv
        yp = self.orig.ypos+y+self.orig.yv
        block = (int(yp/32)*width)+int(xp/32)
        ret = level[block]
        subtype = levelSub[block]
        if show and ke[pg.K_r]:
            if ret!=0:
                pg.draw.circle(screen,(0,255,80),(self.orig.xpos+x-camerax,self.orig.ypos+y-cameray),4)
            else:
                pg.draw.circle(screen,(0,40,255),(self.orig.xpos+x-camerax,self.orig.ypos+y-cameray),4)
        return ret,block,subtype



width = 0
height = 0
startx = 0
starty = 0
loadFrom = 'lvl1.arl'
def loadARL(filename): #Level loading algorithm
    global level,levelSub,width,height,loadedTiles
    f = open(os.path.join(path,"Levels",filename),'rb')
    bites = f.read()
    f.close()
    counter = 0
    cou = 0
    width = 10
    height = 10
    while cou<(len(bites))-6:
        byte = bites[cou]
        if counter==4: #Headers
            width+=byte*256
        if counter==5:
            width+=byte
        if counter==6:
            height+=byte*256
        if counter==7:
            height+=byte
        if counter==8:
            width-=10
            height-=10
            lv = [0] * (width*height)
            lv2 = [0] * (width*height)
        if counter>63: #Data
            if byte==0:
                cou+=1
                byte = bites[cou]
                counter+=byte-1
            else:
                lv.insert(counter-64,byte)
                cou+=1
                byte = bites[cou]
                lv2.insert(counter-64,byte)
                
        counter+=1
        cou+=1
    level = lv
    levelSub = lv2
    bCounter = 0
    blocks = []
    loadedTiles = ['']*65536
    for bl in level:
        if bl!=0:
            blocks.append((bl*256)+levelSub[bCounter])
        bCounter+=1
    setBlock = set(blocks)
    for i in setBlock:
        try:
            loadedTiles[i] = pg.image.load(os.path.join(path,"Images", "Tiles", str(int(i/256)) + "-" + str(int(i%256)) + ".png"))
        except:
            pass


def moveCamera(mousex,mousey,rxy=0): #Camera moving algorithm
    global camerax,cameray,diffcx,diffcy,ke
    if (4*WID/10)<mousex<(6*WID/10):
        camx = WID/2
        if (4*HEI/10)<mousey<(6*HEI/10):
            pg.draw.rect(screen,(60,60,60),pg.Rect(4*WID/10,4*HEI/10,WID/5,HEI/5),3)
    else:
        camx = mousex
    if (4*HEI/10)<mousey<(6*HEI/10):
        camy = HEI/2
    else:
        camy = mousey
    tx = pl.xpos+(pl.xv*128)+(pl.dFacing*128)-(WID/2)+(camx-WID/2)/3
    ty = -(HEI/10)+pl.ypos+(min(0,pl.yv*24))-(HEI/2)+(camy-HEI/2)/3
    remcx = camerax
    remcy = cameray
    camerax += (tx-camerax)*0.0575*(60/targetFps)+random.uniform(-rxy,rxy)
    cameray += (ty-cameray)*0.125*(60/targetFps)+random.uniform(-rxy,rxy)+(-15 if ke[pg.K_w] else 15 if ke[pg.K_s] else 0)
    diffcx = (-math.sqrt(abs(camerax-remcx)) if camerax-remcx<0 else math.sqrt(camerax-remcx))
    diffcy = (-math.sqrt(abs(cameray-remcy)) if cameray-remcy<0 else math.sqrt(cameray-remcy))

#Defines collision detection between player and interactable objects
def playerCollisionDetection(type,block,subtype):
    global level,levelSub,nextCall,triggerPhone,redrawHearts
    #Blocks are 1-3

    #Dash Crystal
    if type == 4:
        pl.abilities[2] = 4
        pl.abilities[3] = 2
        pl.abilities[4] = 2
        pl.energy = 100
        setLevelBlock(block,6,30)
        heal(1)
    
    #Maintinence
    if type == 5:
        if subtype == 1:
            raise Exception("Forced Crash via 5-1 tile")

    #Blue Heart
    elif type == 7:
        health.insert(2,heart.Heart(2,4))
        setLevelBlock(block,0,0)
        redrawHearts = True
    
    #Silver Heart
    elif type == 8:
        health.insert(2,heart.Heart(3,subtype))
        setLevelBlock(block,0,0)
        redrawHearts = True

    #Red Heart
    elif type == 9:
        heal(subtype)
        setLevelBlock(block,0,0)
        redrawHearts = True

    #Maintinence / Blood Heart
    elif type == 10:
        if subtype == 1:
            health.insert(2,heart.Heart(4,1))
            setLevelBlock(block,0,0)
            redrawHearts = True

    #Phone Call Triggers (11-)
    elif type == 11:
        nextCall = levelSub[block]/1000
        triggerPhone = True
        setLevelBlock(block,10,0)

#Sets level blocks
def setLevelBlock(block,lvl,sLvl):
    global level,levelSub
    level[block]=lvl
    levelSub[block]=sLvl

#Changes tile properties such as dash crystal cooldown
def tileProperties(mod): 
    counter = int(mod*(len(level)/60))
    while counter<int((mod+1)*(len(level)/60)):
        block = level[counter]
        if block==6:
            if levelSub[counter]>0:
                levelSub[counter]-=10
            else:
                level[counter]=4
                levelSub[counter]=0
        counter+=1

#Deals damage to hearts in order
def dealDmg(amt):
    global redrawHearts
    for heart in reversed(health):
        amt-=heart.takeDmg(amt)
    for heart in health:
        if heart.amt==0 and heart.type!=1:
            #Do blood heart logic here
            health.pop(health.index(heart))
    redrawHearts=True

#Heals red & silver hearts
def heal(amt):
    global redrawHearts
    for heart in health:
        amt-=heart.heal(amt)
    redrawHearts=True
        
#Main Init
pg.init()
WID = 1280
HEI = 800
gameScale = 1.0
screen = pg.display.set_mode((WID,HEI),pg.DOUBLEBUF,vsync=True)
running = True
state = 'game'
f=1
fList = [idealFps]
fps = pg.time.Clock()
textfont = pg.font.SysFont('Times New Roman',36)
smallfont = pg.font.SysFont('Times New Roman',14)
pl = Player()
se = Sensor(pl)
loadARL(loadFrom)

camerax = 0
cameray = 0

triggerPhone = False
phoneCounter = 0
nextCall = 0
waitCounter = 2
phoneX = 0
phoneY = 0
currentText = []

redrawHearts=True
resumeTimer = 0

boxWidth = 0
targetFps = 60
avgFps = 60
health = [heart.Heart(1,4),heart.Heart(1,4)]

counter = 0



#Main Game Loop
while running:
    mousex,mousey = pg.mouse.get_pos()
    HUD = pg.Surface((WID,HEI),pg.SRCALPHA)
    boxLayer = pg.Surface((WID,HEI),pg.SRCALPHA)
    text = pg.Surface((WID,HEI),pg.SRCALPHA)
    WID,HEI = pg.display.get_surface().get_size()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    screen.fill((30,30,30))
    ke = pg.key.get_pressed()
    gameScale = (HEI/800)

    #Only if the physics are running
    if state=='game':
        pl.update(ke)
        tileProperties(counter%60)
        moveCamera(mousex,mousey,max(0,(pl.yv-2.5)))
    elif state=='phonecall' and boxWidth>width:
        moveCamera(mousex,mousey)
        if line>-1:
            tsurface = textfont.render(str(textName),True,(230,230,230))
            text.blit(tsurface,(70,HEI-385))
        for i in range(0,len(currentText)):
            tsurface = textfont.render(str(currentText[i]),True,(230,230,230))
            text.blit(tsurface,(70,HEI-270+(i*50)))
    elif state=='pause':
        pass
    elif state=='resuming':
        moveCamera(mousex,mousey)
        pg.draw.line(screen,(230,40,40),(pl.xpos-camerax,pl.ypos-cameray),(pl.xpos-camerax+(20*pl.xv),pl.ypos-cameray+(20*pl.yv)),4)
        resumeTimer-=1
        if resumeTimer<=0:
            state = 'game'

    


    #Handle Phone Calls
    if nextCall>=1:
        boxRect = pg.Rect(50,HEI-300,boxWidth,250)
        nameRect = pg.Rect(50,HEI-400,min(150,boxWidth),75)
        pg.draw.rect(boxLayer,(0,0,0),boxRect,0,25)
        pg.draw.rect(boxLayer,(230,230,230),boxRect,5,25)
        pg.draw.rect(boxLayer,(0,0,0),nameRect,0,25)
        pg.draw.rect(boxLayer,(230,230,230),nameRect,5,25)
        state = 'phonecall'
        if boxWidth<WID-100:
            boxWidth+=64
            lineCounter = 0
            charCounter = 0
            line = -1
            txt = []
            textName = ''
            currentText = ['','','']
        else:
            boxWidth=WID-100
            if txt==[]:
                f = open(os.path.join(path,"Phone Calls", str(int(nextCall)) + ".txt"),'r')
                txt = f.read()
            
            if waitCounter<=0:
                if ke[pg.K_x] or ke[pg.K_TAB]:
                    waitCounter=0
                else:
                    waitCounter=random.randint(0,1)
                if charCounter<len(txt):
                    i=txt[charCounter] #Important
                    if line==-1:
                        textName+=i
                        if i=='\n':
                            line=0
                        charCounter+=1
                    else:
                        if i!='\\':
                            currentText[line]+=i
                            charCounter+=1
                        else:
                            j = txt[charCounter+1]
                            if j=='.':
                                waitCounter=10
                                charCounter+=2
                            elif j==',':
                                waitCounter=20
                                charCounter+=2
                            elif j=='|':
                                waitCounter = 60
                                charCounter+=2
                            elif j=='t':
                                charCounter+=2
                                line+=1
                            elif j=='n':
                                if ke[pg.K_RETURN] or ke[pg.K_z]:
                                    currentText = ['','','']
                                    line = -1
                                    charCounter+=2

                else:
                    if ke[pg.K_RETURN] or ke[pg.K_z]:
                        currentText = ['','','']
                        nextCall=0
                        boxWidth = 0
                        state = 'game'
            else:
                waitCounter-=1*(240/targetFps)
            
            
    #Draw Player
    if pl.img!='':
        screen.blit(pl.img,((pl.xpos-camerax+pl.imgPos[0])*gameScale,(pl.ypos-cameray+pl.imgPos[1])*gameScale))

    #Draw Blocks
    re=0
    for x in range(max(0,int(camerax-32)),min(width*32,int((camerax+WID+32))),32):
        for y in range(max(0,int(cameray-32)),min(height*32,int((cameray+HEI+32))),32):
            re+=1
            i = int(y/32)*width+int(x/32)
            x-=(x%32)
            y-=(y%32)
            bl = level[i]
            blSub = levelSub[i]
            if bl==0 or bl==6 or bl==11 or bl==5:
                pass
            else:
                try:
                    if bl==7 or bl==8 or bl==9 or bl==10:
                        screen.blit(pg.transform.scale_by(loadedTiles[bl*256+blSub],2), ((x-camerax)*gameScale,(y-cameray)*gameScale,32*gameScale,32*gameScale))
                    else:
                        screen.blit(loadedTiles[bl*256+blSub], ((x-camerax)*gameScale,(y-cameray)*gameScale,32*gameScale,32*gameScale))
                except:
                    pass
            if ke[pg.K_t]:
                tsurface = smallfont.render(str(bl),True,(255,0,0) if bl!=0 else (180,180,180))
                screen.blit(tsurface, ((x-camerax)*gameScale,(y-cameray)*gameScale,32*gameScale,32*gameScale))
                tsurface = smallfont.render(str(blSub),True,(255,0,0) if bl!=0 else (180,180,180))
                screen.blit(tsurface, ((x-camerax)*gameScale,(y+12-cameray)*gameScale,32*gameScale,32*gameScale))

                    
    #Draw Phone
    if triggerPhone:
        phoneCounter+=1
        if counter%2==0:
            phoneImg = pg.image.load(os.path.join(path,"Images","Phone","phone" + str(1+int((counter%6)/2)) + ".png"))
            phoneImg = pg.transform.scale_by(phoneImg,max(2,min(4,7-phoneCounter/10)))
        if phoneCounter>380*(idealFps/60):
            triggerPhone=False
        elif phoneCounter>360*(idealFps/60):
            phoneX += (WID-20-phoneX)*0.125*(60/targetFps)
            phoneY += (30-phoneY)*0.125*(60/targetFps)
        elif phoneCounter>30*(idealFps/60):
            phoneX += (pl.xpos-camerax-phoneX-13)*0.2*(60/targetFps)+random.uniform(-2,2)
            phoneY += (pl.ypos-cameray-phoneY-170)*0.2*(60/targetFps)+random.uniform(-2,2)
        else:
            phoneX=WID-80
            phoneY=15
        phoneRect = pg.Rect(phoneX,phoneY,30,50)
        if phoneRect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed()[0]:
            pg.draw.rect(screen, (230,20,20), phoneRect)
            triggerPhone=False
            nextCall*=1000

        HUD.blit(phoneImg,(phoneX,phoneY))
    else:

        if counter%60==0 or phoneCounter!=0:
            phoneImg = pg.image.load(os.path.join(path,"Images","Phone","normal1.png"))
            phoneImg = pg.transform.scale_by(phoneImg,4)
            phoneRect = pg.Rect(WID-80,15,60,100)
        if phoneRect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed()[0]:
            if state!='pause':
                state = 'pause'
            else:
                state = 'resuming'
                resumeTimer = 30
        phoneCounter=0
        HUD.blit(phoneImg,(WID-80,15))
        phoneX=WID-80
        phoneY=15



    #Draw Hearts & Hex
    if counter%600==0:
        hexImg = pg.image.load(os.path.join(path,"Images","UI","hex2x.png"))
        hexImg = pg.transform.scale_by(hexImg,0.5)

    HUD.blit(hexImg,(10,HEI-160))

    c=0
    for hp in health:
        if redrawHearts:
            hp.setImg(pg.image.load(os.path.join(path,"Images","Hearts",hp.fileExt + str(hp.amt) + ".png")))
            hp.img = pg.transform.scale_by(hp.img,4)
            hp.img = pg.transform.rotate(hp.img,4.289)
        try:
            HUD.blit(hp.img,(150+(68*c),HEI-80-(c*5.1)))
        except:
            pass
        c+=1
    redrawHearts=False


    
    #HUD

    #Energy Bar
    for j in range(0,10):
        for i in range(0,20):
            pg.draw.aaline(HUD,(60,60,60) if 10*j+(i/2)>=pl.energy else (240-(pl.energy*6),60+(pl.energy*6),40) if pl.energy<30 else (40,220,40), (WID-20-i-(22*j),HEI-55-(j*1.666)-(i/13.333)+(1 if i==0 or i==19 else 0)),(WID-20-i-(22*j),HEI-20-(j*1.666)-(i/13.333)-(1 if i==0 or i==19 else 0)))
    
    #Disclaimer
    tsurface = smallfont.render(str(buildIdentifier) + " - This footage does not neccesarily represent the final game.",True,(230,230,230))
    HUD.blit(tsurface,(10,10))
    
    #Debug Stats
    if ke[pg.K_r]:
        tsurface = smallfont.render(str(pl.xv),True,(230,230,230))
        HUD.blit(tsurface,(10,35))
        tsurface = smallfont.render(str(pl.yv),True,(230,230,230))
        HUD.blit(tsurface,(10,50))
        tsurface = smallfont.render(str(pl.abilities),True,(230,230,230))
        HUD.blit(tsurface,(10,65))
        avgFps = sum(fList)/len(fList)
        tsurface = smallfont.render(str(round(avgFps,2)) + " fps",True,(230,230,230))
        HUD.blit(tsurface,(10,80))
        tsurface = smallfont.render(str(round(1000/f,2)) + " fps",True,(230,230,230))
        HUD.blit(tsurface,(10,95))


    targetFps=min(idealFps,avgFps)
    threeDee=False
    #Rendering 3D Hud
    if threeDee:
        if counter%1==0:
            dst = np.float32([[0,0],[WID,0],[HEI,0],[WID,HEI]])
            w, h = HUD.get_size()
            pts = np.float32([[(-pl.yv/4-diffcy)*2,(-pl.xv/4-diffcx)*2],[WID+((pl.yv/4+diffcy)*4),(pl.xv/4+diffcx)*2],[WID-((pl.yv/4+diffcy)*4),HEI-((pl.xv/4+diffcx)*4)],[(pl.yv/4+diffcy)*2,HEI+((pl.xv/4+diffcx)*4)]])
            src_corners = np.float32([(0, 0), (0, w), (h, w), (h, 0)])
            mat = cv2.getPerspectiveTransform(src_corners, np.float32([(p[1],p[0]) for p in pts]))
            buf_rgb = pg.surfarray.array3d(HUD)
            out_rgb = cv2.warpPerspective(buf_rgb, mat, (HEI,WID), flags=cv2.INTER_LINEAR)
            out = pg.Surface(out_rgb.shape[0:2], pg.SRCALPHA)
            pg.surfarray.blit_array(out, out_rgb)
        screen.blit(out,(0,max(0,-pl.yv*6)),None,1)
    else:
        screen.blit(HUD,((-diffcx*4,max(0,-pl.yv*6))))
    screen.blit(boxLayer,(0,0))
    screen.blit(text,(0,0))


    #End time, processing FPS
    fps.tick(targetFps)
    f = fps.get_rawtime()
    fList.append(1000/f)
    if len(fList)>(targetFps*2):
        fList.pop(0)
    pg.display.flip()
    #time.sleep(0.1)
    counter+=1
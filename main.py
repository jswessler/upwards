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
import sensor
import kunai

import mathFuncs.distFuncs as distF
import mathFuncs.imgFuncs as imgF
import mathFuncs.loadArl as loadARL

gamePath = os.getcwd() #Path to game directory
idealFps = 60 #Target FPS for the game to aim for
buildId = "id153.1" #Build Identifier

class Player(pg.sprite.Sprite):
    def __init__(self,spawn):
        self.ypos = 32*(math.floor(spawn/width))
        self.xpos = 32*(spawn%width)
        self.xv = 0
        self.yv = 0
        self.energy = 100
        self.facing = 0
        self.gravity = 1
        self.jCounter = 0
        self.abilities = [4,15,0,2,2] #Jump, Extended Jump, Double Jump, Dive, Jump Dive
        self.wallClimb = False
        self.timeOnGround = 0
        self.onGround = True
        self.counter=0
        self.slide = 0
        self.slideBoost = 0
        self.img = ''
        self.imgPos = [0,0]
        self.dFacing = 1
        self.animation = 'falling'
        self.nextAni = 'none'
        self.aniFrame = 1
        self.aniTimer = 0
        self.aniiTimer = 0
        self.dt = 0
        self.maxSpd = 2.05
        self.kunaiAni = 0
        self.slideMult = 0

        #Collision Boxes. bottom, top, right, left (in that order)
        self.col = [12,-100,30,-25]
    
    def animations(self):
        global kunais,kuAni
        if self.aniTimer>=0:
            self.aniTimer-=float(60/targetFps)
        self.aniiTimer-=float(60/targetFps)

        #Tumble Landing
        
        #Normal Landing
        if self.animation=='landed':
            if self.aniTimer<0:
                self.animation = 'none'
            self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","land.png"))
            self.img = imgF.imgPos(self.img,self.dFacing)
            self.imgPos = [-36,-94]
        
        #Hard Landing (11 frame animation with 3 images)
        elif self.animation=='hardlanded':
            if self.aniTimer<0:
                self.animation = 'none'
            if self.aniTimer>11:
                self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","hardland1.png"))
            elif self.aniTimer>7:
                self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","hardland2.png"))
            else:
                self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","hardland3.png"))
            self.img = imgF.imgPos(self.img,self.dFacing)
            if self.aniTimer>11:
                self.imgPos = [-34,-94]
            elif self.aniTimer>7:
                self.imgPos = [-32,-66]
            else:
                self.imgPos = [-26,-94]

        #Phone Call



        #Ground Animations

        #Throwing Kunai (not implemented, currently just locks your animation for 40 frames)
        if self.kunaiAni > 0:
            self.kunaiAni -= 1
            if self.kunaiAni == 37: #Spawn a kunai on frame 37
                kuAni = 0
                #Determine direction
                dx, dy, dir = distF.cos(mousex-(self.xpos-camerax),mousey-(self.ypos-cameray))
                dx+=random.uniform(-0.04,0.04)
                dy+=random.uniform(-0.04,0.04)
                spawnedKunai.append(kunai.Kunai(self.xpos,self.ypos-70,dx*30,dy*30,gamePath,level,levelSub,width))
            if self.kunaiAni < 1:
                self.kunaiAni = 0
                kunais-=1

        elif self.onGround:
            #Run (17 frame animation, 1 aniframe per 4.25-2 frames depening on speed)
            if self.animation=='run' or abs(self.xv)>0.35:
                if self.aniTimer<0:
                    self.aniFrame+=1
                    if self.aniFrame==18:
                        self.aniFrame=1
                    self.aniTimer = max(2,int(4.25-abs(self.xv)))
                self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","run" + str(self.aniFrame) + ".png"))
                self.img = imgF.imgPos(self.img,self.dFacing)
                self.imgPos = [-36,-94]
            
            #Idle (4 frame animation on a mod%60)
            elif self.animation=='none':
                if self.counter%60<16:
                    self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","idle1.png"))
                elif self.counter%60<31:
                    self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","idle2.png"))
                elif self.counter%60<47:
                    self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","idle3.png"))
                else:
                    self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","idle4.png"))
                self.img = imgF.imgPos(self.img,self.dFacing)
                self.imgPos = [-26,-100]
        


        #Air Animations

        else:
        #Hover (2 frame animation, 6 frame interval, 2 extra frames when low on energy)
            if self.animation == 'hover':
                self.nextAni = 'low'
                self.aniiTimer = 13
                self.animation = 'none'
                if self.aniTimer < 0:
                    self.aniFrame += 1
                    self.aniTimer = 6
                if self.aniFrame > 6:
                    self.aniFrame = 1
                if self.energy > 30:
                    if abs(self.xv)<0.5:
                        self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","hovern" + str(self.aniFrame) + ".png"))
                    else:
                        self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","hoverr" + str(self.aniFrame) + ".png"))
                else:
                    if abs(self.xv)<1:
                        self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","hovernl" + str(self.aniFrame) + ".png"))
                    else:
                        self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","hoverrl" + str(self.aniFrame) + ".png"))
                self.img = imgF.imgPos(self.img,self.dFacing)
                self.imgPos = [-31,-102]
            #Air Transitions

            elif self.yv>-0.5 and (self.nextAni=='high' or self.nextAni=='low') and not self.onGround: #If we have a queued animation
                #High Transition after Jump
                if self.aniiTimer<-1:
                    self.aniiTimer = 13
                if self.nextAni == 'high':
                    if self.aniiTimer < 0:
                        self.nextAni = 'none'
                        self.animation = 'falling'
                    #After 3 frames, go to standard falling animation
                    self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","jumptrans" + str(int((18-self.aniiTimer)/5)) + ".png"))
                    self.img = imgF.imgPos(self.img,self.dFacing)
                    self.imgPos = [-31,-100]
                
                #Mid Transition after double jump
                elif self.nextAni == 'mid':
                    if self.aniiTimer < 0:
                        self.nextAni = 'none'
                        self.animation = 'falling'
                    self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","lowtrans2.png"))
                    self.img = imgF.imgPos(self.img,self.dFacing)
                    self.imgPos = [-31,-100]

                #Low transition after hover or dive jump
                elif self.nextAni == 'low':
                    if self.aniiTimer < 0:
                        self.nextAni = 'none'
                        self.animation = 'falling'
                    self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","lowtrans" + str(int((18-self.aniiTimer)/5)) + ".png"))
                    self.img = imgF.imgPos(self.img,self.dFacing)
                    self.imgPos = [-31,-100]
                if self.aniiTimer < 0:
                    self.aniiTimer = 13 
            else:
            
            #Air Animations ------

            #Walljump

            #Wallslide
                if self.animation == 'wallslide':
                    if self.counter % 20 < 10:
                        self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","wallslide.png"))
                    else:
                        self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","wallslide2.png"))
                    self.img = imgF.imgPos(self.img,-self.dFacing)
                    self.imgPos = [-26,-101]

            #Double Jump
                if self.nextAni == 'djump':
                    self.animation = 'falling'
                    if self.aniTimer < 0:
                        self.aniFrame += 1
                        self.aniTimer = 3
                    if self.aniFrame > 4:
                        self.nextAni = 'mid'
                        self.aniiTimer = 13
                    self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","djump" + str(min(3,self.aniFrame)) + ".png"))
                    self.img = imgF.imgPos(self.img,self.dFacing)
                    self.imgPos = [-84,-101]
                
                #Djump transition (when moving up)
                elif self.animation=='djumpup':
                    if self.aniTimer<0:
                        self.aniFrame+=1
                        self.aniTimer=3
                    if self.aniFrame>3:
                        self.aniFrame=1
                    if self.aniFrame==3:
                        self.nextAni='djump'
                        self.animation='none'
                    self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","djumpup" + str(min(2,self.aniFrame)) + ".png"))
                    self.img = imgF.imgPos(self.img,self.dFacing)
                    self.imgPos = [-32,-125]
                
                #Djump transition (when moving down)
                elif self.animation == 'djumpdown':
                    if self.aniTimer < 0:
                        self.aniFrame += 1
                        self.aniTimer = 3
                    if self.aniFrame > 3:
                        self.aniFrame = 1
                    if self.aniFrame == 3:
                        self.nextAni = 'djump'
                        self.animation = 'none'
                    self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","djumpdown" + str(min(2,self.aniFrame)) + ".png"))
                    self.img = imgF.imgPos(self.img,self.dFacing)
                    self.imgPos = [-31,-104]
                    
                #First Jump (2 frame animation on mod%30 that plays as long as you're moving up)
                elif self.animation == 'jump':
                    self.nextAni = 'high'
                    self.aniiTimer = 13
                    self.aniTimer = 6
                    if self.counter%30 < 16:
                        self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","jumpup1.png"))
                    else:
                        self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","jumpup2.png"))
                    self.img = imgF.imgPos(self.img,self.dFacing)
                    self.imgPos = [-31,-100]
                


                #Dive

                #Hover
                    

            #Falling Animations

                elif self.nextAni=='fastfall':
                    if self.aniTimer<0:
                        self.aniFrame+=1
                        self.aniTimer=(20-(2*self.yv))
                    if self.aniFrame>4:
                        self.aniFrame=1
                    self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","flail" + str(self.aniFrame) + ".png"))
                    self.img = imgF.imgPos(self.img,self.dFacing)
                    self.imgPos = [-31,-116]

                elif self.nextAni == 'fftrans':
                    if self.aniTimer < 0:
                        self.nextAni = 'fastfall'
                    self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","fftrans.png"))
                    self.img = imgF.imgPos(self.img,self.dFacing)
                    self.imgPos = [-31,-116]

                #Falling
                elif self.animation=='falling':
                    if self.aniTimer<0:
                        self.aniFrame+=1
                        self.aniTimer=5
                    if self.aniFrame>4:
                        self.aniFrame=1
                    if self.yv>4.25:
                        self.aniTimer = 9
                        self.nextAni='fftrans'
                        self.animation='none'
                    self.img = pg.image.load(os.path.join(gamePath,"Images","Aria","falling" + str(self.aniFrame) + ".png"))
                    self.img = imgF.imgPos(self.img,self.dFacing)
                    self.imgPos = [-31,-116]

    #Run Every Frame
    def update(self,keys):
        global kunais, health, redrawHearts
        self.counter+=60/targetFps
        self.dt+=240/targetFps

        #Do collision detection using 8 points scattered around your model
        for i in range(self.col[1]+7,20,32):
            for j in range(-14,19,32):
                det,bl,st,circ = se.detect(j,i)
                playerCollisionDetection(det,bl,st)

        #For complicated reasons physics targets 240fps.
        #If we're running below 240fps then we do multiple physics steps per drawn frame
        #We don't allow running above 240fps
        dtr = targetFps/60
        while self.dt>0:
            #Reduce jump hover counter
            if self.jCounter>0:
                self.jCounter-=0.25
            #Incrase energy if it ends up below 0 (somehow)
            if self.energy<0:
                self.energy+=0.1
            #Energy calculations
            if self.energy < 20:
                eRegen = (self.energy / 105)+0.005
            elif self.energy < 75:
                eRegen = 0.19
            else:
                eRegen = max(0.005,0.0075 + (100-self.energy) / 250)
            for h in health:
                if h.type == 3 and h.amt == 2:
                    eRegen*=1.125
                    self.energy+=0.0025
                    self.yv-=0.001

            #Object Collision Detection

            #Ground Collision (self.col[0] is the bottom of the model)
            if any(se.detect(i,self.col[0])[0]==1 for i in range(-21,29,16)):
                if self.onGround==False:
                    self.ypos+=1
                    self.energy+=(5*eRegen)+0.5 #give you a bit of energy on landing
                    if 0.5<self.yv<4.5:
                        self.animation = 'landed'
                        self.aniTimer = 1+int(self.yv*2.5)
                    elif self.yv > 4.5:
                        self.aniTimer = 20
                        self.animation = 'hardlanded'
                        self.maxSpd = 1.5
                        if self.yv > 7.75:
                            health = heart.dealDmg(1,health)
                        if self.yv > 6.5:
                            health = heart.dealDmg(1,health)
                        if self.yv > 5.75:
                            health = heart.dealDmg(1,health)
                            redrawHearts = True
                        
                self.onGround = True
                self.timeOnGround += 1

                #Slowdown if you landed hard
                if self.animation=='hardlanded':
                    self.xv*=0.5
                self.yv = 0
                self.gravity = 0
                self.abilities[0] = 1 #Jump
                self.abilities[1] = 15 #Jump Extension 
                self.abilities[2] = 4 #Double Jump
                self.abilities[3] = 2 #Dive
                self.abilities[4] = 2 #Dive Jump
                self.energy+=eRegen+0.0001
            else:
                self.onGround = False
                self.timeOnGround = 0
                self.gravity = 1

                #Regen energy if falling quickly and you have >5 energy
                if self.energy > 5:
                    self.energy+= 0.012*(max(0,self.yv))

                #Slide off an edge
                if self.slide > 0:
                    self.slide -= min(5,self.slide)
                    self.jCounter = 1
                    self.energy-=0.075
                    

                #Up detection (only run when not on ground)
                if any(se.detect(i,self.col[1])[0]==1 for i in range(-22,23,11)): #Up
                    self.yv = 0
                    self.ypos+=1
                    self.jCounter=0
            
            #Right & Left Detection
            self.onWall=0
            if any(se.detect(self.col[2],i)[0]==1 for i in range(self.col[1]+10,11,25)): #Right
                self.onWall = 1
                self.xv = 0
            if any(se.detect(self.col[3],i)[0]==1 for i in range(self.col[1]+10,11,25)): #Left
                self.onWall = -1
                self.xv = 0

            #Energy Cap
            if self.energy>100:
                self.energy=100



            if keys[pg.K_SPACE] or keys[pg.K_UP]:

                #Main Single Jump
                if self.abilities[0] > 0: #Jump
                    if self.slide >= 190 and self.slideBoost == 0: #Sliding Boost
                        self.slideBoost = math.pow(90-(self.slide-190),2)
                    self.jCounter = (12 - (3 * self.abilities[0]))
                    self.abilities[0] -= 0.25 if self.slideBoost == 0 else 1
                    self.yv -= 0.345*(1+(self.slideBoost/2500)) + (0.025 * abs(self.xv))
                    self.animation = 'jump'

                #Jump Extension
                if not self.onGround and self.abilities[0]<=0 and self.abilities[1]>0 and self.energy>0.175:
                    self.yv-=0.0325
                    if self.abilities[1]<12.5:
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

                if 0<self.abilities[2]<4 and not self.onGround and not self.wallClimb and self.abilities[0]<=0 and self.abilities[3]==2 and self.energy>0.8:
                    
                    if self.yv>0:
                        self.yv*=0.4
                    self.yv-=(0.325+0.0125*abs(self.xv))
                    self.maxSpd = 2.85
                    self.xv*=1.0125
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
                    #animation
                    self.animation = 'hover'

            #Logic when not pressing space    
            else:
                self.slideBoost = 0
                if 0<self.abilities[0]<4 and not self.onGround: #Lose your single jump if you let go of space
                    self.abilities[0]=0
                    self.abilities[1]=0
                if self.abilities[0]<=0 and self.abilities[2]==4: #Activate double jump once you let go of space after normal jumping
                    self.abilities[2]=3
                    self.abilities[1]=0
                if 0<self.abilities[2]<3: #lose double jump if you let go early
                    self.abilities[2]=0
                
                #Hop off of wall by letting go (fix for right-side wall jump)
                self.wallClimb = False

                #Slight hover at the end of jumps
                if self.yv>-1 and self.jCounter>0:
                    self.energy-=0.05
                    self.gravity = 0.45

            #Wall slide 
                if all(se.detect(self.facing*31,i)[0]==1 for i in range(-70,10,30)) and not self.onGround and self.facing!=0 and self.energy>0.24:
                    self.jCounter=2
                    if self.yv > 1.5:
                        self.yv = 1.5
                    self.wallClimb = True
                    self.energy-=0.04
                    self.animation = 'wallslide'
                    self.nextAni = 'none'
                elif self.animation == 'wallslide':
                    self.nextAni = 'low'
                    self.animation = 'none'
                    self.aniiTimer = 13

            #Wall Jump
                if self.wallClimb and self.energy>6 and (((keys[pg.K_a] or keys[pg.K_LEFT]) and self.onWall==1) or ((keys[pg.K_d] or keys[pg.K_RIGHT]) and self.onWall==-1) or (keys[pg.K_SPACE] or keys[pg.K_UP])):
                    self.yv*=0.25
                    self.yv-=3.75
                    self.jCounter=20
                    self.xv = -self.facing*3
                    self.energy-=6
                    self.wallClimb = False
                    self.abilities[3]=2
                    self.abilities[4]=1
                    self.animation= 'jump' #change to walljump

            #Dive
            if keys[pg.K_LCTRL]:
                if self.abilities[3]>0 and self.abilities[0]<=0 and self.energy>10:
                    if self.dFacing == 1:
                        self.xv = 4.25
                    else:
                        self.xv = -4.25
                    self.yv*=0.975
                    self.yv-=0.125
                    self.abilities[2]=0
                    self.abilities[3]-=0.1
                    self.energy-=1
                    self.maxSpd = 3.4
                    self.animation = 'jump' #change this to 'dive' when dive animation is implemented
                
            #Kunai Spawning on e or click
            if kunais > 0 and self.kunaiAni<18 and self.energy>20 and (ke[pg.K_e] or pg.mouse.get_pressed()[0]):
                if self.kunaiAni!=0:
                    kunais-=1
                    self.energy-=6
                self.kunaiAni = 40
                self.energy-=12
                #self.animation = 'none' #change this to throwing animation

            #Directional Inputs
            self.facing = 0

            #On the ground, you have a lot more traction
            if self.onGround:
                if keys[pg.K_a] or keys[pg.K_LEFT] and self.onWall!=-1:
                    self.xv-=0.1225
                    self.facing = -1
                    self.animation='run'
                    if self.maxSpd<2.75:
                        self.maxSpd+=0.004
                elif keys[pg.K_d] or keys[pg.K_RIGHT] and self.onWall!=1:
                    self.xv+=0.1225
                    self.facing = 1
                    self.animation='run'
                    if self.maxSpd<2.75:
                        self.maxSpd+=0.004
                else:
                    if self.maxSpd>1.9:
                        self.maxSpd-=0.02
                self.xv*=0.96
                if self.facing == 0 or self.facing / self.xv<0:
                    self.maxSpd = 2
                
                #Slide
                if (keys[pg.K_s] or keys[pg.K_DOWN]) and abs(self.xv)>1.6 and self.energy > 15 and (self.slide == 0 or self.slide > 200):
                    self.col = [12,-40,30,-25]
                    if self.timeOnGround < 15 and self.slideMult == 0:
                        self.slideMult = 1.5
                    else:
                        self.slideMult = 1
                    self.maxSpd = 3.25*self.slideMult
                    if 0 < self.xv < 3.25*self.slideMult:
                        self.xv += 0.45*self.slideMult
                    elif -3.25*self.slideMult < self.xv < 0:
                        self.xv -= 0.45*self.slideMult
                    if self.slide == 0:
                        self.xv *= 1.5 * self.slideMult
                        self.slide = 280
                        self.energy -= 5
                else:
                    self.col = [12,-100,30,-25]
                if self.slide > 0:
                    self.slide -= 1
                    if self.slide < 200:
                        self.slideMult = 0
                    else:
                        self.energy-=0.24

            #In the air you have a lot less traction
            else:
                if self.maxSpd>2.25:
                    self.maxSpd-=0.002
                if keys[pg.K_a] or keys[pg.K_LEFT] and self.onWall!=-1:
                    self.xv-=0.02
                    self.facing = -1
                if keys[pg.K_d] or keys[pg.K_RIGHT] and self.onWall!=1:
                    self.xv+=0.02
                    self.facing = 1
                self.xv*=0.9915
            
            if self.xv>self.maxSpd:
                self.xv-=0.0425
            if self.xv<-self.maxSpd:
                self.xv+=0.0425
            if self.maxSpd>2.75:
                self.maxSpd-=0.01
            
            #Forfeit floatiness with S or down arrow
            if keys[pg.K_s] or keys[pg.K_DOWN]:
                self.jCounter=0
            if keys[pg.K_w]:
                self.yv-=0.001
                self.energy-=0.01

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
            if not -3<self.yv<8.5:
                self.yv*=0.985
            
            #Updating x & y pos
            self.xpos+=self.xv
            self.ypos+=self.yv
            self.dt-=1
        pl.animations()



#Level loading routine for now :)
loadFrom = 'lvl1.arl'
level,levelSub,loadedTiles,width,height,spawn = loadARL.loadARL(loadFrom,gamePath)

#Camera moving algorithm
def moveCamera(mousex,mousey,rxy=0):
    global camerax,cameray,diffcx,diffcy,ke
    if (4*WID/10)<mousex<(6*WID/10):
        camx = (WID/2+mousex)/2
    else:
        camx = mousex
    if (4*HEI/10)<mousey<(6*HEI/10):
        camy = (HEI/2+mousey)/2
    else:
        camy = mousey
    
    #Adjust camera parameters
    tx = pl.xpos+(pl.xv*120)+(pl.dFacing*120)-(WID/2)+(camx-WID/2)/2.5
    ty = -(HEI/10)+pl.ypos+(min(0,pl.yv*24))-(HEI/2)+(camy-HEI/2)/2.5
    remcx = camerax
    remcy = cameray
    camerax += (tx-camerax)*0.0575*(60/targetFps)+random.uniform(-rxy,rxy)
    cameray += (ty-cameray)*0.125*(60/targetFps)+random.uniform(-rxy,rxy)+(-16 if ke[pg.K_w] else 4 if ke[pg.K_s] else 0)
    diffcx = (-math.sqrt(abs(camerax-remcx)) if camerax-remcx<0 else math.sqrt(camerax-remcx))
    diffcy = (-math.sqrt(abs(cameray-remcy)) if cameray-remcy<0 else math.sqrt(cameray-remcy))

#Defines collision detection between player and interactable objects (not walls)
def playerCollisionDetection(type,block,subtype):
    global level,levelSub,nextCall,triggerPhone,redrawHearts,health
    #Blocks are 1-3

    #Dash Crystal
    if type == 4:
        if subtype<3:
            pl.abilities[2] = 4
            pl.abilities[3] = 2
            pl.abilities[4] = 2
            pl.energy = 100
            setLevelBlock(block,6,(subtype*10)+30)
            health = heart.healDmg(1,health)
            redrawHearts = True
    
    #Maintinence
    if type == 5:
        if subtype == 1:
            raise Exception("Forced Crash Via 5-1 Tile")

    #Blue Heart
    elif type == 7 and subtype <= 4:
        health.insert(2,heart.Heart(2,(4 if subtype == 0 else subtype)))
        setLevelBlock(block,0,0)
        redrawHearts = True
    
    #Silver Heart
    elif type == 8 and subtype <= 2:
        health.insert(2,heart.Heart(3,subtype))
        setLevelBlock(block,0,0)
        redrawHearts = True

    #Red Heart
    elif type == 9:
        health = heart.healDmg(subtype,health)
        setLevelBlock(block,0,0)
        redrawHearts = True

    #Maintinence / Blood Heart
    elif type == 10:
        if subtype == 1:
            health.insert(2, heart.Heart(4,1))
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



#Changes on-screen tile properties such as dash crystal cooldown
def tileProperties(mod):
    xl,yl = distF.getOnScreen(camerax,cameray,width,height,WID,HEI)
    yf = yl[int((mod/8)*len(yl)): int(((mod+1)/8)*len(yl))] #Only cover 1/8 of the screen per call
    for x in xl:
        for y in yf:
            counter = (int(y/32)*width)+int(x/32) #pick 1 block
            block = level[counter]
            #Reduce dash crystal cooldown
            if block==6:
                if levelSub[counter]>0:
                    levelSub[counter]-=1
                #Set dash crystal cooldown tile back to dash crystal
                else:
                    level[counter]=4
                    levelSub[counter]=0
        
#Main Init
pg.init()
WID = 1280
HEI = 800
gameScale = 1
screen = pg.display.set_mode((WID,HEI),pg.DOUBLEBUF|pg.RESIZABLE,vsync=True)
running = True
state = 'game'
f=1
fList = [idealFps]
spawnedKunai = []
kunais = 5
kuAni = -1
fps = pg.time.Clock()
textfont = pg.font.SysFont('Times New Roman',36)
smallfont = pg.font.SysFont('Times New Roman',14)
pl = Player(spawn)
se = sensor.Sensor(pl,level,levelSub,width)

#Variable Setup
camerax = cameray = 0
triggerPhone = False
phoneCounter = 0
nextCall = 0
waitCounter = 2
phoneX = 0
phoneY = 0
currentText = []
mouseUIInteract = False
redrawHearts=True
resumeTimer = 0
boxWidth = 0 #text box width (0 is invisible)
targetFps = 60
avgFps = 60
health = [heart.Heart(1,4),heart.Heart(1,4)] #Two full red hearts
counter = 0 #frame counter

#Loading & Scaling kunai image
kunaiImg = pg.image.load(os.path.join(gamePath,"Images","UI","kunai.png"))
kunaiImg = pg.transform.rotate(kunaiImg,-4.289)
kunaiImg = pg.transform.smoothscale_by(kunaiImg,0.15)

#Draw Hearts & Hex
hexImg = pg.image.load(os.path.join(gamePath,"Images","UI","hex.png"))
hexImg = pg.transform.smoothscale_by(hexImg,0.25)

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
    #gameScale = (HEI/800) #Set game scale to the window size

    #Only if the physics are running
    if state=='game':
        pl.update(ke) #Do Physics
        tileProperties(counter%8) #Update Tiles (1/8 of the scren at a time)
        moveCamera(mousex,mousey,max(0,(pl.yv-2.5))) #Handle Camera Movement
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

    #In-Game Loop
    if state == 'game' or state == 'resuming' or state == 'pause' or state == 'phonecall':
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
                    f = open(os.path.join(gamePath,"Phone Calls", str(int(nextCall)) + ".txt"),'r')
                    txt = f.read()
                
                if waitCounter <= 0:
                    if ke[pg.K_x] or ke[pg.K_TAB]:
                        waitCounter = 0
                    else:
                        waitCounter = random.randint(0,1)
                    if charCounter < len(txt):
                        i=txt[charCounter] #Important
                        if line == -1:
                            textName += i
                            if i=='\n':
                                line = 0
                            charCounter += 1
                        else:
                            if i!='\\':
                                currentText[line]+=i
                                charCounter+=1
                            else:
                                j = txt[charCounter+1]
                                if j=='.':
                                    waitCounter = 15
                                    charCounter += 2
                                elif j==',':
                                    waitCounter = 25
                                    charCounter += 2
                                elif j=='|':
                                    waitCounter = 60
                                    charCounter += 2
                                elif j=='t':
                                    charCounter += 2
                                    line+=1
                                elif j=='n':
                                    if ke[pg.K_RETURN] or ke[pg.K_z]:
                                        currentText = ['','','']
                                        line = -1
                                        charCounter += 2

                    else:
                        if ke[pg.K_RETURN] or ke[pg.K_z]:
                            currentText = ['','','']
                            nextCall = 0
                            boxWidth = 0
                            state = 'game'
                else:
                    waitCounter-=1*(240/targetFps)
                
                
        #Draw Player
        if pl.img!='':
            screen.blit(pl.img,((pl.xpos-camerax+pl.imgPos[0])*gameScale,(pl.ypos-cameray+pl.imgPos[1])*gameScale))

        #Draw Kunais & do Kunai physics
        for ku in spawnedKunai:
            if not ku.update(pl.xpos,pl.ypos):
                spawnedKunai.pop(spawnedKunai.index(ku))
                kunais += 1
            screen.blit(ku.image,((ku.xpos-camerax)*gameScale,(ku.ypos-cameray)*gameScale))
        
        #Draw HUD Kunais
        for i in range(0,kunais):
            kunaiImg.set_alpha(255)
            if i == 0:
                if 0<=kuAni<=14:
                    kunaiImg.set_alpha(255-(kuAni*15))
                    HUD.blit(kunaiImg,(WID-100-(i*38)+kuAni,HEI-150-(i*3)-(kuAni*kuAni+kuAni)))
                elif kuAni >= 39 or kuAni == -1:
                    HUD.blit(kunaiImg,(WID-100-(i*38),HEI-150-(i*3)))
            else:   
                if 24<=kuAni<=40:
                    HUD.blit(kunaiImg,(WID-152-(i*38)+(kuAni*2.3),HEI-154-(i*3)+(kuAni/5)))
                else:
                    HUD.blit(kunaiImg,(WID-100-(i*38),HEI-150-(i*3)))
        if kuAni!=-1:
            kuAni+=1
        if kuAni >= 40:
            kuAni = -1

        #Draw Blocks
        re=0
        xl,yl = distF.getOnScreen(camerax,cameray,width,height,WID,HEI)
        for x in xl:
            for y in yl:
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
                    tsurface = smallfont.render(str(blSub),True,(255,0,0) if blSub!=0 else (180,180,180))
                    screen.blit(tsurface, ((x-camerax)*gameScale,(y+12-cameray)*gameScale,32*gameScale,32*gameScale))

                        
        #Draw Phone
        if triggerPhone:
            phoneCounter+=1
            if counter%2==0:
                phoneImg = pg.image.load(os.path.join(gamePath,"Images","Phone","phone" + str(1+int((counter%6)/2)) + ".png"))
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
                phoneImg = pg.image.load(os.path.join(gamePath,"Images","Phone","normal1.png"))
                phoneImg = pg.transform.scale_by(phoneImg,4)
                phoneRect = pg.Rect(WID-80,15,60,100)
            if ((phoneRect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed()[0]) or ke[pg.K_ESCAPE]) and not mouseUIInteract:
                mouseUIInteract = True
                if state!='pause':
                    state = 'pause'   
                else:
                    state = 'resuming'
                    resumeTimer = 15
            phoneCounter=0
            HUD.blit(phoneImg,(WID-80,15))
            phoneX=WID-80
            phoneY=15
            #Fix for spamclicking
            if mouseUIInteract and not pg.mouse.get_pressed()[0] and not ke[pg.K_ESCAPE]:
                mouseUIInteract = False

        HUD.blit(hexImg,(10,HEI-210))

        c=0
        for hp in health:
            if redrawHearts:
                try:
                    hp.setImg(pg.image.load(os.path.join(gamePath,"Images","Hearts",hp.fileExt + str(hp.amt) + ".png")))
                except:
                    health.pop(health.index(hp))
                hp.img = pg.transform.scale_by(hp.img,4)
                hp.img = pg.transform.rotate(hp.img,4.289)
            try:
                HUD.blit(hp.img,(180+(68*c),HEI-77-(c*5.1)))
            except:
                pass
            c+=1
        redrawHearts=False


        
        #HUD

        #Energy Bar
        for j in range(0,10):
            for i in range(0,20):
                pg.draw.aaline(HUD,(60,60,60) if 10*j+(i/2)>=pl.energy else (220-(pl.energy*6),40+(pl.energy*6),40) if pl.energy<30 else (40,300-pl.energy,-400+(pl.energy*6)) if pl.energy>80 else (40,220,40), (WID-20-i-(22*j),HEI-55-(j*1.666)-(i/13.333)+(1 if i==0 or i==19 else 0)),(WID-20-i-(22*j),HEI-20-(j*1.666)-(i/13.333)-(1 if i==0 or i==19 else 0)))
        
        #BuildId
        tsurface = smallfont.render(str(buildId),True,(230,230,230))
        HUD.blit(pg.transform.rotate(tsurface,-55),(15,HEI-62))
        
        #Debug Stats
        avgFps = sum(fList)/len(fList)
        if ke[pg.K_r]:
            tsurface = smallfont.render(str(pl.xv),True,(230,230,230))
            HUD.blit(tsurface,(10,HEI-250))
            tsurface = smallfont.render(str(pl.yv),True,(230,230,230))
            HUD.blit(tsurface,(10,HEI-265))
            tsurface = smallfont.render(str(pl.maxSpd),True,(230,230,230))
            HUD.blit(tsurface,(10,HEI-280))
            tsurface = smallfont.render(str(round(avgFps,2)) + " fps",True,(230,230,230))
            HUD.blit(tsurface,(10,HEI-295))
            tsurface = smallfont.render(str(round(1000/f,2)) + " fps",True,(230,230,230))
            HUD.blit(tsurface,(10,HEI-310))
            #Draw a center box (only on R press as of id versions)
            if (4*HEI/10)<mousey<(6*HEI/10) and (4*WID/10)<mousex<(6*WID/10):
                pg.draw.rect(screen,(60,60,60),pg.Rect(4*WID/10,4*HEI/10,WID/5,HEI/5),3)


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
            screen.blit(HUD,((-diffcx*4,(-pl.yv*6 if pl.yv < 0 else 0 if pl.yv < 4 else (-diffcy+4)*4))))
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
import math,os,random
import pygame as pg

import mathFuncs.imgFuncs as imgF
import mathFuncs.distFuncs as distF

import heart
import kunai
import sensor

buildId = 'id152.2'
#Player Animations

    
def animations(self,targetFps):
    if self.aniTimer>=0:
        self.aniTimer-=float(60/targetFps)
    self.aniiTimer-=float(60/targetFps)

    #Tumble Landing

    #Normal Landing
    if self.animation=='landed':
        if self.aniTimer<0:
            self.animation = 'none'
        self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","land.png"))
        self.img = imgF.imgPos(self.img,self.dFacing)
        self.imgPos = [-36,-94]

    #Hard Landing (11 frame animation with 3 images)
    elif self.animation=='hardlanded':
        if self.aniTimer<0:
            self.animation = 'none'
        if self.aniTimer>11:
            self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","hardland1.png"))
        elif self.aniTimer>7:
            self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","hardland2.png"))
        else:
            self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","hardland3.png"))
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
            self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","run" + str(self.aniFrame) + ".png"))
            self.img = imgF.imgPos(self.img,self.dFacing)
            self.imgPos = [-36,-94]
        
        #Idle (4 frame animation on a mod%60)
        elif self.animation=='none':
            if self.counter%60<16:
                self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","idle1.png"))
            elif self.counter%60<31:
                self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","idle2.png"))
            elif self.counter%60<47:
                self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","idle3.png"))
            else:
                self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","idle4.png"))
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
                    self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","hovern" + str(self.aniFrame) + ".png"))
                else:
                    self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","hoverr" + str(self.aniFrame) + ".png"))
            else:
                if abs(self.xv)<1:
                    self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","hovernl" + str(self.aniFrame) + ".png"))
                else:
                    self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","hoverrl" + str(self.aniFrame) + ".png"))
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
                self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","jumptrans" + str(int((18-self.aniiTimer)/5)) + ".png"))
                self.img = imgF.imgPos(self.img,self.dFacing)
                self.imgPos = [-31,-100]
            
            #Mid Transition after double jump
            elif self.nextAni == 'mid':
                if self.aniiTimer < 0:
                    self.nextAni = 'none'
                    self.animation = 'falling'
                self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","lowtrans2.png"))
                self.img = imgF.imgPos(self.img,self.dFacing)
                self.imgPos = [-31,-100]

            #Low transition after hover or dive jump
            elif self.nextAni == 'low':
                if self.aniiTimer < 0:
                    self.nextAni = 'none'
                    self.animation = 'falling'
                self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","lowtrans" + str(int((18-self.aniiTimer)/5)) + ".png"))
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
                    self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","wallslide.png"))
                else:
                    self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","wallslide2.png"))
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
                self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","djump" + str(min(3,self.aniFrame)) + ".png"))
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
                self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","djumpup" + str(min(2,self.aniFrame)) + ".png"))
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
                self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","djumpdown" + str(min(2,self.aniFrame)) + ".png"))
                self.img = imgF.imgPos(self.img,self.dFacing)
                self.imgPos = [-31,-104]
                
            #First Jump (2 frame animation on mod%30 that plays as long as you're moving up)
            elif self.animation == 'jump':
                self.nextAni = 'high'
                self.aniiTimer = 13
                self.aniTimer = 6
                if self.counter%30 < 16:
                    self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","jumpup1.png"))
                else:
                    self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","jumpup2.png"))
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
                self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","flail" + str(self.aniFrame) + ".png"))
                self.img = imgF.imgPos(self.img,self.dFacing)
                self.imgPos = [-31,-116]

            elif self.nextAni == 'fftrans':
                if self.aniTimer < 0:
                    self.nextAni = 'fastfall'
                self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","fftrans.png"))
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
                self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","falling" + str(self.aniFrame) + ".png"))
                self.img = imgF.imgPos(self.img,self.dFacing)
                self.imgPos = [-31,-116]

    
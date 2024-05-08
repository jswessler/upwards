import pygame as pg

import math,os,sensor,heart,particle
import sensor

import mathFuncs.imgFuncs as imgF



buildId = 'id157.2'
class Player(pg.sprite.Sprite):
    def __init__(self,spawn,width,gamePath,level,levelSub):
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
        self.gamePath = gamePath
        self.se = sensor.Sensor(self,level,levelSub,width)

        #Collision Boxes. bottom, top, right, left (in that order)
        self.col = [12,-100,30,-25]
    
    def animations(self,targetFps):
        global kunais,kuAni
        particles = [] #reset particle list
        if self.aniTimer>=0:
            self.aniTimer-=float(60/targetFps)
        self.aniiTimer-=float(60/targetFps)
        if self.kunaiAni > 0:
            self.kunaiAni -= 1

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

        elif self.onGround:
            if self.animation == 'slide' and abs(self.xv)>0.5:
                #Main sliding loop
                if self.slide > 221:
                    if self.counter%12 < 6:
                        self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","slide1.png"))
                    else:
                        self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria","slide2.png"))
                    self.img = imgF.imgPos(self.img,self.dFacing)
                    self.imgPos = [-36,-86]

                #Slide exit transition
                else:
                    self.img = pg.image.load(os.path.join(self.gamePath,"Images","Aria",("slideout1.png" if self.slide > 210 else "slideout2.png")))
                    self.img = imgF.imgPos(self.img,self.dFacing)
                    self.imgPos = [-36,-86]
            #Run (17 frame animation, 1 aniframe per 4.25-2 frames depening on speed)
            elif self.animation == 'run' or abs(self.xv) > 0.35:
                if self.aniTimer < 0:
                    self.aniFrame += 1
                    if self.aniFrame == 18:
                        self.aniFrame = 1
                        particles.append(particle.Particle(self.xpos,self.ypos,'run',self.dFacing,self.gamePath))
                    if self.aniFrame == 9:
                        particles.append(particle.Particle(self.xpos,self.ypos,'run',self.dFacing,self.gamePath))
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
        return particles
    #Run Every Frame
    def update(self,keys,targetFps,health):
        self.counter+=60/targetFps
        self.dt+=240/targetFps
        rdH = False #redraw hearts (communication with main loop)

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
            if any(self.se.detect(i,self.col[0])[0]==1 for i in range(-21,29,8)):
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
                            rdH = True
                        
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
                    self.nextAni = 'low'
                    

                #Up detection (only run when not on ground)
                if any(self.se.detect(i,self.col[1])[0]==1 for i in range(-22,23,11)): #Up
                    self.yv = 0
                    self.ypos+=1
                    self.jCounter=0
            
            #Right & Left Detection
            self.onWall=0
            if any(self.se.detect(self.col[2],i)[0]==1 for i in range(self.col[1]+10,11,25)): #Right
                self.onWall = 1
                self.xv = 0
            if any(self.se.detect(self.col[3],i)[0]==1 for i in range(self.col[1]+10,11,25)): #Left
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
                    self.abilities[0] -= 0.25
                    self.yv -= 0.34 + (self.slideBoost/50000) + (0.025 * abs(self.xv))
                    if self.slideBoost != 0:
                        self.energy-=0.25
                        self.xv *= 1+self.slideBoost/250000
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
                if all(self.se.detect(self.facing*31,i)[0]==1 for i in range(-70,10,30)) and not self.onGround and self.facing!=0 and self.energy>0.24:
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
            if self.kunaiAni<18 and self.energy>20 and (keys[pg.K_e] or pg.mouse.get_pressed()[0]):
                self.kunaiAni = 40
                self.energy-=12
                #self.animation = 'none' #change this to throwing animation

            #Directional Inputs
            self.facing = 0

            #On the ground, you have a lot more traction
            if self.onGround:
                if keys[pg.K_a] or keys[pg.K_LEFT] and self.onWall!=-1:
                    self.xv-=0.122
                    self.facing = -1
                    self.animation='run'
                    if self.maxSpd<2.8:
                        self.maxSpd+=0.004
                elif keys[pg.K_d] or keys[pg.K_RIGHT] and self.onWall!=1:
                    self.xv+=0.122
                    self.facing = 1
                    self.animation='run'
                    if self.maxSpd<2.8:
                        self.maxSpd+=0.004
                else:
                    if self.maxSpd>1.8:
                        self.maxSpd-=0.0125
                self.xv*=0.96
                if self.facing == 0 or self.facing / self.xv<0:
                    self.maxSpd = 2
                
                #Slide
                if (keys[pg.K_s] or keys[pg.K_DOWN]) and abs(self.xv)>1.75 and self.energy > 15 and (self.slide == 0 or self.slide > 200):
                    self.col = [12,-40,30,-25]
                    if self.timeOnGround < 15 and self.slideMult == 0:
                        self.slideMult = 1.5
                        self.energy += 17.5
                    else:
                        self.slideMult = 1
                    self.maxSpd = 3.5*self.slideMult
                    if 0 < self.xv < 3.5*self.slideMult:
                        self.xv += 0.55*self.slideMult
                    elif -3.5*self.slideMult < self.xv < 0:
                        self.xv -= 0.55*self.slideMult
                    if self.slide == 0:
                        self.xv *= 1.5 * self.slideMult
                        self.slide = 280
                        self.energy -= 12.5
                else:
                    self.col = [12,-100,30,-25]
                if self.slide > 0:
                    self.slide -= 1
                    if self.slide < 200:
                        self.slideMult = 0
                        self.animation = 'run'
                    else:
                        self.energy-=0.24
                        self.animation = 'slide'

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
        p = self.animations(targetFps)
        return rdH,p

import pygame as pg
from time import process_time
import random,os,math

import heart,sensor,kunai,player,button,particle

import mathFuncs.distFuncs as distF
import mathFuncs.imgFuncs as imgF
import mathFuncs.loadArl as loadARL

gamePath = os.getcwd() #Path to game directory
idealFps = 60 #Target FPS for the game to aim for
buildId = "id157.2" #Build Identifier

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
particles = []
kunais = 5
kuAni = -1
fps = pg.time.Clock()
textfont = pg.font.SysFont('Times New Roman',36)
smallfont = pg.font.SysFont('Times New Roman',14)
pl = player.Player(spawn,width,gamePath,level,levelSub)
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
redrawHearts = True
resumeTimer = 0
boxWidth = 0 #text box width (0 is invisible)
targetFps = 60
avgFps = 60
health = [heart.Heart(1,4),heart.Heart(1,3)] #Two full red hearts
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

    #Only if the physics are running
    if state=='game':
        redrawHearts,p = pl.update(ke,targetFps,health) #Do Physics
        for i in p: #for each generated particle, add it to the list
            particles.append(i)
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

    #Main Menu
    if state == 'menu': 
        pass



    #MAIN GAME LOOP
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
        for i in range(pl.col[1]+7,20,32):
            for j in range(-14,19,32):
                det,bl,st,circ = se.detect(j,i)
                playerCollisionDetection(det,bl,st)

        #Draw Particles
        for i in particles:
            if i.update():
                particles.pop(particles.index(i))
            else:
                screen.blit(i.img,((i.xpos+i.xoffset-camerax)*gameScale,(i.ypos+i.yoffset-cameray)*gameScale))

        #Draw Kunais & do Kunai physics
        #Spawn kunai (moved from player to main in id153.2)
        if pl.kunaiAni == 37:
            dx,dy,dir = distF.cos(mousex-(pl.xpos-camerax),mousey-(pl.ypos-cameray))
            dx += random.uniform(-0.04,0.04)
            dy += random.uniform(-0.04,0.04)
            spawnedKunai.append(kunai.Kunai(pl.xpos,pl.ypos-60,dx*30,dy*30,gamePath,level,levelSub,width))
            kunais -= 1
            kuAni = 0
            pl.energy -= 12 #id155.1 moved from player to main
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

        #Draw Hex
        HUD.blit(hexImg,(10,HEI-210))

        #Draw Hearts
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
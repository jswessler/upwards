import pygame as pg
import random
import time

pg.init()
screen = pg.display.set_mode((440,660))
running = True
fps = pg.time.Clock()
font = pg.font.SysFont('Times New Roman',18)
counter = 0

hand1 = [] #Your Hand
hand2 = []
hand3 = []
hand4 = []
play = []
nR=0.001
dR=0.004
nP=0.001
dP=0.004
nW=0.001
dW=0.004
nPQ=0.001
dPQ=0.004
nT=0.001
dT=0.001
skip = 0
amt = 1
turn = 0 #cards is missing the 3 of clubs since its assumed it will always be the 1st card played
cards = [3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,11,11,11,11,12,12,12,12,13,13,13,13,14,14,14,14,15,15,15,15]


lookup = ['','','','3','4','5','6','7','8','9','10','J','Q','K','A','2']

def shuffle(yours):
    global hand1,hand2,hand3,hand4,hands,yourHand
    if yours:
        hand1 = []
    hand2 = []
    hand3 = []
    hand4 = []
    tempCards = cards.copy()
    for ca in hand1:
        tempCards.pop(ca)
    counter = len(tempCards)
    while counter>0:
        card = random.randint(0,len(tempCards)-1)
        ca = tempCards.pop(card)
        if yours:
            if counter%4==0:
                hand1.append(ca)
            elif counter%4==1:
                hand2.append(ca)
            elif counter%4==2:
                hand3.append(ca)
            elif counter%4==3:
                hand4.append(ca)
        else:
            if counter%3==0:
                hand2.append(ca)
            elif counter%3==1:
                hand3.append(ca)
            elif counter%3==2:
                hand4.append(ca)
        counter-=1
    yourHand = hand1.copy()
    hands = [hand1,hand2,hand3,hand4]


#Type 1 - everyone plays randomly
#Type 2 - you play perfect, everyone else random
#Type 3 - you play random, everyone else perfect

def runSimulation(typ):
    global play,turn,ke,skip,yourHand,amt
    turn = random.randint(0,3)
    play = [3] #3 of clubs is played
    shuffle(False)
    hands[0]=yourHand.copy()
    while True:
        if typ==4:
            if turn==0:
                playPerfect(hands[turn],play[-1] if len(play)!=0 else '',amt)
            else:
                playRandom(hands[turn],play[-1] if len(play)!=0 else '',amt)
                completeQuads(0,hands[0])
        elif typ==2:
            if turn==0:
                playPerfect(hands[turn],play[-1] if len(play)!=0 else '',amt)
            else:
                playRandom(hands[turn],play[-1] if len(play)!=0 else '',amt)
                
        elif typ==3:
            if turn==0:
                playRandom(hands[turn],play[-1] if len(play)!=0 else '',amt)
            else:
                playPerfect(hands[turn],play[-1] if len(play)!=0 else '',amt)
        elif typ==1:
            playRandom(hands[turn],play[-1] if len(play)!=0 else '',amt)

        for h in range(0,4):
            if len(hands[h])==0:
                #print('winner is player ' + str(h+1))
                if h==0:
                    return 1
                else:
                    return 0
        if play[-1]==15 or (len(play)>=4 and play[-1]==play[-2]==play[-3]==play[-4]):
            play = []
        elif skip==3:
            play = []
            turn+=1
            skip = 0
        else:
            turn+=1
        if turn>3:
            turn-=4



def playRandom(hand,topcard,a): 
    global play,turn,skip,amt
    if topcard=='': #If we're starting out
        ra = random.randint(0,len(hand)-1)
        ca = hand[ra]
        #print("Player " + str(turn+1) + " starts with " + str(hand[ra]))
        play.append(hand.pop(ra))
        amt=1
        while ca in hand and random.randint(1,2)==1:
            ra = hand.index(ca)
            play.append(hand.pop(ra))
            amt+=1
        return
    if all(h<topcard for h in hand) or all(hand.count(h)<a for h in range(topcard,15)): #If we have no legal cards
        #print('no valid card')
        skip+=1
        return
    while True: #Otherwise, just play a random legal card
        ra = random.randint(0,len(hand)-1)
        ca = hand[ra]
        if (hand[ra]>=topcard and hand.count(ca)>=a) or ra==15:
            skip = 0
            #print("Player " + str(turn+1) + " plays " + str(hand[ra]))
            if hand[ra]==topcard:
                #print('skipped! ' + str(hand[ra]) + " - " + str(topcard))
                turn+=1
                skip+=1
            for i in range(0,a):
                ra = hand.index(ca)
                #print(ra)
                play.append(hand.pop(ra))
            return


def playPerfect(hand,topcard,a): 

    #Rules
    #If we start, play the lowest card possible. We always try to start with doubles/triples/quads
    #If it's our turn, we try to skip by playing same number
    #Otherwise, play the lowest card possible
    #We can only bomb if we have no other options


    global play,turn,skip,amt
    if topcard=='': #If we're starting out
        for i in range(3,16):
            if i in hand:
                ca = i
                break
        ra = hand.index(ca)
        play.append(hand.pop(ra))
        amt=1
        while ca in hand:
            ra = hand.index(ca)
            play.append(hand.pop(ra))
            amt+=1
        return
    if all(h<topcard for h in hand) or all(hand.count(h)<a for h in range(topcard,15)): #If we have no legal cards
        skip+=1
        return
    j=0
    while True: #Otherwise, follow rules above
        for i in range(topcard+j,15):
            if i in hand:
                ra = hand.index(i)
                break
        ca = hand[ra]
        if (hand[ra]>=topcard and hand.count(ca)>=a) or ra==15:
            skip = 0
            if hand[ra]==topcard:
                turn+=1
                skip+=1
            for i in range(0,a):
                ra = hand.index(ca)
                play.append(hand.pop(ra))
            return
        j+=1
        if topcard+j>15: #Skip if we can't play anything
            skip+=1
            return

def completeQuads(tu,hand):
    global turn,play
    if (len(play)>0 and play[-1] in hand and hand.count(play[-1])==3) or (len(play)>1 and play[-1]==play[-2] and play[-1] in hand and hand.count(play[-1]==2) or (len(play)>2 and play[-1]==play[-2]==play[-3] and play[-1] in hand)):
        #print('i completed a quad!')
        #print(pl)
        #print(hand)
        turn = tu
        temp = play[-1]
        while temp in hand:
            ra = hand.index(temp)
            play.append(hand.pop(ra))
        #print(hand)
        #print('\n')
        








stopped = False

while running:
    displayHand = []
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    screen.fill((30,30,30))
    ke = pg.key.get_pressed()
    


    if ke[pg.K_ESCAPE]:
        hand1 = []
        hand2 = []
        hand3 = []
        hand4 = []


    elif ke[pg.K_RETURN]:
        for i in range(0,20):
            nR+=runSimulation(1)
            nP+=runSimulation(2)
            nW+=runSimulation(3)
            nPQ+=runSimulation(4)
        dR+=20
        dP+=20
        dW+=20
        dPQ+=20
        dT+=80

    if ke[pg.K_2]:
        if not stopped:
            hand1.append(15)
            stopped = True
    elif ke[pg.K_3]:
        if not stopped:
            hand1.append(3)
            stopped = True
    elif ke[pg.K_4]:
        if not stopped:
            hand1.append(4)
            stopped = True
    elif ke[pg.K_5]:
        if not stopped:
            hand1.append(5)
            stopped = True
    elif ke[pg.K_6]:
        if not stopped:
            hand1.append(6)
            stopped = True
    elif ke[pg.K_7]:
        if not stopped:
            hand1.append(7)
            stopped = True
    elif ke[pg.K_8]:
        if not stopped:
            hand1.append(8)
            stopped = True
    elif ke[pg.K_9]:
        if not stopped:
            hand1.append(9)
            stopped = True
    elif ke[pg.K_0]:
        if not stopped:
            hand1.append(10)
            stopped = True
    elif ke[pg.K_j]:
        if not stopped:
            hand1.append(11)
            stopped = True
    elif ke[pg.K_q]:
        if not stopped:
            hand1.append(12)
            stopped = True
    elif ke[pg.K_k]:
        if not stopped:
            hand1.append(13)
            stopped = True
    elif ke[pg.K_a]:
        if not stopped:
            hand1.append(14)
            stopped = True
    elif ke[pg.K_LSHIFT]:
        nR=0.001
        dR=0.004
        nP=0.001
        dP=0.004
        nW=0.001
        dW=0.004
        nWQ=0.001
        dWQ=0.004
        nT=0.001
        dT=0.004
        shuffle(False)
    elif ke[pg.K_TAB]:
        nR=0.001
        dR=0.004
        nP=0.001
        dP=0.004
        nW=0.001
        dW=0.004
        nPQ=0.001
        dPQ=0.004
        nT=0.001
        dT=0.004
        shuffle(True)
    else:
        stopped = False
    
    for i in hand1:
        displayHand.append(lookup[i])

    tsurface = font.render("Hand: " + str(displayHand),True,(230,230,230))
    screen.blit(tsurface,(10,90))
    tsurface = font.render("President Win Rate Calculator - by Jonathan",True,(230,230,230))
    screen.blit(tsurface,(10,10))
    tsurface = font.render("Esc: Reset - Tab: Shuffle - Keyboard: Input Cards",True,(230,230,230))
    screen.blit(tsurface,(10,30))
    tsurface = font.render("Shift: Lock in - Enter: Simulate",True,(230,230,230))
    screen.blit(tsurface,(10,50))
    tsurface = font.render(str(round(nR*100/dR,2)) + "% Win Rate (Random)",True,(200,200,60))
    screen.blit(tsurface,(10,120))
    tsurface = font.render(str(round(nP*100/dP,2)) + "% Win Rate (Perfect Play, No Jumping On Quads)",True,(40,220,90))
    screen.blit(tsurface,(10,160))
    tsurface = font.render(str(round(nW*100/dW,2)) + "% Win Rate (Bad Play)",True,(180,70,40))
    screen.blit(tsurface,(10,140))
    tsurface = font.render(str(round(nPQ*100/dPQ,2)) + "% Win Rate (Perfect Play, Jump On Quads)",True,(30,230,255))
    screen.blit(tsurface,(10,180))
    tsurface = font.render(str(round((nR+nP+nW+nPQ)*100/dT,2)) + "% Overall Win Rate",True,(230,230,230))
    screen.blit(tsurface,(10,200))

    pg.draw.line(screen,(70,70,70),(20,300),(420,300),2)
    pg.draw.line(screen,(230,230,230),(20,300),(20+(400*(nR/dR)),300),2)
    pg.draw.line(screen,(130,130,130),(120,290),(120,310),2)
    pg.draw.line(screen,(200,200,200),(20,290),(20,310),2)
    pg.draw.line(screen,(200,200,200),(420,290),(420,310),2)

    pg.draw.line(screen,(200,200,60),(20+(400*(nR/dR)),290),(20+(400*(nR/dR)),310),2)
    pg.draw.line(screen,(40,220,90),(20+(400*(nP/dP)),290),(20+(400*(nP/dP)),310),2)
    pg.draw.line(screen,(180,70,40),(20+(400*(nW/dW)),290),(20+(400*(nW/dW)),310),2)
    pg.draw.line(screen,(30,230,255),(20+(400*(nPQ/dPQ)),290),(20+(400*(nPQ/dPQ)),310),2)
    pg.draw.line(screen,(230,230,230),(20+(400*(nR+nP+nW+nPQ)/dT),290),(20+(400*(nR+nP+nW+nPQ)/dT),310),2)

    fps.tick(144)
    pg.display.flip()
    
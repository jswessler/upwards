import pygame as pg
import os

buildId = 'id152.2'

#Load ARL from a file
def loadARL(filename,gamePath):
    global level,levelSub,width,height,loadedTiles, spawn
    f = open(os.path.join(gamePath,"Levels",filename),'rb')
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
            #If block is 0-0, skip ahead RLE bytes
            if byte==0:
                cou+=1
                byte = bites[cou]
                counter+=byte-1
            #Otherwise, add the block to the list
            else:
                lv.insert(counter-64,byte)
                cou+=1
                byte = bites[cou]
                lv2.insert(counter-64,byte)
            if lv[counter-64] == 5 and lv2[counter-64] == 0:
                spawn = counter - 64
                
        counter+=1
        cou+=1
    level = lv
    levelSub = lv2
    bCounter = 0
    blocks = []
    for bl in level:
        if bl!=0:
            blocks.append((bl*256)+levelSub[bCounter])
        bCounter+=1

    #Converting to set to see which blocks to load
    loadedTiles = ['']*65536
    setBlock = set(blocks)
    for i in setBlock:
        try:
            loadedTiles[i] = pg.image.load(os.path.join(gamePath,"Images", "Tiles", str(int(i/256)) + "-" + str(int(i%256)) + ".png"))
        except:
            pass
    return level,levelSub,loadedTiles,width,height,spawn
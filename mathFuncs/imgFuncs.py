import pygame as pg

buildId = 'id157.2'

#Scale & Flip player images properly
def imgPos(img,fac):
    img = pg.transform.scale_by(img,2)
    if fac==-1:
        img = pg.transform.flip(img,True,False)
    return img

def img2x(img):
    img = pg.transform.scale_by(img,2)
    return img
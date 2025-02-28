import pygame as pg

def drawText(text,x,y,dest,size,color=(255,255,255),imm=True):
    tempFont = pg.font.SysFont("Times New Roman",size)
    tsurface = tempFont.render(str(text),True,color)
    if imm:
        dest.blit(tsurface,(x,y))
    return tsurface
import pygame as pg

buildId = 'id166.1'

#Clicky button
#Credit to Patryk Karbowy on stackoverflow
class Button(pg.sprite.Sprite):
    def __init__(self, color, x, y, width, height, text='',name=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.name = name #variable to set state to when pressed

    def draw(self):
        #Call this method to draw the button on the screen
        r = pg.Rect(self.x, self.y, self.width, self.height)
        if self.text != '':
            font = pg.font.SysFont('Times New Roman', 24)
            text = font.render(self.text, 1, (0, 0, 0))
        return r,text
    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
import os

class Heart():
    def __init__(self,typ,amt):
        self.type = typ
        self.amt = amt

        #Set maxhp depending on what type of heart we are
        if typ==1:
            self.fileExt = 'red'
            self.maxHp = 4
        elif typ==2:
            self.fileExt = 'blue'
            self.maxHp = 4
        elif typ==3:
            self.fileExt = 'silver'
            self.maxHp = 2
        elif typ==4:
            self.fileExt = 'blood'
            self.maxHp = 1
        self.img = ''
    
    #Updates our image
    def setImg(self,img):
        self.img = img

    #Deal damage to heart. We pass in an amount of damage to take, and return how much we absorbed
    def takeDmg(self,amt):

        #Return how much dmg was absorbed
        if amt>self.amt:
            temp = self.amt
            amt-=self.amt
            self.amt=0
            return temp
        else:
            self.amt-=amt
            return amt
    
    #Heal this heart (only works on red and silver hearts). We pass in an amount of healing, and return how much we absorbed
    def heal(self,amt):
        if self.type==1 or self.type==3:
            if self.amt==self.maxHp:
                return 0
            elif amt+self.amt>self.maxHp:
                amt-=self.maxHp-self.amt
                self.amt=self.maxHp
                return amt
            else:
                self.amt+=amt
                return amt
        else:
            return 0
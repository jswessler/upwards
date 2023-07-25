
class Heart():
    def __init__(self,typ,amt):
        self.type = typ
        self.amt = amt
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
    def takeDmg(self,amt):
        #return how much dmg was absorbed
        if amt>self.amt:
            temp = self.amt
            amt-=self.amt
            self.amt=0
            return temp
        else:
            self.amt-=amt
            return amt
    def heal(self,amt):
        if self.type==1:
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
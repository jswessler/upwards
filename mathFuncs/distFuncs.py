import math

buildId = 'id152.2'

#Get angle based on relative x and y
def cos(relx,rely):
    dir = math.atan2(rely,relx)
    yf = math.sin(dir)
    xf = math.cos(dir)
    return xf,yf,dir

#Get distance between 2 points
def getDist(ix,iy,dx,dy):
    fx = dx-ix
    fy = dy-iy
    final = math.sqrt((fx**2)+(fy**2))
    return final

#Return a list of x and y ranges that are on screen (coordinates, divide by 32 to get block numbers)
def getOnScreen(camerax,cameray,width,height,WID,HEI):
    xs = max(0, int(camerax - 24))
    xf = min(width * 32, int((camerax + WID + 24)))
    ys = max(0, int(cameray - 24))
    yf = min(height * 32, int((cameray + HEI + 24)))
    xl = list(range(xs,xf,32))
    yl = list(range(ys,yf,32))
    return xl,yl
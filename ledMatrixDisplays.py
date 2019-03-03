#!/usr/bin/env python3

from rgbmatrix5x5 import RGBMatrix5x5

class LEDMatrixDisplays:
    """ Wrapper class representing a pair of 5x5 RGB LED matrix i2c display breakouts
    """
    
    frameQueue = []
    
    def __init__(self):
        self.d1 = RGBMatrix5x5(0x74)
        self.d2 = RGBMatrix5x5(0x77)
        self.clear()
        
    def clear(self):
        self.d1.clear()
        self.d1.show()
        self.d2.clear()
        self.d2.show()
        
    def reshow(self):
        self.d1.show()
        self.d2.show()
        
    def showPattern(self,display,pattern,rotate=0):
        """ Display an array of rgb values on the display, with optional rotate of the pattern """
        
        if rotate==1:
            #Rotate 90 deg
            for y in range(0,5):
                for x in range(0,5):
                    i = 5*x+y
                    display.set_pixel(x,y,pattern[i][0],pattern[i][1],pattern[i][2])
            
        elif rotate==2:
            #Rotate 180 deg
            for y in range(0,5):
                for x in range(0,5):
                    i = 24 - (5*y+4-x)
                    display.set_pixel(x,y,pattern[i][0],pattern[i][1],pattern[i][2])
            
        elif rotate==3:
            #Rotate 270 deg
            for y in range(0,5):
                for x in range(0,5):
                    i = 24 - (5*x+y)
                    display.set_pixel(x,y,pattern[i][0],pattern[i][1],pattern[i][2])
            
        else:
            #No rotation
            for y in range(0,5):
                for x in range(0,5):
                    i = 5*y+4-x
                    display.set_pixel(x,y,pattern[i][0],pattern[i][1],pattern[i][2])

        display.show()

    def addFrame(self,pattern):
        self.frameQueue.append(pattern)
    
    def fetchFrame(self):
        pattern = self.frameQueue[len(self.frameQueue)-1]
        return pattern
        
    def showNext(self):
        if len(self.frameQueue) > 0:
            #Get next pattern
            #pattern = self.frameQueue[len(self.frameQueue)-1]
            pattern = self.frameQueue.pop(0)
            self.showPattern(self.d1,pattern,2)
            self.showPattern(self.d2,pattern)
        else:
            self.reshow()
            
            
#Define colour codes and patterns
o = (0,0,0)
b = (0,0,200)
p = (255,153,204)
g = (128,255,0)
m = (255,0,127)
w = (255,255,255)
r = (255,0,0)

eye_open = [
o,w,w,w,o,
w,w,b,w,w,
w,b,b,b,w,
w,w,b,w,w,
o,w,w,w,o
]

eye_lid1 = [
o,o,o,o,o,
o,w,w,w,o,
w,b,b,b,w,
w,w,b,w,w,
o,w,w,w,o
]

eye_lid2 = [
o,o,o,o,o,
o,o,o,o,o,
o,w,w,w,o,
w,w,b,w,w,
o,w,w,w,o
]

eye_lid3 = [
o,o,o,o,o,
o,o,o,o,o,
o,o,o,o,o,
o,o,w,o,o,
o,w,w,w,o
]

red_eye = [
o,w,w,w,o,
w,w,r,w,w,
w,r,r,r,w,
w,w,r,w,w,
o,w,w,w,o
]

one = [
p,p,g,p,p,
p,g,g,p,p,
p,p,g,p,p,
p,p,g,p,p,
p,g,g,g,p
]


#!/usr/bin/env python3

from rgbmatrix5x5 import RGBMatrix5x5

class LEDMatrixDisplays:
    """ Wrapper class representing a pair of 5x5 RGB LED matrix i2c display breakouts
    """
    
    frameQueueL = []
    frameQueueR = []
    
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


    def addFrame(self,pattern,display=0):
        """ Add frame to animation queue for specified display.
            display 1 = left display only
            display 2 = right display only
            Any other value = both displays
        """
        if display != 2:
            self.frameQueueL.append(pattern)
        if display != 1:
            self.frameQueueR.append(pattern)


    def showNext(self):
        if len(self.frameQueueL) > 0:
            #Get next pattern from front of queue
            pattern = self.frameQueueL.pop(0)
            self.showPattern(self.d1,pattern,2)
        else:
            self.d1.show()
            
        if len(self.frameQueueR) > 0:
            #Get next pattern from front of queue
            pattern = self.frameQueueR.pop(0)
            self.showPattern(self.d2,pattern)
        else:
            self.d2.show()
    
    
    def showNow(self,pattern,display=0):
        """ Show pattern immediately on display(s)
            display 1 = left display only
            display 2 = right display only
            Any other value = both displays
        """
        if display != 2:
            self.showPattern(self.d1,pattern,2)
        
        if display != 1:
            self.showPattern(self.d2,pattern)
        
        
    def blink(self):
        """ Queue up blink animation frames for both eyes """
        self.addFrame(eye_lid1)
        self.addFrame(eye_lid2)
        self.addFrame(eye_lid3)
        self.addFrame(eye_lid2)
        self.addFrame(eye_lid1)
        self.addFrame(eye_open)
        
            
#Define colour codes and patterns
o = (0,0,0)
b = (0,0,200)
p = (255,153,204)
g = (0,255,0)
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

eye_left = [
o,w,w,o,o,
w,b,w,w,o,
w,b,b,w,o,
w,b,w,w,o,
o,w,w,o,o
]

eye_right = [
o,o,w,w,o,
o,w,b,w,w,
o,w,b,b,w,
o,w,b,w,w,
o,o,w,w,o
]

eye_downright = [
o,o,o,o,o,
o,o,w,w,o,
o,w,b,b,w,
o,w,b,b,w,
o,o,w,w,o
]

eye_downleft = [
o,o,o,o,o,
o,w,w,o,o,
w,b,b,w,o,
w,b,b,w,o,
o,w,w,o,o
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

red_eye_narrow = [
o,o,o,o,o,
o,w,w,w,o,
w,r,r,r,w,
o,w,w,w,o,
o,o,o,o,o
]

one = [
p,p,g,p,p,
p,g,g,p,p,
p,p,g,p,p,
p,p,g,p,p,
p,g,g,g,p
]

target = [
o,g,g,g,o,
g,r,r,r,g,
g,r,w,r,g,
g,r,r,r,g,
o,g,g,g,o
]

red_cross = [
o,r,r,r,o,
r,r,r,r,r,
r,r,r,r,r,
r,r,r,r,r,
o,r,r,r,o
]
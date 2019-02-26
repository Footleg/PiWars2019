#!/usr/bin/env python3

from rgbmatrix5x5 import RGBMatrix5x5

class LEDMatrixDisplays:

    def __init__(self):
        self.d1 = RGBMatrix5x5(0x74)
        self.d2 = RGBMatrix5x5(0x77)
        self.d1.clear()
        self.d1.show()
        self.d1.clear()
        self.d1.show()
        

    def showPattern(self,display,pattern):

        for y in range(0,5):
            for x in range(0,5):
                i = 5*y+x
                display.set_pixel(x,y,pattern[i][0],pattern[i][1],pattern[i][2])
        display.show()

    def openEyes(self):
        self.showPattern(self.d1,eye_open)
        self.showPattern(self.d2,red_eye)
        
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



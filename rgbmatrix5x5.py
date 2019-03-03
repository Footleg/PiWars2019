#!/usr/bin/env python3
""" Mock of Pimoroni 5x5 RGB LED matrix breakout board for PiWars 2019 robot Rocky Rover testing

    Represents a class to display LED states on pygame display surface.
    The mounted orientation of a pair of displays is encoded into this module based on
    how the actual displays (identified by their i2c addresses) are mounted on the robot
    so that the image on one is rendered upside down compared to the other.
"""
import pygame

LED_DIA = 8

class RGBMatrix5x5():
    ADDRESS = 0
    
    def __init__(self, address):
        self.ADDRESS = address
        self.clear()
        self.SCREEN = pygame.display.get_surface()
        
    def set_pixel(self, x,y,r,g,b):
        idx = y*5+x
        self.LEDS[idx] = [r,g,b]
        #print("Set pixel")
        
    def show(self):
        print("Update LEDS {}".format(self.ADDRESS) )
        if self.ADDRESS == 0x74:
            marginX = 170
        elif self.ADDRESS == 0x77:
            marginX = 530
        else:
            marginX = 800
        
        #Draw background rectangle
        pygame.draw.rect(self.SCREEN, (40,40,40),pygame.Rect(marginX-2,18,100,100) )
        if self.ADDRESS == 0x74:
            #Render array upside down (rotated 180 degrees)             
            for x in range(5):
                for y in range(5):
                    idx = 24 - (y*5+x)
                    pygame.draw.circle(self.SCREEN, self.LEDS[idx],(x*20+marginX+LED_DIA,y*20+20+LED_DIA),LED_DIA)
        else:
            #Render array upright             
            for x in range(5):
                for y in range(5):
                    idx = y*5+x
                    pygame.draw.circle(self.SCREEN, self.LEDS[idx],(x*20+marginX+LED_DIA,y*20+20+LED_DIA),LED_DIA)
    
    def clear(self):
        o = [0,0,0]
        self.LEDS = [
        o,o,o,o,o,
        o,o,o,o,o,
        o,o,o,o,o,
        o,o,o,o,o,
        o,o,o,o,o
        ]
    
             
def main():
    """ Test function for module
    """
    print("""This module cannot run stand alone. Use it from within a pygame application where
the screen has been initialised.""")
  
    
if __name__ == '__main__':
    main()
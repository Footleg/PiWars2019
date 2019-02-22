#!/usr/bin/env python3

""" Class to switch i2c channels using an AdaFruit TCA9548A 1-to-8 i2c
    multiplexer breakout board.
    
    Based on code written by Brian Corteil (Coretec Robotics) in 2017
    Updated by Footleg (2019) to use smbus2 and moved configuration of
    board i2c address into initialiser.
"""

from smbus2 import SMBus

class multiplexer:
    
    def __init__(self, bus, address):
        self.bus = SMBus(bus)
        self.address = address

    def channel(self, channel):
        """ Activate an i2c channel.
            Values 0-7 indicate the channel,
            any other value turns off all channels.
        """
        
        if   (channel==0): action = 0x01
        elif (channel==1): action = 0x02
        elif (channel==2): action = 0x04
        elif (channel==3): action = 0x08
        elif (channel==4): action = 0x10
        elif (channel==5): action = 0x20
        elif (channel==6): action = 0x40
        elif (channel==7): action = 0x80
        else : action = 0x00

        self.bus.write_byte_data(self.address,0x04,action)  #0x04 is the register for switching channels 

if __name__ == '__main__':
    
    bus=1       # 0 for rev1 boards 
    address=0x70
    
    plexer = multiplexer(bus,address)
    plexer.channel(7)
    
    print("Now run i2cdetect")

import time
import rtmidi
import numpy as np 

import game_modes as gm
import variables as v
import functions as f

midiout = f.get_midiout() 
play=True
with midiout: 
    while play: 
        print("")
        print("Choose Activity by Typing the activity number:")
        print("Chromatic Intervals (1); Major Scale (2); Root Intervals (3); Varying Intervals (4); Scale Intervals (5); Exit (-1)")
        try:
            mode = input("Choice of mode: ")
            
            if mode == "1": 
                gm.ear_chromatic(midiout)
                
            elif mode == "2":
                gm.ear_major_scale(midiout)
                
            elif mode == "3": 
                gm.play_root_intervals(midiout)
                
            elif mode == "4": 
                gm.play_varying_intervals(midiout)
                
            elif mode == "5": 
                gm.play_scale_intervals(midiout)
            
            elif mode == "b": 
                play = False
        except: 
            print("Invalid Mode!")
        
del midiout
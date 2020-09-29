import numpy as np

def key_lm_oct(): 
    key_letter_map = {}
    for i, kl in enumerate(keys_oct):
        key_letter_map[kl] = i 
    return key_letter_map

def key_nm(): #Key number map
    knm = {} 
    for i, k in enumerate(keys_oct): 
        knm[i] = k
    return knm

keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
keys_oct = [k + str(i) for i in range(0, 8) for k in keys] 
key_letter_map = {
        "A": [i for i in range(9, 120, 12)], 
        "A#": [i for i in range(10, 120, 12)], 
        "B": [i for i in range(11, 120, 12)], 
        "C": [i for i in range(0, 120, 12)],
        "C#": [i for i in range(1, 120, 12)],
        "D": [i for i in range(2, 120, 12)],
        "D#": [i for i in range(3, 120, 12)],
        "E": [i for i in range(4, 120, 12)],
        "F": [i for i in range(5, 120, 12)],
        "F#": [i for i in range(6, 120, 12)],
        "G": [i for i in range(7, 120, 12)],
        "G#": [i for i in range(8, 120, 12)]}
key_letter_map_oct = key_lm_oct()

key_number_map_oct = key_nm()

#Scales: 
ionian_scale =       [-12, -10, -8, -7, -5, -3, -1, 0, 2, 4, 5, 7, 9, 11, 12]
dorian_scale =       [-12, -10, -9, -7, -5, -3, -2, 0, 2, 3, 5, 7, 9, 10, 12]
phrygian_scale =    [-12, -11, -9, -7, -5, -4, -2, 0, 1, 3, 5, 7, 8, 10, 12]
lydian_scale =      [-12, -10, -8, -6, -5, -3, -1, 0, 2, 4, 6, 7, 9, 11, 12]
mixolydian_scale =  [-12, -10, -8, -7, -5, -3, -2, 0, 2, 4, 5, 7, 9, 10, 12]
aeolian_scale =     [-12, -10, -9, -7, -5, -4, -2, 0, 2, 3, 5, 7, 8, 10, 12]
locrian_scale =     [-12, -11, -9, -7, -6, -4, -2, 0, 1, 3, 5, 6, 8, 10, 12]

modes = {"ionian": ionian_scale, 
         "dorian": dorian_scale, 
         "phrygian": phrygian_scale, 
         "lydian": lydian_scale, 
         "mixolydian": mixolydian_scale, 
         "aeolian": aeolian_scale, 
         "locrian": locrian_scale}


#Soon: Chords

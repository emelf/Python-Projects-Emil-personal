import time
import rtmidi
import numpy as np 

import game_modes as gm
import variables as v
import functions as f

def save_score(gamemode, score, total): 
    file = open("scores.txt", 'a')
    file.write("Gamemode {}: {}:{} \n".format(gamemode, score, total))
    file.close()
    

key_number_map = {"A":57, "A#":58, "Bb":58, "B":59, "Cb":59, "C":60, "C#":61, "Db":61, "D":62, "Eb":62, 
                  "E":63, "F":64, "F#":65, "Gb":65, "G":66, "G#":67, "Ab":67}

key_number_map3 = {"A": [i for i in range(9, 120, 12)], 
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

#Generate dict of key number -> key letter: 
keys = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
key_map_numbers = {}
j = 0
for i in range(0, 109): 
    index = 3 + i - 12*j #Starts with C at i = 0
    if index > 11: 
        j += 1
        index = 0
    key_map_numbers[i] = keys[index]+str(j)
    
key_number_map2 = {} 
for el in key_map_numbers: 
    key_number_map2[key_map_numbers[el]] = el

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")
    
def chromatic(midiout, tempo, N, key_start=60): #60 = middel C
    t_on = 3/4 * (tempo/60)**-1
    t_off = 1/4 * (tempo/60)**-1 
    try:
        note = key_start
        N_int = int(N)
        for i in range(N_int):
            note_on = [0x90, note, 112] # channel 1, middle C, velocity 112
            note_off = [0x80, note, 0]
            time.sleep(t_off)
            midiout.send_message(note_on)
            time.sleep(t_on)
            midiout.send_message(note_off)
            note += np.random.choice([-1, 1])
    except:
        print("Invalid argument!")
    
def play_chromatic(midiout): 
    play = True
    notes = int(input("Number of notes each level: "))
    while play: 
        level = float(input("Choose Level: "))
        try:
            tempo = 60 + level*5
            chromatic(midiout, tempo, notes)
            keep_playing = input("Play again? (y/n): ")
            play = True if keep_playing=="y" else False
        
        except: 
            print("ERROR: Invalid argument!")
     
        
def major_scale(midiout, tempo, N, key_start="C"):
    #Ionian Scale:  [-12, -10, -8, -7, -5, -3, -1, +0, +2, +4, +5, +7, +9, +11, +12] adding to the root note
    try: 
        t_on = 3/4 * (tempo/60)**-1
        t_off = 1/4 * (tempo/60)**-1 
        note_start = key_number_map[key_start]
        note = note_start
        for i in range(N): 
            note_on = [0x90, note, 112] # channel 1, middle C, velocity 112
            note_off = [0x80, note, 0]
            time.sleep(t_off)
            midiout.send_message(note_on)
            time.sleep(t_on)
            midiout.send_message(note_off)
            note = note_start + np.random.choice([-12, -10, -8, -7, -5, -3, -1, 0, 2, 4, 5, 7, 9, 11, 12])
    except: 
        pass
            
def play_major(midiout): 
    play = True
    start_note = input("Input root note: ")
    notes = int(input("Number of notes each level: "))
    while play: 
        level = float(input("Choose Level: "))
        try:
            tempo = 60 + level*5
            major_scale(midiout, tempo, notes, key_start=start_note)
            keep_playing = input("Play again? (y/n): ")
            play = True if keep_playing=="y" else False
        
        except: 
            print("ERROR: Invalid argument!")
            break


def root_intervals(midiout): 
    play = True
    mode = True
    print("\n\n")
    print("Welcome to the first exercise: Root Intervals ")
    print("Try to guess the interval in number of half-note steps.")
    print("Difficulty is selected by standard deviation from root note. Level number is the standard deviation.")
    
    while mode:
        try:
            start_key = input("Starting Key (exit = b):")
            if start_key == "b":  
                break
            start_key = key_number_map2[start_key]
            level = float(input("Level: "))
            score = 0
            tries = 0
            print("")
            print("Guess interval number (exit = b):")
            while play: 
                interval = round(np.random.normal(0, level))
                while interval == 0:
                    interval = round(np.random.normal(0, level))
                note = start_key + interval
                
                root_on = [0x90, start_key, 112]
                root_off = [0x80, start_key, 0]
                note_on = [0x90, note, 112]
                note_off = [0x80, note, 0]
                
                midiout.send_message(root_on)
                time.sleep(0.5)
                midiout.send_message(root_off)
                time.sleep(0.05)
                midiout.send_message(note_on)
                time.sleep(0.5)
                midiout.send_message(note_off)
                time.sleep(0.05)
                tries += 1
                
                guessed = False
                while not guessed:
                    print("Exit: b; Repeat: r")
                    guess = input("Intervals = ")
                    if guess == 'r': 
                        midiout.send_message(root_on)
                        time.sleep(0.5)
                        midiout.send_message(root_off)
                        time.sleep(0.05)
                        midiout.send_message(note_on)
                        time.sleep(0.5)
                        midiout.send_message(note_off)
                        time.sleep(0.05)
                    else: 
                        guessed = True
                
                if start_key + int(guess) == note: 
                    score += 1
                    print("Correct! The key goes from {} to {}. Score = {}/{}".format(
                        key_map_numbers[start_key], key_map_numbers[note], score, tries))
                    
                elif guess == "b": 
                    play=False
                else:
                    print("Wrong! The actual interval was {}, and the note went from {} to {}.".format(
                        note-start_key, key_map_numbers[start_key], key_map_numbers[note]))
                time.sleep(0.2)
                
        except: 
            print("Some invalid argument!")
            
            
def varying_intervals(midiout): 
    play = True
    mode = True
    print("\n\n")
    print("Welcome to the exercise: Varying Intervals ")
    print("Exercise for a constant interval. User specifies what interval and then get asked for what the new note is.")
    print("Difficulty is selected by specifying maximum interval allowed")
    
    while mode:
        try:
            print("Choose note range: ")
            print("C2 to C4 (1); C3 to C5 (2); C2 to C5 (3)")
            note_range = input("Note range (exit = b):")
            if note_range == "b":  
                break
            #Make the allowed note range    
            if note_range == "1": 
                allowed_notes = [i for i in range(36, 61, 1)]
            elif note_range == "2": 
                allowed_notes = [i for i in range(48, 73, 1)]
            elif note_range == "3": 
                allowed_notes = [i for i in range(36, 73, 1)]
            
            else: 
                print("No range selected: Playing from C3 to C5")
                allowed_notes = [i for i in range(48, 73, 1)]
                
            diff = int(input("Max interval number: "))
            diff = np.delete([i for i in range(-diff, diff+1, 1)], diff) #Deletes the zero in the interval array
            score = 0
            tries = 0
            print("")
            print("Guess New note (exit = b, repeat note = r):")
            while play: 
                root_note = np.random.choice(allowed_notes)
                note = root_note + np.random.choice(diff)
                
                root_on = [0x90, root_note, 112]
                root_off = [0x80, root_note, 0]
                note_on = [0x90, note, 112]
                note_off = [0x80, note, 0]
                
                midiout.send_message(root_on)
                time.sleep(0.65)
                midiout.send_message(root_off)
                time.sleep(0.05)
                midiout.send_message(note_on)
                time.sleep(0.65)
                midiout.send_message(note_off)
                time.sleep(0.3)
                midiout.send_message(root_on)
                midiout.send_message(note_on)
                time.sleep(0.5)
                midiout.send_message(root_off)
                midiout.send_message(note_off)
                time.sleep(0.02)
                
                #Find the note: 
                for el in key_number_map3: 
                    root_trig = False
                    note_trig = False
                    
                    if root_note in key_number_map3[el]: 
                        root_note_letter = el 
                        root_trig = True
                    if note in key_number_map3[el]: 
                        note_letter = el 
                        note_trig = True
                        
                    if root_trig and note_trig: #Breaks the loop when found both notes. 
                        break 
                
                guessed = False
                while not guessed:
                    guess = input("Played note: {}. New note = ".format(root_note_letter))
                    if guess == 'r': 
                        midiout.send_message(root_on)
                        time.sleep(0.5)
                        midiout.send_message(root_off)
                        time.sleep(0.05)
                        midiout.send_message(note_on)
                        time.sleep(0.5)
                        midiout.send_message(note_off)
                        time.sleep(0.05)
                    else: 
                        guessed = True
                
                if guess == note_letter: 
                    tries += 1
                    score += 1
                    print("Correct! Score = {}/{}".format(score, tries))
                    
                elif guess == "b": 
                    play=False
                    save_score(4, score, tries)
                else:
                    tries += 1
                    print("Wrong! The note went from {} to {}. Score = {}/{}.".format(root_note_letter, note_letter, score, tries))
                time.sleep(0.2)
                
        except: 
            print("Some invalid argument!")        
    

#Program: 
with midiout:
    while True: 
        print("")
        print("Choose Activity by Typing the activity number:")
        print("Chromatic Intervals (1); Major Scale (2); Root Intervals (3); Varying Intervals (4); Exit (-1)")
        try:
            mode = input("Choice of mode: ")
            
            if mode == "1": 
                play_chromatic(midiout)
                
            elif mode == "2": 
                play_major(midiout)
                
            elif mode == "3": 
                root_intervals(midiout)
                
            elif mode == "4": 
                varying_intervals(midiout)
                
            elif mode == "b": 
                break
            
        except: 
            print("Invalid Mode!")
        

del midiout
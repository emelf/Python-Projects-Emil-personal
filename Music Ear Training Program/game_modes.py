import numpy as np
import time

import functions as f
import variables as v 

def ear_chromatic(midiout): #60 = middel C
    mode = True
    while mode:
        try:
            play=True
            N_notes = int(input("Number of notes each level: "))
            note_letter = input("Starting key (specify note and octave): ")
            tempo = float(input("Choose Tempo: "))
            t = f.calc_time(tempo)
            t_on = 3/4*t
            t_off = 1/4*t 
            
            while play:
                note = f.find_key_number(note_letter)
                all_keys = [note_letter]
                f.play_one(midiout, note, t_on, t_off)
                for i in range(N_notes):
                    note += np.random.choice([-1, 1])
                    all_keys.append(f.find_key_letter(note, exact=True))
                    f.play_one(midiout, note, t_on, t_off)
                    
                print("Notes are: ... ")
                time.sleep(1)
                print(str(all_keys))
                print("")
                play_ask = input("Play Again? (y/n): ")
                if not play_ask == "y": 
                    play = False
        except:
            print("Invalid argument!")
        keep_playing = input("Keep playing? (y/n): ")
        if not keep_playing == "y": 
            mode = False
      
def ear_major_scale(midiout):
    relative_notes = [-12, -10, -8, -7, -5, -3, -1, 0, 2, 4, 5, 7, 9, 11, 12]
    mode = True
    while mode:
        try:
            play=True
            N_notes = int(input("Number of notes each loop: "))
            note_letter = input("Starting key (specify note and octave): ")
            tempo = float(input("Choose Tempo: "))
            t = f.calc_time(tempo)
            t_on = 3/4*t
            t_off = 1/4*t 
            
            while play:
                note0 = f.find_key_number(note_letter)
                all_keys = [note_letter]
                f.play_one(midiout, note0, t_on, t_off)
                for i in range(N_notes):
                    note = note0 + np.random.choice(relative_notes)
                    all_keys.append(f.find_key_letter(note, exact=True))
                    f.play_one(midiout, note, t_on, t_off)
                    
                print("Notes are: ... ")
                time.sleep(1)
                print(str(all_keys))
                print("")
                play_ask = input("Play Again? (y/n): ")
                if not play_ask == "y": 
                    play = False
        except:
            print("Invalid argument!")
        keep_playing = input("Keep playing? (y/n): ")
        if not keep_playing == "y": 
            mode = False
                        
def play_root_intervals(midiout): 
    play = True
    mode = True
    print("")
    print("Welcome to the first exercise: Root Intervals")
    print("Try to guess the interval in number of half-note steps.")
    print("Difficulty is selected by standard deviation from root note. Level number is the standard deviation.")
    print("Exit with b")
    print("")
    while mode:
        try:
            start_key = input("Starting Key (exit = b):")
            
            if start_key == "b":  
                break
            start_note = f.find_key_number(start_key)
            level = float(input("Level: "))
            score = 0
            tries = 0
            
            while play: 
                interval = round(np.random.normal(0, level))
                while interval == 0:
                    interval = round(np.random.normal(0, level))
                note = start_note + interval
                f.play_induvidual(midiout, [start_note, note], [0.6, 0.6], [0.2, 0.3])
                f.play_together(midiout, [start_note, note], 0.6)
                
                guessed = False
                while not guessed:
                    guess = input("(repeat = r) Intervals: ")
                    if guess == 'r': 
                        f.play_induvidual(midiout, [start_note, note], [0.6, 0.6], [0.2, 0.3])
                        f.play_together(midiout, [start_note, note], 0.6)
                    else: 
                        guessed = True
                if guess == "b": 
                    play=False
                    f.save_score(3, score, tries, level)
                    
                elif start_note + int(guess) == note: 
                    tries += 1
                    score += 1
                    print("Correct! The key goes from {} to {}. Score = {}/{}".format(
                        start_key, f.find_key_letter(note), score, tries))
                    
                
                else:
                    tries += 1
                    print("Wrong! The actual interval was {}, and the note went from {} to {}. Score = {}/{}".format(
                        interval, start_key, f.find_key_letter(note), score, tries))
                time.sleep(0.2)
   
        except: 
            f.save_score(3, score, tries, level)
            print("Some invalid argument!")
            
    
def play_varying_intervals(midiout): 
    play = True
    mode = True
    print("")
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
                f.play_induvidual(midiout, [root_note, note], [0.6, 0.6], [0.3, 0.3])
                f.play_together(midiout, [root_note, note], 0.6)             
                #Find the note: 
                root_note_letter = f.find_key_letter(root_note, exact=False)
                note_letter = f.find_key_letter(note, exact=False)
                
                guessed = False
                while not guessed:
                    guess = input("Played note: {}. New note = ".format(root_note_letter))
                    if guess == 'r': 
                        f.play_induvidual(midiout, [root_note, note], [0.6, 0.6], [0.3, 0.3])
                        f.play_together(midiout, [root_note, note], 0.6) 
                    else: 
                        guessed = True
                        
                if guess == "b": 
                    play=False
                    f.save_score(4, score, tries, diff)
                
                elif guess == note_letter: 
                    tries += 1
                    score += 1
                    print("Correct! Score = {}/{}".format(score, tries))
                
                else:
                    tries += 1
                    print("Wrong! The note went from {} to {}. Score = {}/{}.".format(root_note_letter, note_letter, score, tries))
                time.sleep(0.2)
                
        except: 
            f.save_score(4, score, tries, diff)
            print("Some invalid argument!")        


def play_scale_intervals(midiout): 
    play = True
    mode = True
    print("")
    print("Welcome to the exercise: Scale Intervals ")
    print("Random intervals in a given scale.")
    print("Difficulty is selected by specifying maximum interval allowed")
    
    while mode:
        try:
            play=True
            print("Specify scale: Ionian; Dorian; Phrygian; Lydian; Mixolydian; Aeolian; Locrian")
            scale = input("Scale: ").lower() 
            if scale == "b": 
                break 
            key = input("What key is the scale? ")
            if key == "b": 
                break 
            scale_notes = v.modes[scale]
            scale_notes = np.delete(scale_notes, 7)
            key_number = f.find_key_number(key)
            score = 0
            tries = 0
            print("")
            print("Guess New note (exit = b, repeat note = r):")
            while play: 
                root_note = key_number
                note = root_note + np.random.choice(scale_notes)
                f.play_induvidual(midiout, [root_note, note], [0.6, 0.6], [0.3, 0.3])
                f.play_together(midiout, [root_note, note], 0.6)             
                #Find the note: 
                root_note_letter = f.find_key_letter(root_note, exact=False)
                note_letter = f.find_key_letter(note, exact=False)
                
                guessed = False
                while not guessed:
                    guess = input("Played note: {}. New note = ".format(root_note_letter))
                    if guess == 'r': 
                        f.play_induvidual(midiout, [root_note, note], [0.6, 0.6], [0.3, 0.3])
                        f.play_together(midiout, [root_note, note], 0.6) 
                    else: 
                        guessed = True
                        
                if guess == "b": 
                    play=False
                    f.save_score(5, score, tries, scale)
                
                elif guess == note_letter: 
                    tries += 1
                    score += 1
                    print("Correct! Score = {}/{}".format(score, tries))
                
                else:
                    tries += 1
                    print("Wrong! The note went from {} to {}. Score = {}/{}.".format(root_note_letter, note_letter, score, tries))
                time.sleep(0.2)
                
        except: 
            f.save_score(5, score, tries, scale)
            print("Some invalid argument!")  
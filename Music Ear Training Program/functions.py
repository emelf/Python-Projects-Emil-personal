#https://spotlightkid.github.io/python-rtmidi/
import numpy as np 
import time 
import rtmidi

import variables as v

def save_score(gamemode, score, total, level): 
    """"save_score(gamemode, score, total, level)"""
    file = open("scores.txt", 'a')
    file.write("Gamemode_{};{};{};{} \n".format(gamemode, score, total, level))
    file.close()
    
def get_midiout(): 
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    
    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("My virtual output")
    return midiout

def calc_time(bpm): 
    """calc_time(bpm)"""
    t = (bpm/60)**-1
    return t #where t is the time of one beat (1/4'th note)

def find_key_letter(key, exact=True): 
    """Finds the letter to a key number -> find_key_letter(key, exact=False)"""
    if exact: 
        return v.key_number_map_oct[key]
    else: 
        for k in v.key_letter_map: 
            if key in v.key_letter_map[k]: 
                key_letter = k
                break 
        return key_letter

def find_key_number(key): 
    """Finds the number of a key letter"""     
    return v.key_letter_map_oct[key]

def play_one(midiout, note, t_on, t_off=0): 
    """play_one(midiout, note, t_on, t_off=0)"""
    note_on = [0x90, note, 112] # channel 1, middle C, velocity 112
    note_off = [0x80, note, 0]
    midiout.send_message(note_on)
    time.sleep(t_on)
    midiout.send_message(note_off)
    time.sleep(t_off + 0.02)
    
def play_induvidual(midiout, notes, t_ons, t_offs):
    """play_induvidual(midiout, notes, t_ons, t_offs)"""
    for note, t_on, t_off in zip(notes, t_ons, t_offs):
        play_one(midiout, note, t_on)
        time.sleep(t_off) 
    time.sleep(0.02)
    
def play_together(midiout, notes, t_on): 
    """play_together(midiout, notes, t_on)"""
    notes_on = [] 
    notes_off = [] 
    for note in notes: 
        notes_on.append([0x90, note, 112])
        notes_off.append([0x80, note, 0])
    #Play the notes
    for n_on in notes_on: 
        midiout.send_message(n_on)
    time.sleep(t_on) 
    for n_off in notes_off: 
        midiout.send_message(n_off)
    time.sleep(0.02)

if __name__ == "__main__":        
    midiout = get_midiout()
    play_one(midiout, 60, 1)
    time.sleep(1)
    play_induvidual(midiout, [60,61,62], [0.3,0.3,0.3], [0.1,0.1,0.1])
    time.sleep(1)
    play_together(midiout, [60,64], 1)

    midiout.close_port()
    del midiout 
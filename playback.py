import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import base64
from music21 import midi

def play_music(music_file):
 
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        #print("Music file %s loaded!" % music_file)
    except pygame.error:
        #print("File %s not found! (%s)" % (music_file, pygame.get_error())) 
        return
    pygame.mixer.music.play(0)
    while pygame.mixer.music.get_busy():
        clock.tick(30)

def midiToBase64(music_file):
    mid64 = base64.b64encode(open(music_file, 'rb').read())
    #print(mid64)
    # convert back to a binary midi and save to a file in the working directory
    #return base64.b64decode(mid64)
    return mid64

if __name__ == "__main__":

    music_file = "bwv-773.mid"
    mid64 = midiToBase64(music_file)
    #freq, bitsize, channels, buffer
    pygame.mixer.init(44100, -16, 2, 1024)
    
    try:
        play_music(music_file)
    except KeyboardInterrupt:

        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit
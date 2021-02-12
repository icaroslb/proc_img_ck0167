import pygame
import base64
from music21 import midi

def play_music(music_file):
 
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print("Music file %s loaded!" % music_file)
    except pygame.error:
        print("File %s not found! (%s)" % (music_file, pygame.get_error())) 
        return
    pygame.mixer.music.play(0)
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)

if __name__ == "__main__":
    mid64 = base64.b64encode(open("bwv-773.mid", 'rb').read())
    #print(mid64)
    music_file = "bwv-773.mid"
    
    # convert back to a binary midi and save to a file in the working directory
    fish = base64.b64decode(mid64)
    fout = open(music_file,"wb")
    fout.write(fish)
    fout.close()
    
    freq = 44100    # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2    # 1 is mono, 2 is stereo
    buffer = 1024    # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)
    
    try:
        # use the midi file you just saved
        play_music(music_file)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit
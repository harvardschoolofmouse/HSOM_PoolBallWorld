#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 17:00:42 2020

@author: lilis
"""
import pygame
import sys
import os
import random

# to include images, we need the png sources in the working directory
# I'll use John's head as example - johnpic.jpg

_image_library = {}
image = pygame.image.load('johnpic.jpg')
_songs = ['stressclock.mp3', 'stressclock.mp3']#'stresspulse.mp3']
_currently_playing_song = None


def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image

def play_a_different_song():
    global _currently_playing_song, _songs
    next_song = random.choice(_songs)
    while next_song == _currently_playing_song:
        next_song = random.choice(_songs)
        _currently_playing_song = next_song
        pygame.mixer.music.load(next_song)
        pygame.mixer.music.play()
        
_sound_library = {}
def play_sound(path):
    global _sound_library
    sound = _sound_library.get(path)
    if sound == None:
        cannonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(cannonicalized_path)
        _sound_library[path] = sound
    sound.play()
    
    


pygame.init()


# Including music -- can play a song once or on a loop
pygame.mixer.music.load('stressclock.mp3')
pygame.mixer.music.play(-1) # indexes from 1, so zero means play once.
# to play infinitely, use -1, to play once is 0
# pygame.mixer.music.stop() -- stops current song and also erases whole queue



# window of desired size, a surface obj
screen = pygame.display.set_mode((400,300))
done = False
is_blue = True
x = 30
y = 30    

clock = pygame.time.Clock()

while not done:
    
    
    
    # pygame.event.get() clears the event 
    #queue. If don't call, the window's 
    #messages will pile up, game gets slow
    # EVENT PUMPING
    for event in pygame.event.get():
        # pygame.QUIT called when you hit 
        # x marker in corner
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue
        
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: y -= 3
    if pressed[pygame.K_DOWN]: y += 3
    if pressed[pygame.K_LEFT]: x -= 3
    if pressed[pygame.K_RIGHT]: x += 3
    
    if x < 0 or y < 0 or x>400 or y>300:
#        pygame.mixer.music.load('stresspulse.mp3')
#        pygame.mixer.music.play(0)
        # this version plays our sound only once
        effect = pygame.mixer.Sound('stresspulse.mp3')
        effect.play(0)
        # queues the next song to start after...
#        pygame.mixer.music.queue('stressclock.mp3')
    
    #interactivity from if statements in the event queue
    if is_blue: 
        color = (0,128,255)
    else: 
        color = (255,100,0)
    # display some objects
    # first, reset the screen before displaying things otherwise won't update right:
    screen.fill((0,0,0))
    # render the rect
    pygame.draw.rect(screen, color, pygame.Rect(x,y,60,60))
    
    
    # Create a surface object on which we will put an image. 
    #If no image, it's just a black square
    # The SRCALPHA makes an empty transparent image, we can't see it
    surface = pygame.Surface((100,100), pygame.SRCALPHA)
    screen.blit(get_image("johnpic.jpg"), (400-x,300-y))
            
    # pygame is double buffered -- has 2 
    # buffers. Whatever is the latest screen
    # needs to be displayed. So a load
    # buffer and a display buffer
    pygame.display.flip()
    
    # We first adjust the frame update rate to be reasonable
    clock.tick(60) # wait 1/60s before executing this loop, 60fps
    
        
    

pygame.quit()
sys.exit()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 18:55:26 2020

@author: lilis
"""

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

tableSize = [8*100, 4*100] 
tableEdges = 20

# to include images, we need the png sources in the working directory
# I'll use John's head as example - johnpic.jpg

_image_library = {}
#image = pygame.image.load('johnpic.jpg')
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
image = get_image('johnpic.jpg')

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
    
    
def draw_grid(surface, tableSize, tableEdges):
    global _text
    pocket_topleft_top = pygame.draw.rect(surface, (255,0,0), (0,0,50+tableEdges,tableEdges))
    pocket_topleft_left = pygame.draw.rect(surface, (255,0,0), (0,0,tableEdges,50+tableEdges))
    pocket_bottomright_bottom = pygame.draw.rect(surface, (255,0,0), (tableSize[0]-50+tableEdges,tableSize[1]+tableEdges,50+tableEdges,tableEdges))
    pocket_bottomright_right = pygame.draw.rect(surface, (255,0,0), (tableSize[0]+tableEdges,tableSize[1]-50+tableEdges,tableEdges,50+tableEdges))
    pocket_topright_top = pygame.draw.rect(surface, (255,0,0), (tableSize[0]-50+tableEdges,0,50+tableEdges,tableEdges))
    pocket_topright_right = pygame.draw.rect(surface, (255,0,0), (tableSize[0]+tableEdges,0,tableEdges,50+tableEdges))
    pocket_bottomleft_bottom = pygame.draw.rect(surface, (255,0,0), (0,tableSize[1]+tableEdges,50+tableEdges,tableEdges))
    pocket_bottomleft_left = pygame.draw.rect(surface, (255,0,0), (0,tableSize[1]-50+tableEdges,tableEdges,50+tableEdges))

    wall_top = pygame.draw.rect(surface, (0,0,0), (50+tableEdges,0,tableSize[0]-100,tableEdges))
    wall_left = pygame.draw.rect(surface, (0,0,0), (0,50+tableEdges,tableEdges,tableSize[1]-100))
    wall_bottom = pygame.draw.rect(surface, (0,0,0), (50+tableEdges,tableSize[1]+tableEdges,tableSize[0]-100,tableEdges))
    wall_right = pygame.draw.rect(surface, (0,0,0), (tableSize[0]+tableEdges,50+tableEdges,tableEdges,tableSize[1]-100))
    
    pockets = {'topleft': (pocket_topleft_top,pocket_topleft_left), 'topright': (pocket_topright_right,pocket_topright_top), 'bottomleft': (pocket_bottomleft_bottom, pocket_bottomleft_left), 'bottomright': (pocket_bottomright_right, pocket_bottomright_bottom)}
    walls = {'wall_top': wall_top, 'wall_left': wall_left, 'wall_bottom': wall_bottom, 'wall_right':wall_right}
    table = pygame.draw.rect(screen, (255,255,255), (tableEdges,tableEdges, tableSize[0], tableSize[1]))
    color = (0.8*255,0.8*255,0.8*255)
    xpnts = range(1, tableSize[0], 100)
    ypnts = range(1, tableSize[1], 100)
    for i in range(1,len(xpnts)):
        pygame.draw.line(surface, color, (xpnts[i]+tableEdges,1+tableEdges), (xpnts[i]+tableEdges,tableSize[1]+tableEdges), 1)
    for i in range(1,len(ypnts)):
        pygame.draw.line(surface, color, (1+tableEdges,ypnts[i]+tableEdges), (tableSize[0]+tableEdges,ypnts[i]+tableEdges), 1)
        
#    _text = font.render("Wall", True, (255,255,255))
#    surface.blit(_text,((50+tableSize[0])/2 - _text.get_width()//2, 0))
    return (table, pockets, walls)
    
    
    


pygame.init()
# text seems buggy so maybe don't use
#font = pygame.font.SysFont("helvetica", 20)
#_text = font.render("Wall", True, (0,120,0))


# Including music -- can play a song once or on a loop
pygame.mixer.music.load('stressclock.mp3')
pygame.mixer.music.play(-1) # indexes from 1, so zero means play once.
# to play infinitely, use -1, to play once is 0
# pygame.mixer.music.stop() -- stops current song and also erases whole queue



# window of desired size, a surface obj
screen = pygame.display.set_mode((tableSize[0] + 2*tableEdges,tableSize[1] + 2*tableEdges))


table = draw_grid(screen, tableSize,tableEdges)
 
done = False
has_collided = False
xs = [30,60,600]
ys = [30,100,300]
colors = [(0,128,255), (255,100,0), (100,255,0)]


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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                has_collided = not has_collided
            elif event.key == pygame.K_ESCAPE:
                done = True
        
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: ys[0] -= 3
    if pressed[pygame.K_DOWN]: ys[0] += 3
    if pressed[pygame.K_LEFT]: xs[0] -= 3
    if pressed[pygame.K_RIGHT]: xs[0] += 3
    
    if not all(i > 0 and i < tableSize[0] for i in xs) or not all(i > 0 and i < tableSize[1] for i in ys):
#        pygame.mixer.music.load('stresspulse.mp3')
#        pygame.mixer.music.play(0)
        # this version plays our sound only once
        effect = pygame.mixer.Sound('stresspulse.mp3')
        effect.play(0)
        # queues the next song to start after...
#        pygame.mixer.music.queue('stressclock.mp3')
    
    #interactivity from if statements in the event queue
    if has_collided: 
        colors[0] = (255,0,0)
    else: 
        colors[0] = (0,128,255)
    # display some objects
    # first, reset the screen before displaying things otherwise won't update right:
    screen.fill((0,0,0))
    # draw the grid
    table,pockets,walls = draw_grid(screen, tableSize,tableEdges)
    # draw our pool balls
    for i in range(0, len(xs)):
        pygame.draw.circle(screen, colors[i], (xs[i],ys[i]),23)
    

            
    # pygame is double buffered -- has 2 
    # buffers. Whatever is the latest screen
    # needs to be displayed. So a load
    # buffer and a display buffer
    pygame.display.flip()
    
    # We first adjust the frame update rate to be reasonable
    clock.tick(60) # wait 1/60s before executing this loop, 60fps
    
        
    

pygame.quit()
sys.exit()
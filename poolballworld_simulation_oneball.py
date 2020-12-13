#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 18:55:26 2020

@author: A Hamilos [ahamilos at g.harvard.edu]

This version intended for construction, testing and debugging.
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
import math


# import params from Julia
_tableSize = [3*100, 3*100] 
_tableEdges = 20
_ballRadius = 23

# to include images, we need the png sources in the working directory
# I'll use John's head as example - johnpic.jpg

_image_library = {}
#image = pygame.image.load('johnpic.jpg')
_songs = ['stressclock.mp3', 'stressclock.mp3']#'stresspulse.mp3']
_currently_playing_song = None


class SceneBase:
    def __init__(self):
        self.next = self
    def ProcessInput(self, events):
        # receives all events occurring since last frame
        print("You didn't overwrite this")
    def Update(self):
        # going to act on the objects
        print("rbf")
    def Render(self, screen):
        # will overwrite the previous screen
        print("rbf")
    def switchToScene(self, next_scene):
        self.next = next_scene
    


class Wall:
    def __init__(self):
        global _tableSize, _tableEdges
        self.font = pygame.font.SysFont('Arial', 25)
        pygame.display.set_caption('Box Test')
        self.screen = pygame.display.set_mode((600,400), 0, 32)
        self.screen.fill((white))
        pygame.display.update()


    def addRect(self):
        self.rect = pygame.draw.rect(self.screen, (black), (175, 75, 200, 100), 2)
        pygame.display.update()

    def addText(self):
        self.screen.blit(self.font.render('Hello!', True, (255,0,0)), (200, 100))
        pygame.display.update()
        
class Pocket(object):
    def __init__(self):
        global _tableSize, _tableEdges
        self.font = pygame.font.SysFont('Arial', 25)
        pygame.display.set_caption('Box Test')
        self.screen = pygame.display.set_mode((600,400), 0, 32)
        self.screen.fill((white))
        pygame.display.update()


    def addRect(self):
        self.rect = pygame.draw.rect(self.screen, (black), (175, 75, 200, 100), 2)
        pygame.display.update()

    def addText(self):
        self.screen.blit(self.font.render('Hello!', True, (255,0,0)), (200, 100))
        pygame.display.update()

class Ball:
    def __init__(self, x, y, speed, angle, ballNo):
        global _ballRadius
        self.ballRadius = _ballRadius
        self.x = x
        self.y = y
        self.ballNo = ballNo
        if self.ballNo == 1:
            self.color = (0,0,255)#(255,0,0)
        elif self.ballNo == 2:
            self.color = (0,255,0)
        else:
            self.color = (0,0,255)
        self.speed = speed
        self.angle = angle
        
        # render and create object we can use to check for collisions
#        self.object = surface.get_circle()#pygame.draw.circle(screen, self.color, (xs[i],ys[i]),23)
        
        
#        self.surface = pygame.Surface((ballRadius*2,ballRadius*2))
#        self.rect = self.surface.get_rect(center = (self.x, self.y))
#        self.circle = pygame.draw.circle(self.surface, self.color, (ballRadius,ballRadius),ballRadius)
        ball_surface = pygame.Surface((_ballRadius*2,_ballRadius*2), pygame.SRCALPHA)
        rect = ball_surface.get_rect(center = (self.x, self.y))
        pygame.draw.circle(ball_surface, self.color, (self.ballRadius,self.ballRadius),self.ballRadius)
        self.ball_surface = ball_surface
        self.rect = rect
        
        
    def proposeX(self, update=False):
        s = self.speed
        th = self.angle
        x = self.x + s*math.cos(th)
        if update:
            self.x = x
        return x
    def proposeY(self, update=False):
        s = self.speed
        th = self.angle
        y = self.y - 1*s*math.sin(th)
        if update:
            self.y = y
        return y
        
    def bounce(self, objects):
        global _tableSize, _tableEdges
        leftwall = _tableEdges
        rightwall = _tableSize[0]+_tableEdges
        topwall = _tableEdges
        bottomwall = _tableSize[1]+_tableEdges
#        width = tableSize[0]+tableEdges
#        height = tableSize[1]+tableEdges
        x = self.proposeX()
        y = self.proposeY()
        
#        if x > width - self.ballRadius:
        if x > rightwall - self.ballRadius:
            self.x = 2 * (rightwall - self.ballRadius) - self.x
            self.angle = math.pi - self.angle
#        elif x < self.ballRadius+tableEdges:
        elif x < leftwall+self.ballRadius:
            self.x = 2 * (leftwall+self.ballRadius) - self.x
            self.angle = math.pi - self.angle
        else:
            self.x = x
            
        if y > bottomwall - self.ballRadius:
            self.y = 2 * (bottomwall - self.ballRadius) - self.y
            self.angle = - self.angle
        elif y < topwall+self.ballRadius:
            self.y = 2 * (topwall+self.ballRadius) - self.y
            self.angle = - self.angle
        else:
            self.y = y
            
            
    def updateX(self):      
        self.rect.centerx = round(self.x)
    def updateY(self):
        self.rect.centery = round(self.y)
        
    def checkCollision(self,other_objects):
        for i in other_objects:
            if self.rect.colliderect(other_objects[i]):
                print(True)
                
#            else:
#                nothing
#                print(False)
    def render(self, screen):
        # draw our pool balls
#        self.surface = pygame.Surface((ballRadius*2,ballRadius*2))
#        self.rect = self.surface.get_rect(center = (self.x, self.y))
#        self.circle = pygame.draw.circle(self.surface, self.color, (self.ballRadius,self.ballRadius),self.ballRadius)
#        screen.blit(self.surface, (xs[0]-self.ballRadius, ys[0]-self.ballRadius))
#        ball_surface = pygame.Surface((ballRadius*2,ballRadius*2))
#        ball_surface.get_rect(center = (self.x, self.y))
#        ball = pygame.draw.circle(ball_surface, self.color, (self.ballRadius,self.ballRadius),self.ballRadius)
#        screen.blit(self.ball_surface, (self.x-self.ballRadius, self.y-self.ballRadius))
#        screen.blit(self.ball_surface, ball_surface.get_rect(center = (self.x, self.y)))
        rect = self.rect
        screen.blit(self.ball_surface, rect)
        
#        ball = pygame.draw.circle(ball_surface, self.color, (self.ballRadius,self.ballRadius),self.ballRadius)

        
    def addText(self):
        self.screen.blit(self.font.render('Hello!', True, (255,0,0)), (200, 100))
        pygame.display.update()
        
        
def collide(b1, b2):
    elasticity = 1
    dx = b1.x - b2.x
    dy = b1.y - b2.y
    
    distance = math.hypot(dx, dy)
    if distance < b1.ballRadius + b2.ballRadius:
        tangent = math.atan2(dy, dx)
        b1.angle = math.pi + 2 * tangent - b1.angle #math.pi + 
#        b1.angle = 3*math.pi/2 + tangent - b1.angle #math.pi + 
        b2.angle = math.pi + 2 * tangent - b2.angle #math.pi + 
#        b2.angle = 3*math.pi/2 * tangent - b2.angle #math.pi + 
        (b1.speed, b2.speed) = (b2.speed, b1.speed)
        b1.speed *= elasticity
        b2.speed *= elasticity
        
#        while distance < b1.ballRadius + b2.ballRadius:
#            print("still overlapping...")
#            b1.proposeX(update=True)
#            b1.proposeY(update=True)
#            b2.proposeX(update=True)
#            b2.proposeY(update=True)
#            dx = b1.x - b2.x
#            dy = b1.y - b2.y
#            distance = math.hypot(dx, dy)
#        
#        
#        print("resolved")
#        print(" ")
#        pygame.time.wait(1000)
        # check for collision, and if colliding still, update the position        
        angle = 0.5 * math.pi + tangent
        b1.x += math.sin(angle)
        b1.y -= math.cos(angle)
        b2.x -= math.sin(angle)
        b2.y += math.cos(angle)


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
    
    
def draw_grid(surface):
    global _tableSize, _tableEdges
    pocket_topleft_top = pygame.draw.rect(surface, (255,0,0), (0,0,50+_tableEdges,_tableEdges))
    pocket_topleft_left = pygame.draw.rect(surface, (255,0,0), (0,0,_tableEdges,50+_tableEdges))
    pocket_bottomright_bottom = pygame.draw.rect(surface, (255,0,0), (_tableSize[0]-50+_tableEdges,_tableSize[1]+_tableEdges,50+_tableEdges,_tableEdges))
    pocket_bottomright_right = pygame.draw.rect(surface, (255,0,0), (_tableSize[0]+_tableEdges,_tableSize[1]-50+_tableEdges,_tableEdges,50+_tableEdges))
    pocket_topright_top = pygame.draw.rect(surface, (255,0,0), (_tableSize[0]-50+_tableEdges,0,50+_tableEdges,_tableEdges))
    pocket_topright_right = pygame.draw.rect(surface, (255,0,0), (_tableSize[0]+_tableEdges,0,_tableEdges,50+_tableEdges))
    pocket_bottomleft_bottom = pygame.draw.rect(surface, (255,0,0), (0,_tableSize[1]+_tableEdges,50+_tableEdges,_tableEdges))
    pocket_bottomleft_left = pygame.draw.rect(surface, (255,0,0), (0,_tableSize[1]-50+_tableEdges,_tableEdges,50+_tableEdges))

    wall_top = pygame.draw.rect(surface, (0,0,0), (50+_tableEdges,0,_tableSize[0]-100,_tableEdges))
    wall_left = pygame.draw.rect(surface, (0,0,0), (0,50+_tableEdges,_tableEdges,_tableSize[1]-100))
    wall_bottom = pygame.draw.rect(surface, (0,0,0), (50+_tableEdges,_tableSize[1]+_tableEdges,_tableSize[0]-100,_tableEdges))
    wall_right = pygame.draw.rect(surface, (0,0,0), (_tableSize[0]+_tableEdges,50+_tableEdges,_tableEdges,_tableSize[1]-100))
    
    pockets = {'topleft': (pocket_topleft_top,pocket_topleft_left), 'topright': (pocket_topright_right,pocket_topright_top), 'bottomleft': (pocket_bottomleft_bottom, pocket_bottomleft_left), 'bottomright': (pocket_bottomright_right, pocket_bottomright_bottom)}
    walls = {'wall_top': wall_top, 'wall_left': wall_left, 'wall_bottom': wall_bottom, 'wall_right':wall_right}
    table = pygame.draw.rect(surface, (255,255,255), (_tableEdges,_tableEdges, _tableSize[0], _tableSize[1]))
    color = (0.8*255,0.8*255,0.8*255)
    xpnts = range(1, _tableSize[0], 100)
    ypnts = range(1, _tableSize[1], 100)
    for i in range(1,len(xpnts)):
        pygame.draw.line(surface, color, (xpnts[i]+_tableEdges,1+_tableEdges), (xpnts[i]+_tableEdges,_tableSize[1]+_tableEdges), 1)
    for i in range(1,len(ypnts)):
        pygame.draw.line(surface, color, (1+_tableEdges,ypnts[i]+_tableEdges), (_tableSize[0]+_tableEdges,ypnts[i]+_tableEdges), 1)
    return (table, pockets, walls)
    
    
    


pygame.init()

# Game variables
gravity = 0.25
ball_movement = 0


# Including music -- can play a song once or on a loop
#pygame.mixer.music.load('stressclock.mp3')
#pygame.mixer.music.play(-1) # indexes from 1, so zero means play once.
# to play infinitely, use -1, to play once is 0
# pygame.mixer.music.stop() -- stops current song and also erases whole queue



# window of desired size, a surface obj
screen = pygame.display.set_mode((_tableSize[0] + 2*_tableEdges,_tableSize[1] + 2*_tableEdges))

table_surface = pygame.Surface((_tableSize[0] + 2*_tableEdges,_tableSize[1] + 2*_tableEdges))

#table,pockets,walls = draw_grid(table_surface, tableSize,tableEdges)
table,pockets,walls = draw_grid(table_surface)
 
done = False
has_collided = False
xs = [50.]#,150.,250.]
ys = [50.]#,150.,250.]
speeds = [1.0/5.0] #[1.]#, 1., 1.]
angles = [math.radians(i) for i in [-25.]]#,180.+45.,180.]]
colors = [(0,128,255)] #(0,128,255)]#, (255,100,0), (100,255,0)]

# collect our balls:
balls = []
for i in range(0,len(xs)):
    balls.append(Ball(xs[i], ys[i], speeds[i], angles[i], i+1))

#ball_surface = pygame.Surface((_ballRadius*2,_ballRadius*2))
#rect = ball_surface.get_rect(center = (xs[0], ys[0]))
#ball = pygame.draw.circle(ball_surface, colors[0], (_ballRadius,_ballRadius),_ballRadius)

clock = pygame.time.Clock()

STARTMOTION = pygame.USEREVENT
pygame.time.set_timer(STARTMOTION, 10) #ms

started = False

try:
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
                    
            if event.type == STARTMOTION:
                started = True
    
    
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: ys[0] -= 3
        if pressed[pygame.K_DOWN]: ys[0] += 3
        if pressed[pygame.K_LEFT]: xs[0] -= 3
        if pressed[pygame.K_RIGHT]: xs[0] += 3
        
        if not all(i > 0 and i < _tableSize[0] for i in xs) or not all(i > 0 and i < _tableSize[1] for i in ys):
            effect = pygame.mixer.Sound('stresspulse.mp3')
            effect.play(0)
        
        #interactivity from if statements in the event queue
        if has_collided: 
            colors[0] = (255,0,0)
        else: 
            colors[0] = (0,128,255)
    
        # first, reset the screen before displaying things otherwise won't update right:
        screen.fill((0,0,0))
    #    draw_grid(screen, tableSize,tableEdges);
        screen.blit(table_surface, (0,0))
        
     
        for i in range(0, len(xs)):
            if started:
                balls[i].bounce(walls)
                if len(xs)>1:
                    for j in range(i+1, len(xs)):
                        collide(balls[i],balls[j])
                balls[i].updateX()
                balls[i].updateY()
    #            balls[i].checkCollision(walls)
            balls[i].render(screen)
    #    ball_surface.get_rect(center = (xs[0], ys[0]))
#        screen.blit(ball_surface, (xs[0]-_ballRadius, ys[0]-_ballRadius))
        
    #    ball = pygame.draw.circle(ball_surface, colors[0], (ballRadius,ballRadius),ballRadius)
                
        # pygame is double buffered -- has 2 
        # buffers. Whatever is the latest screen
        # needs to be displayed. So a load
        # buffer and a display buffer
        pygame.display.flip()
        
        # We first adjust the frame update rate to be reasonable
        clock.tick(120) # wait 1/60s before executing this loop, 60fps
except:
    pygame.quit()
    raise
    
pygame.quit()
#sys.exit()
    


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 08:39:41 2021

@author: ahamilos, developed from example from pymunk
"""

"""This example spawns (bouncing) balls randomly on a L-shape constructed of 
two segment shapes. Not interactive.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

# Python imports
import random
import sys
import os
import math
from typing import List

# Library imports
import pygame

# pymunk imports
import pymunk
import pymunk.pygame_util


# import params from Julia
_tableSize = [3*100, 3*100] 
_tableEdges = 20
_ballRadius = 23

xs = [50.,150.,250.]
ys = [50.,150.,250.]
jspeeds = [1.0/5.0, 1., 1.]
speeds = [i*1000. for i in jspeeds]
angles = [math.radians(i) for i in [-25.,180.+45.,180.]]


# generic functions
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


class BouncyBalls(object):
    """
    This class implements a simple scene in which there is a static platform (made up of a couple of lines)
    that don't move. Balls appear occasionally and drop onto the platform. They bounce around.
    """

    def __init__(self, xs, ys, speeds, angles) -> None:
        # Space
        self._space = pymunk.Space()
        self._space.gravity = (0.0, 0.0)#900.0) removing gravity for PBW

        # Physics
        # Time step
        self._dt = 1.0 / 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1
        

        # Balls that exist in the world
        self._balls: List[pymunk.Circle] = []

        # pygame
        pygame.init() 

        
        self.done = False
        self.has_collided = False
#        done = False
#        has_collided = False
        self.xs = [50.]#,150.,250.]
        self.ys = [50.]#,150.,250.]
        self.speeds = [1.0/5.0] #[1.]#, 1., 1.]
        self.angles = [math.radians(i) for i in [-25.]]#,180.+45.,180.]]
        self.colors = [(0,128,255, 255), (255,100,0, 255), (100,255,0, 255)]
        
#        # collect our balls:
#        self.balls = []
        self.balls_in_pocket = []
        for i in range(0,len(xs)):
            self._create_ball(x=xs[i], y=ys[i], speed=speeds[i], angle=angles[i], color=self.colors[i])
            self.balls_in_pocket.append(False)
#            balls.append(Ball(xs[i], ys[i], speeds[i], angles[i], i+1))
        
      
        
        self.STARTMOTION = pygame.USEREVENT
        pygame.time.set_timer(self.STARTMOTION, 10) #ms
        self.CLOCKTICK = pygame.USEREVENT+1
        pygame.time.set_timer(self.CLOCKTICK, 1) 
        self.timer_ms = 0
        
        self.started = False
        
        
        
        # window of desired size, a surface obj
        self._screen = pygame.display.set_mode((_tableSize[0] + 2*_tableEdges,_tableSize[1] + 2*_tableEdges))
        self.table_surface = pygame.Surface((_tableSize[0] + 2*_tableEdges,_tableSize[1] + 2*_tableEdges))
        #table,pockets,walls = draw_grid(table_surface, tableSize,tableEdges)
        self.table,self.pockets,self.walls = draw_grid(self.table_surface)
#        self._screen = pygame.display.set_mode((600, 600))
        self._clock = pygame.time.Clock()

        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Static barrier walls (lines) that the balls bounce off of
        self._add_static_scenery()



        # Execution control and time until the next ball spawns
        self._running = True
#        self._ticks_to_next_ball = 10

    def run(self) -> None:
        """
        The main loop of the game.
        :return: None
        """
        # Main loop
        try:
            while self._running:
                # pygame.event.get() clears the event 
                #queue. If don't call, the window's 
                #messages will pile up, game gets slow
                # EVENT PUMPING
                for event in pygame.event.get():
                    # pygame.QUIT called when you hit 
                    # x marker in corner
                    if event.type == pygame.QUIT:
                        self.done= True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            has_collided = not has_collided
                        elif event.key == pygame.K_ESCAPE:
                            done = True
                            
                    if event.type == self.STARTMOTION:
                        self.started = True
                    if event.type == self.CLOCKTICK: # count up the clock
                        #Timer
                        self.timer_ms += 1
#                        if self.timer_ms % 1000 == 0:
#                            print("Time: ", self.timer_ms/1000., "s")
                
                # Progress time forward
                for x in range(self._physics_steps_per_frame):
                    self._space.step(self._dt)
    
                self._process_events()
                self._update_balls()
#                self._clear_screen()
                self._draw_objects()
                pygame.display.flip()
                self._screen.blit(self.table_surface, (0,0))
                # Delay fixed time between frames
                self._clock.tick(50)
                pygame.display.set_caption("fps: " + str(self._clock.get_fps()))
                
                if self.done:
                    pygame.quit()
        except:
            pygame.quit()
            raise
        pygame.quit()

    def _add_static_scenery(self) -> None:
        """
        Create the static bodies.
        :return: None
        """
        static_body = self._space.static_body
        static_lines = [
            pymunk.Segment(static_body, (50+_tableEdges,_tableEdges),(_tableSize[1]-50+20,_tableEdges), 2.0),#top wall
            pymunk.Segment(static_body, (_tableEdges,50+_tableEdges),(_tableEdges,_tableSize[0]-50+20), 2.0),#left wall
            pymunk.Segment(static_body, (50+_tableEdges,_tableEdges+_tableSize[1]),(_tableSize[1]-50+20,_tableSize[1]+_tableEdges), 2.0), #bottom wall
            pymunk.Segment(static_body, (_tableEdges+_tableSize[0],50+_tableEdges),(_tableEdges+_tableSize[0],_tableSize[0]-50+20), 2.0),#left wall
        ]
        for line in static_lines:
            line.elasticity = 1#0.95
            line.friction = 0#0.9
            
        
        self._space.add(*static_lines)

    def _process_events(self) -> None:
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(self._screen, "bouncing_balls.png")

    def _update_balls(self) -> None:
        """
        Create/remove balls as necessary. Call once per frame only.
        :return: None
        """
#        self._ticks_to_next_ball -= 1
#        if self._ticks_to_next_ball <= 0:
#            self._create_ball()
#            self._ticks_to_next_ball = 100
        # Remove balls that fall below 100 vertically
#        balls_to_remove = [ball for ball in self._balls if ball.body.position.y > 500]
#        for ball in balls_to_remove:
#            self._space.remove(ball, ball.body)
#            self._balls.remove(ball)
        for i in range(0,len(self._balls)):
            ball = self._balls[i]
            if ball.body.position.x < _tableEdges or ball.body.position.y < _tableEdges or ball.body.position.x > _tableEdges*2+_tableSize[0] or ball.body.position.y > _tableEdges*2+_tableSize[1]:
                if self.balls_in_pocket[i] == False:
                    print("Ball ", i+1, "in the pocket at ", self.timer_ms/1000, "s!")
                    self.balls_in_pocket[i] = self.timer_ms/1000
                    
        
        
    def _create_ball(self, x=random.randint(115, 350), y=200, speed=0, angle=0, color=(255, 0, 0, 255)) -> None:
        """
        Create a ball.
        :return:
        """
        mass = 10
        radius = _ballRadius
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
#        x = random.randint(115, 350)
        body.position = x, y
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 1#0.95
        shape.friction = 0#0.9
        shape.color = color
        
        # calculate the impulse based on velocity and angle
        x_impulse = speed*math.cos(angle)
        y_impulse = -speed*math.sin(angle)
        
        body.apply_impulse_at_local_point((x_impulse,y_impulse)) # applies impulse of 10,000 to center of ball, 0
        
        self._space.add(body, shape)
        self._balls.append(shape)
        
        

    def _clear_screen(self) -> None:
        """
        Clears the screen.
        :return: None
        """
        self._screen.fill(pygame.Color("white"))

    def _draw_objects(self) -> None:
        """
        Draw the objects.
        :return: None
        """
        self._space.debug_draw(self._draw_options)
        
    


if __name__ == "__main__":
    game = BouncyBalls(xs, ys, speeds, angles)
    game.run()
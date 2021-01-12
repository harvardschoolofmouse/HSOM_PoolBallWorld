#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 08:39:41 2021

@author: ahamilos (ahamilos [at] g.harvard.edu)

pool_ball_world_physics_engine.py
"""

"""
Visual simulation of Pool Ball World Physics. Built from example from Pymunk
"""

__version__ = "1.0.0" #"$Id:$"
__docformat__ = "reStructuredText"

# Python imports
import random
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
angles = [math.radians(i) for i in [90.,180.+45.,180.]]
timelimit = 12000

collision_types = {
    "ball": 1,
    "wall": 2,
}



class PBW(object):
    """
    This class implements Pool Ball World simulations
    """

    def __init__(self, xs, ys, speeds, angles, timelimit=10000, verbose=True) -> None:
        self.verbose = verbose
        # Data
        self.xs = xs
        self.ys = ys
        self.speeds = speeds
        self.angles = angles
        self.colors = [(0,128,255, 255), (255,100,0, 255), (100,255,0, 255)]
       
        # Space
        self._space = pymunk.Space()
        self._space.gravity = (0.0, 0.0)#900.0) removing gravity for PBW
        pymunk.pygame_util.positive_y_is_up = True
        self.timelimit = timelimit

        # Physics
        # Time step
        self._dt = 1.0 / 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1
        
        # Balls that exist in the world
        self._balls: List[pymunk.Circle] = []

        # pygame
        pygame.init() 

        # collect our balls:
        self.balls_in_pocket = []
        for i in range(0,len(xs)):
            self._create_ball(x=xs[i], y=ys[i], speed=speeds[i], angle=angles[i], color=self.colors[i])
            self.balls_in_pocket.append(False)
        
        
        self.CLOCKTICK = pygame.USEREVENT+1
        pygame.time.set_timer(self.CLOCKTICK, 1) 
        self.timer_ms = 0
        
        self._clock = pygame.time.Clock()

        # Static barrier walls (lines) that the balls bounce off of
        self._add_static_scenery()

        # Execution control and time until the next ball spawns
        self._running = True
        
        # add deets to handle collision tracking
        # collision_times_ball_ball
        self.collision_times_ball_ball = {"1-2": [], "1-3": [], "2-3": []}
        
        def get_collision_time(arbiter, space, data):
            ball_shape_0 = arbiter.shapes[0]
            ball_shape_1 = arbiter.shapes[1]         
            if ball_shape_0.color[1] == self.colors[1][1]:
                if ball_shape_1.color[1] == self.colors[2][1]:
                    key = "1-2"
                else:
                    key = "1-3"
            elif ball_shape_0.color[1] == self.colors[2][1]:
                if ball_shape_1.color[1] == self.colors[1][1]:
                    key = "1-2"
                else:
                    key = "2-3"
            else:
                if ball_shape_1.color[1] == self.colors[2][1]:
                    key = "2-3"
                else:
                    key = "1-3"
                    
            self.collision_times_ball_ball[key].append(self.timer_ms/1000)
            if verbose:
                print("Collision ", key, " at: ", self.timer_ms/1000)
                
        h = self._space.add_collision_handler(collision_types["ball"], collision_types["ball"])
        h.separate = get_collision_time
        
        # collision_times_ball_wall
        self.collision_times_ball_wall = {"1-wall": [], "2-wall": [], "3-wall": []}
        def get_collision_time_walls(arbiter, space, data):
            ball = arbiter.shapes[0]        
            if ball.color[1] == self.colors[1][1]:
                key = "1-wall"
            elif ball.color[1] == self.colors[2][1]:
                key = "2-wall"
            else:
                key = "3-wall"
                    
            self.collision_times_ball_wall[key].append(self.timer_ms/1000)
            if verbose:
                print("Collision ", key, " at: ", self.timer_ms/1000)
                
        h = self._space.add_collision_handler(collision_types["ball"], collision_types["wall"])
        h.separate = get_collision_time_walls

    def run(self) -> None:
        """
        The main loop of the game.
        :return: None
        """
        # Main loop
        try:
            while self._running and self.timer_ms < self.timelimit:
                
                # Progress time forward
                for x in range(self._physics_steps_per_frame):
                    self._space.step(self._dt)
    
                self._process_events()
                self._update_balls()
                
#                # Delay fixed time between frames
                self._clock.tick(50)
                
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
            # add code to handle the collision
            line.collision_type = collision_types["wall"]
            
        self._space.add(*static_lines)

    def _process_events(self) -> None:
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        for event in pygame.event.get():
            if event.type == self.CLOCKTICK: # count up the clock
                #Timer
                self.timer_ms += 1
                
        if sum(self.balls_in_pocket) == len(self.balls_in_pocket):
            if self.verbose:
                print("All balls in pocket")
            self._running = False


    def _update_balls(self) -> None:
        """
        Check if ball in pocket, update once per frame.
        :return: None
        """
        for i in range(0,len(self._balls)):
            ball = self._balls[i]
            if ball.body.position.x < _tableEdges or ball.body.position.y < _tableEdges or ball.body.position.x > _tableEdges*2+_tableSize[0] or ball.body.position.y > _tableEdges*2+_tableSize[1]:
                if self.balls_in_pocket[i] == False:
                    if self.verbose:
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
        y_impulse = speed*math.sin(angle)
        
        body.apply_impulse_at_local_point((x_impulse,y_impulse)) # applies impulse of 10,000 to center of ball, 0
        
        # add code to handle the collision
        shape.collision_type = collision_types["ball"]
        
        
        self._space.add(body, shape)
        self._balls.append(shape)
        
        

    


if __name__ == "__main__":
    game = PBW(xs, ys, speeds, angles, timelimit, verbose=False)
    game.run()
    print(game.collision_times_ball_ball)
    print(game.collision_times_ball_wall)
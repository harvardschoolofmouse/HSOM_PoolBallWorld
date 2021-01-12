#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 08:39:41 2021

@author: ahamilos (ahamilos [at] g.harvard.edu)
"""

"""
Visual simulation of Pool Ball World Physics. Built from example from Pymunk
"""

__version__ = "$Id:$"
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


class PBW(object):
    """
    This class implements Pool Ball World simulations
    """

    def __init__(self, xs, ys, speeds, angles, timelimit=10000) -> None:
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

        
        self.done = False
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
        
        
        # add deets to handle collision tracking
        # collision_times_ball_ball
        self.collision_times_ball_ball = {"1-2": [], "1-3": [], "2-3": []}
        
        def get_collision_time(arbiter, space, data):
            ball_shape_0 = arbiter.shapes[0]
            ball_shape_1 = arbiter.shapes[1]         
            if ball_shape_0.color[1] == self.colors[1][1]:
#                ball_0_ix = 1
                if ball_shape_1.color[1] == self.colors[2][1]:
#                    ball_1_ix = 2
                    key = "1-2"
                else:
#                    ball_1_ix = 3
                    key = "1-3"
            elif ball_shape_0.color[1] == self.colors[2][1]:
#                ball_0_ix = 2
                if ball_shape_1.color[1] == self.colors[1][1]:
#                    ball_1_ix = 1
                    key = "1-2"
                else:
#                    ball_1_ix = 3
                    key = "2-3"
            else:
#                ball_0_ix = 3
                if ball_shape_1.color[1] == self.colors[2][1]:
#                    ball_1_ix = 2
                    key = "2-3"
                else:
#                    ball_1_ix = 1
                    key = "1-3"
                    
            self.collision_times_ball_ball[key].append(self.timer_ms/1000)
            print("Collision ", key, " at: ", self.timer_ms/1000)
                
        h = self._space.add_collision_handler(collision_types["ball"], collision_types["ball"])
        h.separate = get_collision_time
        
        # collision_times_ball_wall
        self.collision_times_ball_wall = {"1-wall": [], "2-wall": [], "3-wall": []}
        def get_collision_time_walls(arbiter, space, data):
            ball = arbiter.shapes[0]
#            wall = arbiter.shapes[1]         
            if ball.color[1] == self.colors[1][1]:
                key = "1-wall"
            elif ball.color[1] == self.colors[2][1]:
                key = "2-wall"
            else:
                key = "3-wall"
                    
            self.collision_times_ball_wall[key].append(self.timer_ms/1000)
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
#                self._clear_screen()
                self._draw_objects()
                pygame.display.flip()
                self._screen.blit(self.table_surface, (0,0))
                # Delay fixed time between frames
                self._clock.tick(50)
#                pygame.display.set_caption("time: " + str(self.timer_ms/1000))#str(self._clock.get_fps()))
                
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
            # add code to handle the collision
            line.collision_type = collision_types["wall"]
            
        self._space.add(*static_lines)

    def _process_events(self) -> None:
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        # pygame.event.get() clears the event 
        #queue. If don't call, the window's 
        #messages will pile up, game gets slow
        # EVENT PUMPING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            
            elif event.type == self.CLOCKTICK: # count up the clock
                #Timer
                self.timer_ms += 1
                if self.timer_ms % 1000 == 0:
                    pygame.display.set_caption("time: " + str(self.timer_ms/1000))
#                        if self.timer_ms % 1000 == 0:
#                            print("Time: ", self.timer_ms/1000., "s")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(self._screen, "PBWsnap.png")

    def _update_balls(self) -> None:
        """
        Check if ball in pocket, update once per frame.
        :return: None
        """
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
        y_impulse = speed*math.sin(angle)
        
        body.apply_impulse_at_local_point((x_impulse,y_impulse)) # applies impulse of 10,000 to center of ball, 0
        
        # add code to handle the collision
        shape.collision_type = collision_types["ball"]
        
        
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
    game = PBW(xs, ys, speeds, angles, timelimit)
    game.run()
    print(game.collision_times_ball_ball)
    print(game.collision_times_ball_wall)
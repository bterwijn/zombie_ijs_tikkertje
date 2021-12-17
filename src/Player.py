import random
import pygame

import Frame

class Player:
    line_width=1
    
    def __init__(self,pos):
        self.frame=Frame.Frame(pos,0)
        self.speed=pygame.Vector2(0,0)
        self.radius=20
        self.color=pygame.Color(random.randint(100,255),random.randint(100,255),random.randint(100,255))
        self.zombie=False
        self.score=0
        
    def get_frame(self):
        return self.frame

    def is_zombie(self):
        return self.zombie

    def set_zombie(self,zombie_flag):
        self.zombie=zombie_flag
    
    def do_actions(self,action_list):
        thrust_sum=0
        rotation_sum=0
        if len(action_list)>0:
            for a in action_list:
                thrust_sum+=a.thrust
                rotation_sum+=a.rotation
            thrust_sum/=len(action_list)
            rotation_sum/=len(action_list)
            if self.zombie:
                thrust_sum*=1.1
            self.frame.angle+=rotation_sum
            accel=pygame.Vector2(0,0)
            accel.from_polar((thrust_sum, self.frame.angle))
            self.speed+=accel
    
    def step(self):
        self.frame.pos+=self.speed
        self.speed*=0.975

    def is_in_collision_with_player(self,other,additional_radius=0):
        if self is other:
            return False
        square_distance=(self.frame.pos-other.frame.pos).length_squared()
        return square_distance<(self.radius+additional_radius+other.radius)**2
    
    def is_in_collision_with_polygon_line(self,polygon):
        dist,p1,p2=polygon.min_distance_line(self.frame.pos,self.radius)
        collision=not dist is None and dist<self.radius**2
        return (collision,p1,p2)

    def is_in_collision_with_polygon_corner(self,polygon):
        dist,p=polygon.min_distance_corner(self.frame.pos)
        collision=not dist is None and dist<self.radius**2
        return (collision,p)
        
    def draw(self,screen,viewport,name,name_textures,zombie_radius):
        center=viewport.tranform_vec(self.frame.pos)
        if self.zombie:
            pygame.draw.circle(screen, pygame.Color(255,0,0), center, viewport.transform(self.radius))
            pygame.draw.circle(screen, pygame.Color(255,0,0), center, viewport.transform(self.radius+zombie_radius),1)
        pygame.draw.circle(screen, self.color, viewport.tranform_vec(self.frame.pos), viewport.transform(self.radius), self.line_width)
        line=pygame.Vector2(0,0)
        line.from_polar((self.radius*2, self.frame.angle))
        pygame.draw.line(screen, self.color, center, viewport.tranform_vec(self.frame.pos+line), self.line_width )
        if not name in name_textures:
            font = pygame.font.Font(pygame.font.get_default_font(), 24)
            name_textures[name]=font.render(name,True,self.color)
        name_texture=name_textures[name]
        name_size=pygame.Vector2(name_texture.get_size())
        pos=viewport.tranform_vec(self.frame.pos)-name_size/2
        pos.y+=self.radius
        screen.blit(name_texture, pos)

import random
import pygame

class Player:
    line_width=6
    
    def __init__(self,world_size):
        self.radius=random.randint(30,80)
        self.color=pygame.Color(random.randint(100,255),random.randint(100,255),random.randint(100,255))
        self.pos=world_size/2
        self.speed=pygame.Vector2(0,0)
        
    def update(self,action_list,world_size):
        for a in action_list:
            self.speed+=a.accel
        self.pos+=self.speed
        if self.pos[0]<0 or self.pos[0]>world_size[0]:
            self.pos-=self.speed
            self.speed[0]=-self.speed[0]
        if self.pos[1]<0 or self.pos[1]>world_size[1]:
            self.pos-=self.speed
            self.speed[1]=-self.speed[1]
        self.speed[1]+=0.8
        self.speed*=0.995

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius, self.line_width)

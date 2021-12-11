import pygame
import math
import random
import time

import Player
import Polygon
import Viewport
import Frame
import Circles

class Game_State:

    def __init__(self):
        self.players={}
        self.polygons=[]
        self.circles=Circles.Circles.random(20,pygame.Vector2(-2000,-2000),pygame.Vector2(2000,2000),100,1000,5,60)
        self.add_polygons()
        self.zombie_radius=0
        self.zombie_radius_max=200
        self.no_zombie_time=time.time()
         
    def add_polygons(self):
        p=Polygon.Polygon([pygame.Vector2(-1500,  -900),
                           pygame.Vector2(-1300,  2200),
                           pygame.Vector2( 1700,  2100),
                           pygame.Vector2( 2000,  -700),
                           pygame.Vector2( 1100, -1500)])
        self.polygons.append(p)
        
        p=Polygon.Polygon([pygame.Vector2(80,80),pygame.Vector2(300,10),pygame.Vector2(100,300)])
        self.polygons.append(p)
        p=Polygon.Polygon([pygame.Vector2(400,300),pygame.Vector2(500,360),pygame.Vector2(450,500)])
        self.polygons.append(p)
        p=Polygon.Polygon([pygame.Vector2(645, -68),
                           pygame.Vector2(939, -1079),
                           pygame.Vector2(1414, -437)])
        self.polygons.append(p)
        p=Polygon.Polygon([pygame.Vector2(29, 822),
                           pygame.Vector2(-233, 1812),
                           pygame.Vector2(-930, 1847)])
        self.polygons.append(p)
        p=Polygon.Polygon([pygame.Vector2(1352, 1683),
                           pygame.Vector2(710, 1801),
                           pygame.Vector2(790, 672),
                           pygame.Vector2(1559, 339)])
        self.polygons.append(p)
        p=Polygon.Polygon([pygame.Vector2(-335, 42),
                           pygame.Vector2(228, -438),
                           pygame.Vector2(89, -817),
                           pygame.Vector2(-903, -573)])
        self.polygons.append(p)
        p=Polygon.Polygon([pygame.Vector2(338, -968),
                           pygame.Vector2(517, -733),
                           pygame.Vector2(626, -1095)])
        self.polygons.append(p)
        p=Polygon.Polygon([pygame.Vector2(-1081, -298),
                           pygame.Vector2(-814, -72),
                           pygame.Vector2(-1095, 224)])
        self.polygons.append(p)
        p=Polygon.Polygon([pygame.Vector2(187, 1864),
                           pygame.Vector2(443, 1869),
                           pygame.Vector2(388, 1247)])
        self.polygons.append(p)
        p=Polygon.Polygon([pygame.Vector2(1207, 71),
                           pygame.Vector2(1143, -13),
                           pygame.Vector2(1548, -290),
                           pygame.Vector2(1661, -109)])
        self.polygons.append(p)
        p=Polygon.Polygon([pygame.Vector2(880, 171),
                           pygame.Vector2(721, 275),
                           pygame.Vector2(931, 258)])
        self.polygons.append(p)
        p=Polygon.Polygon([pygame.Vector2(-339, 318),
                           pygame.Vector2(-223, 225),
                           pygame.Vector2(-144, 416)])
        self.polygons.append(p)
        p=Polygon.Polygon([pygame.Vector2(-749, 370),
                           pygame.Vector2(-434, 694),
                           pygame.Vector2(-977, 1097),
                           pygame.Vector2(-1022, 684)])
        self.polygons.append(p)
        p=Polygon.Polygon([pygame.Vector2(-1225, 1715),
                           pygame.Vector2(-1232, 1474),
                           pygame.Vector2(-1061, 1531)])
        self.polygons.append(p)

    def get_player(self,name):
        return self.players.get(name,None)
        
    def update(self,elapsed_time,actions):
        for name,player in self.players.items():
            if name in actions.get_actions():
                player.do_actions(actions.get_actions()[name])
                del actions.get_actions()[name]
            player.step()
            self.collision_handling(player)
        for name,action_list in actions.get_actions().items():
            if name not in self.players:
                print("new player:",name)
                self.players[name]=Player.Player(pygame.Vector2(0,100*len(self.players)))
        self.set_zombie()

    def collision_handling(self,player):
        for other in self.players.values():
            if player.is_in_collision_with_player(other,self.zombie_radius):
                if player.is_zombie() and not other.is_zombie():
                    other.set_zombie(True)
                    other.score+=1+self.zombie_radius
                if other.is_zombie() and not player.is_zombie():
                    player.set_zombie(True)
                    player.score+=1+self.zombie_radius 
            if player.is_in_collision_with_player(other):
                player.frame.pos-=player.speed
                temp=player.speed
                player.speed=other.speed
                other.speed=temp
        for polygon in self.polygons:
            collision,p1,p2=player.is_in_collision_with_polygon_line(polygon)
            if collision:
                player.frame.pos-=player.speed
                player.speed=Polygon.Polygon.bounce_line(p1,p2,player.speed)
                break
        if not collision:
            for polygon in self.polygons:
                collision,p=player.is_in_collision_with_polygon_corner(polygon)
                if collision:
                    player.frame.pos-=player.speed
                    player.speed=Polygon.Polygon.bounce_corner(p,player.frame.pos,player.speed)
                    break
        
    def get_viewport(self,screen,player,frame_averager):
        world_frame=frame_averager.update(player.get_frame(),0.05)
        screen_size=pygame.Vector2(screen.get_size())
        screen_y_center=3*screen_size[1]/4
        screen_frame=Frame.Frame(pygame.Vector2(screen_size[0]/2,screen_y_center),90)
        scale=self.get_scale(world_frame,screen_y_center*0.96)
        return Viewport.Viewport(world_frame,screen_frame,scale)

    def max_player_distance(self,world_frame):
        max_distance=1
        for n,p in self.players.items():
            distance=(p.frame.pos-world_frame.pos).length_squared()
            if distance>max_distance:
                max_distance=distance
        return math.sqrt(max_distance)

    def get_scale(self,world_frame,screen_y_center):
        max_player_distance=self.max_player_distance(world_frame)
        scale=max_player_distance/screen_y_center
        if scale<1.5:
            scale=1.5
        if scale>4:
            scale=4
        return scale
        
    def draw(self,screen,viewport,player,name_textures,score_texture):
        screen.fill((0,0,0))
        self.circles.draw(screen,viewport)
        for polygon in self.polygons:
            polygon.draw(screen,viewport)
        for name,player in self.players.items():
            player.draw(screen,viewport,name,name_textures,self.zombie_radius)
        self.draw_score(screen,score_texture)
        pygame.display.flip()

    def draw_score(self,screen,score_texture):
        score=self.get_score()
        if not score in score_texture:
            score_texture.clear()
            font = pygame.font.Font(pygame.font.get_default_font(), 24)
            scores=score.split('\n')
            textures=[]
            for s in scores:
                textures.append(font.render(s,True,pygame.Color(255,255,255)))
            score_texture[score]=textures
        textures=score_texture[score]
        y=0
        for s in textures:
            screen.blit(s,(0,y))
            #print(s.get_size(), type(s.get_size()))
            y+=s.get_size()[1]
        
    def zombie_count(self):
        count=0
        for n,p in self.players.items():
            if p.is_zombie():
               count+=1
        return count

    def set_zombie(self):
        if len(self.players)>0:
            if self.zombie_count()==0 and time.time()-self.no_zombie_time>2:
                name=random.sample(self.players.keys(),1)[0]
                self.players[name].set_zombie(True)
                self.zombie_radius=0
            if self.zombie_count()==len(self.players):            
                for p in self.players.values():
                    p.set_zombie(False)
                self.no_zombie_time=time.time()
            self.zombie_radius+=0.005
            if self.zombie_radius>self.zombie_radius_max:
                self.zombie_radius=self.zombie_radius_max

    def get_score(self):
        score=""
        names=list(self.players.keys())
        names.sort()
        for n in names:
            p=self.players[n]
            score+=f"{n}: {round(p.score)}\n"
        return score

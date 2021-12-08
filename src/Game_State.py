import pygame

import Player
import Polygon
import Viewport
import Frame
import Circles

class Game_State:

    def __init__(self):
        self.players={}
        self.polygons=[]
        self.circles=Circles.Circles.random(20,pygame.Vector2(-2000,-2000),pygame.Vector2(2000,2000),100,1000,5,40)
        self.add_polygons()
        
    def add_polygons(self):
        p=Polygon.Polygon([pygame.Vector2(-1300,  -800),
                           pygame.Vector2(-1000,  2100),
                           pygame.Vector2( 1500,  1900),
                           pygame.Vector2( 1900,  -300),
                           pygame.Vector2(  800, -1300)])
        self.polygons.append(p)
        p=Polygon.Polygon([pygame.Vector2(80,80),pygame.Vector2(300,10),pygame.Vector2(100,300)])
        self.polygons.append(p)
        p=Polygon.Polygon([pygame.Vector2(400,300),pygame.Vector2(500,360),pygame.Vector2(450,500)])
        self.polygons.append(p)

    def get_player(self,name):
        return self.players.get(name,None)
        
    def update(self,elapsed_time,actions):
        for name,action_list in actions.get_actions().items():
            if name not in self.players:
                print("new player:",name)
                self.players[name]=Player.Player(pygame.Vector2(0,0))
            player=self.players[name]
            player.update(action_list)
            for other in self.players.values():
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
                    
    def draw(self,screen,name,frame_averager,name_textures):
        viewport=self.get_viewport(screen,name,frame_averager)
        screen.fill((0,0,0))
        self.circles.draw(screen,viewport)
        for polygon in self.polygons:
            polygon.draw(screen,viewport)
        for name,player in self.players.items():
            player.draw(screen,viewport,name,name_textures)
        pygame.display.flip()
        
    def get_viewport(self,screen,name,frame_averager):
        player=self.get_player(name)
        if player is None:
            world_frame=Frame.Frame.zero()
        else:
            world_frame=frame_averager.update(player.get_frame(),0.05)
        screen_size=pygame.Vector2(screen.get_size())
        screen_frame=Frame.Frame(pygame.Vector2(screen_size[0]/2,3*screen_size[1]/4),90)
        return Viewport.Viewport(world_frame,screen_frame,2)

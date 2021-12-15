import sys
import zmq
import time

import pygame
from pygame.locals import *

import Action
import Game_State
import Frame_Averager

def main():
    if len(sys.argv)>1:
        game_client=Game_Client(*sys.argv[1:])
        game_client.run()
    else:
        print("usage: ",sys.argv[0],"<name> [port] [host] ")

class Game_Client:
    game_fps=60
    
    def __init__(self,name,port="2222",host="127.0.0.1"):
        self.name=name
        context = zmq.Context()
        print(f"Connecting as '{name}' to server {host} on port {port}")
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://"+host+":"+port)
        
    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600), RESIZABLE)
        frame_averager=Frame_Averager.Frame_Averager()
        name_textures={}
        score_texture={}
        game_state=None
        viewport=None
        clock = pygame.time.Clock()
        self.running = True        
        while self.running:
            self.socket.send_pyobj(self.get_action(viewport))  # send action
            if game_state is not None:
                player=game_state.get_player(self.name)
                if not player is None:
                    viewport=game_state.get_viewport(screen,player,frame_averager)
                    game_state.draw(screen,viewport,player,name_textures,score_texture)  # draw game state
            clock.tick(self.game_fps)                                                    # sleep to limit frame rate
            game_state = self.socket.recv_pyobj()                                        # receive game state
        pygame.quit()
        
    def get_action(self,viewport):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not viewport is None:
                    p=pygame.Vector2(event.pos)
                    p=viewport.reverse_tranform_vec(p)
                    print(f"pygame.Vector2({round(p.x)}, {round(p.y)}),")
            if event.type == pygame.MOUSEBUTTONUP:
                pass
        keys=pygame.key.get_pressed()
        t=0.4
        r=4.3
        thrust= -t if keys[pygame.K_DOWN] else 0 + +t if keys[pygame.K_UP]    else 0
        rotation= -r if keys[pygame.K_LEFT] else 0 + +r if keys[pygame.K_RIGHT] else 0
        return Action.Action(self.name,thrust,rotation)
            
if __name__ == "__main__":
    main()
    

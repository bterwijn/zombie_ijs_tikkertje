import sys
import zmq
import time

import pygame
from pygame.locals import *

import Action
import Game_State

def main():
    if len(sys.argv)>1:
        game_client=Game_Client(*sys.argv[1:])
        game_client.run()
    else:
        print("usage: ",sys.argv[0],"<name> [port] [host] ")

class Game_Client:
    game_fps=100
    
    def __init__(self,name,port="2222",host="127.0.0.1"):
        self.name=name
        self.frame_history=[]
        context = zmq.Context()
        print("Connecting as '",name,"' to server",host,"on port",port)
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://"+host+":"+port)
        print("Connected")
        
    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600), RESIZABLE)
        game_state=None
        clock = pygame.time.Clock()
        self.running = True        
        while self.running:
            self.socket.send_pyobj(self.get_action())  # send action
            if game_state is not None:
                frame_history=self.update_frame_history(game_state,self.name)
                game_state.draw(screen,frame_history)      # draw game state
            clock.tick(self.game_fps)                      # sleep to limit frame rate
            game_state = self.socket.recv_pyobj()          # receive game state
        pygame.quit()

    def update_frame_history(self,game_state,name):
        player=game_state.get_player(name)
        if player is not None:
            self.frame_history.append(player.get_frame())
            if len(self.frame_history)>12:
                self.frame_history.pop(0)
        return self.frame_history
        
    def get_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event)
            if event.type == pygame.MOUSEBUTTONUP:
                print(event)
        keys=pygame.key.get_pressed()
        t=0.4
        r=4
        thrust= -t if keys[pygame.K_DOWN] else 0 + +t if keys[pygame.K_UP]    else 0
        rotation= -r if keys[pygame.K_LEFT] else 0 + +r if keys[pygame.K_RIGHT] else 0
        return Action.Action(self.name,thrust,rotation)
            
if __name__ == "__main__":
    main()
    

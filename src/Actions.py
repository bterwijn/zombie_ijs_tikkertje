
class Actions:

    def __init__(self):
        self.actions={}

    def add_action(self,action):
        player_actions=self.actions.get(action.name,[])
        player_actions.append(action)
        self.actions[action.name]=player_actions

    def clear(self):
        self.actions.clear()
            
    def get_actions(self):
        return self.actions

    



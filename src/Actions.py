
class Actions:

    def __init__(self):
        self.actions={}

    def add_action(self,action):
        if not action.name in self.actions:
            self.actions[action.name]=[]
        self.actions[action.name].append(action)

    def clear(self):
        self.actions.clear()
            
    def get_actions(self):
        return self.actions

    



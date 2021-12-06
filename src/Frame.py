
class Frame:

    def __init__(self,vector,angle):
        self.vector=vector
        self.angle=angle

    def __repr__(self):
        return f"{self.vector}:{self.angle}"

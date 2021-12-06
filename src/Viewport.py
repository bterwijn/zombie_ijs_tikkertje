
class Viewport:

    def __init__(self,world_frame,view_frame,zoom):
        self.world_frame=world_frame
        self.view_frame=view_frame
        self.zoom=zoom

    def transform(self,value):
        return value/self.zoom
        
    def tranform_vec(self,v):
        v=v-self.world_frame.vector
        v/=self.zoom
        r,phi=v.as_polar()
        phi-=self.world_frame.angle+self.view_frame.angle
        v.from_polar((r,phi))
        v+=self.view_frame.vector
        return v

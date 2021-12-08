import pygame

def main():
    p1=pygame.Vector2(3,5)
    p2=pygame.Vector2(0,4)
    pos=pygame.Vector2(2,3)
    print(Polygon.distance(p1,p2+p1,pos+p1))
    p=Polygon([pygame.Vector2(0,0),pygame.Vector2(100,0),pygame.Vector2(0,100)])
    pos=pygame.Vector2(400,10)
    print(p.min_distance(pos))
    p1=pygame.Vector2(0,0)
    p2=pygame.Vector2(1,0)
    speed=pygame.Vector2(1,1)
    print(Polygon.bounce(p1,p2,speed))

class Polygon:
    color=pygame.Color(255,255,255)
    
    def __init__(self,points=[]):
        self.points=points

    def add_point(self,point):
        self.points.append(point)

    def draw(self,screen,viewport):
        for i in range(-1,len(self.points)-1):
            p1=self.points[i]
            p2=self.points[i+1]
            pygame.draw.line(screen, Polygon.color, viewport.tranform_vec(p1), viewport.tranform_vec(p2))

    def min_distance(self,pos):
        min_dist=None
        mp1=None
        mp2=None
        for i in range(-1,len(self.points)-1):
            p1=self.points[i]
            p2=self.points[i+1]
            dist=Polygon.distance(p1,p2,pos)
            if not dist is None:
                if min_dist is None or dist<min_dist:
                    min_dist=dist
                    mp1=p1
                    mp2=p2
        return (min_dist,mp1,mp2)

    def distance(p1,p2,pos):
        p2=p2-p1
        length=p2.length()
        p2/=length
        pos=pos-p1
        proj=p2.dot(pos)
        if proj>0 and proj<length:
            return (proj*p2-pos).length()
        return None

    def bounce(p1,p2,speed):
        p2=p2-p1
        length=p2.length()
        p2/=length
        proj=p2.dot(speed)*p2
        diff=proj-speed
        return speed+2*diff

if __name__ == "__main__":
    main()

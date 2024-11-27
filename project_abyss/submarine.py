from settings import *

class Submarine:
    def __init__(self, pos, image):
        self.pos = pg.Vector2(pos)
        self.size = (320, 320)
        self.image = pg.transform.scale(image, self.size)
    
    def draw(self, window, focus_pos):
        rect = pg.Rect((0, 0), self.size)
        rect.center = self.pos - focus_pos
        window.blit(self.image, rect)
    
    def go_to_waypoint(self, waypoint):
        self.pos.x = waypoint.x
        self.pos.y = waypoint.y
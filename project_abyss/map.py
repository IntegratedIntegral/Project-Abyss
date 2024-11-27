from settings import *

class Map:
    def __init__(self):
        self.scale = 0.005
        self.focus_pos = pg.Vector2()

        self.surf = pg.surface.Surface((320, 320))
        self.pos = pg.Vector2(10, 200)

        self.waypoint = pg.Vector2(-1)
    
    def update(self, window, chunks, lmb_pressed, rmb_pressed, submarine):
        self.draw(window, chunks, submarine)
        self.pan(lmb_pressed)
        self.set_waypoint(rmb_pressed)
    
    def draw_border(self):
        corners = [
            (0, 0),
            (self.surf.size[0] - 1, 0),
            (self.surf.size[0] - 1, self.surf.size[1] - 1),
            (0, self.surf.size[1] - 1)
        ]
        colour = (32, 32, 32)
        pg.draw.line(self.surf, colour, corners[0], corners[1])
        pg.draw.line(self.surf, colour, corners[1], corners[2])
        pg.draw.line(self.surf, colour, corners[2], corners[3])
        pg.draw.line(self.surf, colour, corners[3], corners[0])
    
    def draw_chunk(self, chunk):
        size = self.scale * CHUNK_SIZE
        rect = pg.Rect(self.scale * chunk.pos - self.focus_pos, (size, size))
        pg.draw.rect(self.surf, (176, 162, 127), rect)
    
    def draw_point(self, pos, colour):
        rect = pg.Rect((0, 0), (4, 4))
        rect.center = self.scale * pos - self.focus_pos
        pg.draw.rect(self.surf, colour, rect)
    
    def draw_layers(self):
        for i in range(len(LAYER_DEPTH_VALS)):
            depth = LAYER_DEPTH_VALS[i]
            rect = pg.Rect((0 - self.focus_pos.x, self.scale * depth - self.focus_pos.y), (WORLD_WIDTH * self.scale, 0))
            if i < len(LAYER_DEPTH_VALS) - 1:
                rect.height = (LAYER_DEPTH_VALS[i + 1] - depth) * self.scale
            else:
                rect.height = (WORLD_HEIGHT - depth) * self.scale
            
            colour = LAYER_BG_COLOURS[i]
            pg.draw.rect(self.surf, colour, rect)

    def draw(self, window, chunks, submarine):
        self.surf.fill((0, 0, 0))
        self.draw_layers()

        self.draw_border()

        #draw chunks
        for chunk in chunks:
            self.draw_chunk(chunk)
        
        #draw submarine on map
        self.draw_point(submarine.pos, (255, 255, 0))

        #draw waypoint on map
        self.draw_point(self.waypoint, (0, 255, 0))
        
        window.blit(self.surf, self.pos)
    
    def pan(self, lmb_pressed):
        rel = pg.Vector2(pg.mouse.get_rel())
        if lmb_pressed:
            mouse_pos = pg.Vector2(pg.mouse.get_pos())
            rel_mouse_pos = mouse_pos - self.pos
            if rel_mouse_pos.x >= 0 and rel_mouse_pos.x <= self.surf.size[0] and rel_mouse_pos.y >= 0 and rel_mouse_pos.y <= self.surf.size[1]:
                self.focus_pos -= rel
                focus_pos_max_x = WORLD_WIDTH * self.scale - self.surf.size[0]
                focus_pos_max_y = WORLD_HEIGHT * self.scale - self.surf.size[1]
                if self.focus_pos.x < 0:
                    self.focus_pos.x = 0
                if self.focus_pos.x > focus_pos_max_x:
                    self.focus_pos.x = focus_pos_max_x
                if self.focus_pos.y < 0:
                    self.focus_pos.y = 0
                if self.focus_pos.y > focus_pos_max_y:
                    self.focus_pos.y = focus_pos_max_y
    
    def set_waypoint(self, rmb_pressed):
        if rmb_pressed:
            mouse_pos = pg.Vector2(pg.mouse.get_pos())
            rel_mouse_pos = mouse_pos - self.pos
            if rel_mouse_pos.x >= 0 and rel_mouse_pos.x <= self.surf.size[0] and rel_mouse_pos.y >= 0 and rel_mouse_pos.y <= self.surf.size[1]:
                self.waypoint = (rel_mouse_pos + self.focus_pos) / self.scale
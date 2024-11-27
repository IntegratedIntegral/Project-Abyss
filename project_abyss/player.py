from settings import *
from journal import Journal

class Player:
    def __init__(self, pos, image, tank_image):
        self.pos = pg.Vector2(pos)
        self.rect = pg.Rect((0, 0), PLAYER_DIMENSIONS)
        self.old_rect = self.rect.copy()
        self.dir_vec = pg.Vector2(1.0, 0.0)
        self.speed = 0.09
        self.is_moving = False

        self.template_image = image
        self.template_reverse_image = pg.transform.flip(image, True, False)
        self.image = image

        self.tank_image = tank_image

        self.boarded = False #whether the player has boarded the submarine or not

        self.oxygen = MAX_OXYGEN

        self.journal = Journal()
        self.journal_open = False
    
    def update(self, window, focus_pos, tiles, submarine, waypoint, images, lmb_pressed, delta_t):
        self.rect.center = self.pos #update position of rect
        self.old_rect = self.rect.copy()
        self.rect.size = PLAYER_DIMENSIONS
        
        self.peform_actions(focus_pos, tiles, submarine, waypoint, delta_t)
        if not self.boarded:
            self.draw(window, focus_pos)
            self.oxygen -= delta_t
        
        if self.journal_open:
            self.journal.update(window, images, lmb_pressed)
        
        self.draw_oxygen_bar(window)
    
    def peform_actions(self, focus_pos, tiles, submarine, waypoint, delta_t):
        key_state_pressed = pg.key.get_pressed()
        self.is_moving = False
        if key_state_pressed[pg.K_w]:
            #swim, but only when outside the submarine
            if not self.boarded:
                self.get_dir(focus_pos)
                self.swim(delta_t)
                self.is_moving = True
        
        key_state_just_pressed = pg.key.get_just_pressed()
        if key_state_just_pressed[pg.K_c]:
            #board/leave submarine
            if self.boarded:
                self.boarded = False
            else:
                self.board(submarine)
        if key_state_just_pressed[pg.K_RETURN]:
            #go to waypoint
            if self.boarded:
                self.go_to_waypoint(waypoint, submarine)
        if key_state_just_pressed[pg.K_TAB]:
            #open/close journal
            self.journal_open = not self.journal_open
        
        if not self.boarded:
            self.collide(tiles)
    
    def swim(self, delta_t):
        self.pos += self.speed * self.dir_vec * delta_t
        self.rect.center = self.pos #update position of rect
    
    def get_dir(self, focus_pos):
        mouse_pos = pg.Vector2(pg.mouse.get_pos())
        rel_mouse_pos = mouse_pos - self.pos + focus_pos #mouse position relative to player position on screen
        if rel_mouse_pos:
            self.dir_vec = rel_mouse_pos.normalize()
        else:
            self.dir_vec = pg.Vector2(1.0, 0.0)
        
        if self.dir_vec.x > 0:
            self.image = self.template_image
        else:
            self.image = self.template_reverse_image
    
    def draw(self, window, focus_pos):
        rect = pg.Rect((0, 0), self.rect.size)
        rect.center = self.pos - focus_pos
        window.blit(self.image, rect)
    
    def draw_oxygen_bar(self, window):
        bottom = WINDOW_HEIGHT - 10
        rect = pg.Rect((5, 0), TANK_DIMENSIONS)
        rect.bottom = bottom
        window.blit(self.tank_image, rect)
        
        height = self.oxygen / MAX_OXYGEN * OXYGEN_BAR_DIMENSIONS[1]
        oxygen_rect = pg.Rect((15, 0), (OXYGEN_BAR_DIMENSIONS[0], height))
        oxygen_rect.bottom = bottom
        pg.draw.rect(window, (201, 201, 201), oxygen_rect)

    def collide(self, tiles):
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.rect.left <= tile.right and self.old_rect.left >= tile.right:
                    self.rect.left = tile.right
                if self.rect.right >= tile.left and self.old_rect.right <= tile.left:
                    self.rect.right = tile.left
                if self.rect.top <= tile.bottom and self.old_rect.top >= tile.bottom:
                    self.rect.top = tile.bottom
                if self.rect.bottom >= tile.top and self.old_rect.bottom <= tile.top:
                    self.rect.bottom = tile.top
                self.pos = pg.Vector2(self.rect.center)
    
    def board(self, submarine):
        if (submarine.pos - self.pos).magnitude_squared() < BOARDING_DIST * BOARDING_DIST:
            self.boarded = True
            self.pos.x = submarine.pos.x
            self.pos.y = submarine.pos.y
            self.oxygen = MAX_OXYGEN
    
    def go_to_waypoint(self, waypoint, submarine):
        submarine.go_to_waypoint(waypoint)
        self.pos.x = submarine.pos.x
        self.pos.y = submarine.pos.y
    
    def reset(self):
        self.pos = pg.Vector2(PLAYER_STARTING_POS)
        self.oxygen = MAX_OXYGEN
        self.journal.reset()
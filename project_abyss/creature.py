from settings import *

class Creature:
    def __init__(self, pos, size, type, images):
        self.pos = pg.Vector2(pos)
        self.size = pg.Vector2(size)
        self.type = type
        self.image = images[type["image_id"]]
        self.rect = pg.FRect((0, 0), size)
        self.rect.center = self.pos
    
    def draw(self, window, focus_pos):
        rect = pg.Rect((0, 0), self.size)
        rect.center = self.pos - focus_pos
        window.blit(self.image, rect)
    
    def add_to_journal(self, focus_pos, player, lmb_pressed):
        mouse_pos = pg.Vector2(pg.mouse.get_pos())
        rel_mouse_pos = mouse_pos - self.pos + focus_pos
        #if player clicks on creature while it is within the documenting distance and if the creature has not been documented before then it will get added to the journal
        if lmb_pressed and rel_mouse_pos.magnitude_squared() < 40 * 40 and (self.pos - player.pos).magnitude_squared() < DOCUMENT_DIST * DOCUMENT_DIST and not self.type in player.journal.species:
            player.journal.add_species(self.type)

#creatures that swim, such as fish, jelly fish and sea turtles
class SwimmingCreature(Creature):
    def __init__(self, pos, type, images):
        super().__init__(pos, (type["size"]["x"], type["size"]["y"]), type, images)
        self.template_image = pg.transform.scale(self.image, self.size)
        self.dir_vec = pg.Vector2()
        self.speed = type["speed"]
        self.spook_speed = type["spook_speed"]
        self.cruising_time = type["cruising_time"]
        self.cruise_timer = 0 #a timer for how long the creature will be cruising at a constant velocity before turning
        self.turn_time = type["turn_time"]
        self.turn_timer = self.turn_time
        self.spooked = False
        self.just_fled = False
        self.set_dir_change()

    def set_cruise_timer(self):
        self.cruise_timer = random.randint(self.cruising_time // 2, self.cruising_time // 2 * 3)
    
    def set_dir_change(self):
        new_angle = random.random() * 2 * math.pi
        new_dir = pg.Vector2(math.cos(new_angle), math.sin(new_angle))
        self.dir_change = new_dir - self.dir_vec
    
    def update(self, window, focus_pos, player, lmb_pressed, delta_t):
        self.draw(window, focus_pos)
        self.swim(delta_t)
        self.update_timers(delta_t)
        self.add_to_journal(focus_pos, player, lmb_pressed)
    
    def swim(self, delta_t):
        if self.spooked: self.pos += self.spook_speed * self.dir_vec * delta_t
        else: self.pos += self.speed * self.dir_vec * delta_t
        
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > WORLD_WIDTH:
            self.pos.x = WORLD_WIDTH
        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y > WORLD_HEIGHT:
            self.pos.y = WORLD_HEIGHT
    
    def update_timers(self, delta_t):
        if self.cruise_timer > 0:
            self.cruise_timer -= delta_t
            self.just_fled = False
        elif self.turn_timer > 0:
            self.turn_timer -= delta_t
            self.turn(delta_t)
            if not self.just_fled: self.spooked = False
        else:
            self.dir_vec.normalize()
            self.set_cruise_timer()
            self.turn_timer = self.turn_time
            self.set_dir_change()
    
    def turn(self, delta_t):
        self.dir_vec += self.dir_change * delta_t / self.turn_time
        if self.dir_vec.x < 0:
            self.image = pg.transform.flip(self.template_image, True, False) #flip the image if the creature is swimming left
        else:
            self.image = self.template_image
    
    def flee(self, player):
        new_dir = (self.pos - player.pos).normalize()
        self.dir_change = new_dir - self.dir_vec
        self.cruise_timer = 0
        self.spooked = True
        self.just_fled = True

#creatures that live on solid surfaces, such as sea anemones, barnacles and sea grass
class GroundCreature(Creature):
    def __init__(self, chunk, type, images):
        size = (type["size"]["x"], type["size"]["y"])
        self.tile, self.orientation = self.get_tile(chunk)

        super().__init__(self.get_pos(size), size if self.orientation % 2 == 0 else size[::-1], type, images)
        
        self.rotate_image()
    
    def update(self, window, focus_pos, player, lmb_pressed):
        self.draw(window, focus_pos)
        self.add_to_journal(focus_pos, player, lmb_pressed)
    
    def get_tile(self, chunk):
        completely_obstructed = True
        #does some logic to find a collidable tile that is adjacent to open space. If a collidable tile is completely obstructed by other collidable tiles, it will try again with a different one
        while completely_obstructed:
            ran_id = random.randint(0, len(chunk.collidable_ids) - 1)
            tile_id = chunk.collidable_ids[ran_id] #random id for a collidable tile

            possible_orientations = []

            if tile_id >= CHUNK_SIZE_TILES: #tile is not in the top row
                if chunk.tiles[tile_id - CHUNK_SIZE_TILES] != 1: #tile above is open space
                    possible_orientations.append(0)
                    completely_obstructed = False
            if tile_id % CHUNK_SIZE_TILES != CHUNK_SIZE_TILES - 1: #tile is not in the rightmost column
                if chunk.tiles[tile_id + 1] != 1: #tile to the right is open space
                    possible_orientations.append(1)
                    completely_obstructed = False
            if tile_id <= CHUNK_AREA_TILES - CHUNK_SIZE_TILES: #tile is not in the bottom row
                if chunk.tiles[tile_id + CHUNK_SIZE_TILES] != 1: #tile below is open space
                    possible_orientations.append(2)
                    completely_obstructed = False
            if tile_id % CHUNK_SIZE_TILES != 0: #tile is not in the leftmost column
                if chunk.tiles[tile_id - 1] != 1: #tile to the left is open space
                    possible_orientations.append(3)
                    completely_obstructed = False

            if not completely_obstructed:
                #a suitable tile has been found! this will be used as an anchor point for the sessile creature
                tile = chunk.collidable_tiles[ran_id]
                orientation = possible_orientations[random.randint(0, len(possible_orientations) - 1)]
                return tile, orientation
    
    def get_pos(self, size):
        offset = size[1] / 2
        #position the creature relative to the tile according to its orientation
        match self.orientation:
            case 0: #top
                midtop = self.tile.midtop
                pos = (midtop[0], midtop[1] - offset)
            case 1: #right
                midright = self.tile.midright
                pos = (midright[0] + offset, midright[1])
            case 2: #bottom
                midbottom = self.tile.midbottom
                pos = (midbottom[0], midbottom[1] + offset)
            case 3: #left
                midleft = self.tile.midleft
                pos = (midleft[0] - offset, midleft[1])
        return pos
    
    def rotate_image(self):
        match self.orientation:
            case 1: #right
                self.image = pg.transform.rotate(self.image, 270)
            case 2: #bottom
                self.image = pg.transform.rotate(self.image, 180)
            case 3: #left
                self.image = pg.transform.rotate(self.image, 90)

#creatures that move on solid surfaces, such as crabs (discontinued until I have the motivation to continue)
class CrawlingCreature(GroundCreature):
    def __init__(self, chunk, type, images):
        super().__init__(chunk, type, images)
        self.chunk = chunk
        self.speed = type["speed"]
        self.pos = pg.Vector2(self.pos)
        self.direction = pg.Vector2(1.0, 1.0)

        self.update_collision_rects()
    
    def update_collision_rects(self):
        self.collision_rects = [
            pg.Rect(self.rect.left, self.rect.top - 1, self.rect.width, 1), #top
            pg.Rect(self.rect.right, self.rect.top, 1, self.rect.height), #right
            pg.Rect(self.rect.left, self.rect.bottom, self.rect.width, 1), #bottom
            pg.Rect(self.rect.left - 1, self.rect.top, 1, self.rect.height) #left
        ]
    
    def move(self, collidable_tiles, delta_t):
        self.pos += self.speed * self.direction * delta_t
        self.rect.center = self.pos
        self.clip_to_tile_surfaces(collidable_tiles)
    
    def clip_to_tile_surfaces(self, collidable_tiles):
        for tile in collidable_tiles:
            if tile.colliderect(self.collision_rects[0]): #top
                self.rect.top = tile.bottom
            if tile.colliderect(self.collision_rects[1]): #right
                self.rect.right = tile.left
            if tile.colliderect(self.collision_rects[2]): #bottom
                self.rect.bottom = tile.top
            if tile.colliderect(self.collision_rects[3]): #left
                self.rect.left = tile.right
        
        self.pos = self.rect.center
        #self.rotate_image()

    def update(self, window, focus_pos, collidable_tiles, delta_t):
        self.draw(window, focus_pos)
        self.move(collidable_tiles, delta_t)
        for rect in self.collision_rects:
            apparent_rect = rect.copy()
            apparent_rect.left -= focus_pos.x
            apparent_rect.top -= focus_pos.y
            pg.draw.rect(window, (255, 0, 0), apparent_rect)
        self.update_collision_rects()

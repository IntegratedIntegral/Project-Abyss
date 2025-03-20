from settings import *

def generate_unit_vec_list():
    unit_vectors = []
    for i in range(32):
        angle = i / 16 * math.pi
        vector = pg.Vector2(math.cos(angle), math.sin(angle))
        unit_vectors.append(vector)
    return unit_vectors

unit_vec_list = generate_unit_vec_list()

def ran_unit_vector(x, y, seed):
    unit_vec_id = (5 * x + 3 * y + 7 * seed + 11 * x * y) % 16
    return unit_vec_list[unit_vec_id]

def lerp(a0, a1, t):
    return a0 + (a1 - a0) * t

def smooth(x):
    return x * x * x * (x * (6 * x - 15) + 10)

def noise(x, y, seed):
    int_x = math.floor(x)
    int_y = math.floor(y)
    local_x = x - int_x
    local_y = y - int_y
    ran_corner_vecs = (
        ran_unit_vector(int_x, int_y, seed), #upper left
        ran_unit_vector(int_x + 1, int_y, seed), #upper right
        ran_unit_vector(int_x, int_y + 1, seed), #lower left
        ran_unit_vector(int_x + 1, int_y + 1, seed) #lower right
    )
    corner_offsets = (
        pg.Vector2(local_x, local_y),
        pg.Vector2(local_x - 1, local_y),
        pg.Vector2(local_x, local_y - 1),
        pg.Vector2(local_x - 1, local_y - 1)
    )
    dot_prods = []
    for ran_corner_vec, corner_offset in zip(ran_corner_vecs, corner_offsets):
        dot_prods.append(ran_corner_vec.dot(corner_offset))
    return lerp(lerp(dot_prods[0], dot_prods[1], smooth(local_x)), lerp(dot_prods[2], dot_prods[3], smooth(local_x)), smooth(local_y)) * 2 / 3 ** 0.5

class Chunk:
    def __init__(self, chunk_pos, dominant_sessile_creature, generate_new_tiles=True, tiles=[]):
        self.pos = CHUNK_SIZE * pg.Vector2(chunk_pos)

        if generate_new_tiles: self.tiles, self.collidable_tiles, self.collidable_ids = self.generate_tiles()
        else:
            self.tiles = tiles
            self.collidable_tiles, self.collidable_ids = self.get_collidable_tiles()

        self.dominant_sessile_creature = dominant_sessile_creature
    
    def generate_tiles(self):
        tiles = []
        collidable_tiles = []
        collidable_ids = []
        radius = CHUNK_SIZE_TILES / 2

        collidable_seed = random.randint(0, 31)
        deform_seed = random.randint(0, 31)
        hole_seed = random.randint(0, 31)

        for tile_y in range(CHUNK_SIZE_TILES):
            for tile_x in range(CHUNK_SIZE_TILES):
                noise_val = noise(tile_x * 0.18, tile_y * 0.18, collidable_seed)
                if (tile_x - radius) ** 2 + (tile_y - radius) ** 2 + 64 * noise(tile_x * 0.25, tile_y * 0.25, deform_seed) < radius * radius: #makes the filled in area of the chunk into a deformed circle shape
                    if abs(noise_val) < 0.25: #empty space
                        if noise(tile_x * 0.11, tile_y * 0.11, hole_seed) > 0.2:
                            #nothing
                            tiles.append(0)
                        else:
                            #wall
                            tiles.append(2)
                    else:
                        #collidable tile
                        tiles.append(1)
                        collidable_tiles.append(pg.Rect((tile_x * TILE_SIZE + self.pos.x, tile_y * TILE_SIZE + self.pos.y), (TILE_SIZE, TILE_SIZE)))
                        collidable_ids.append(tile_x + tile_y * CHUNK_SIZE_TILES)
                else:
                    tiles.append(0)
        
        return tiles, collidable_tiles, collidable_ids
    
    def get_collidable_tiles(self):
        collidable_tiles = []
        collidable_ids = []
        for i in range(len(self.tiles)):
            tile_id = self.tiles[i]
            if tile_id == 1:
                collidable_ids.append(i)

                x = (i % CHUNK_SIZE_TILES) * TILE_SIZE
                y = (i // CHUNK_SIZE_TILES) * TILE_SIZE
                collidable_tiles.append(pg.Rect((x + self.pos.x, y + self.pos.y), (TILE_SIZE, TILE_SIZE)))
        
        return collidable_tiles, collidable_ids

    def draw(self, window, focus_pos, tile_images):
        for i in range(CHUNK_AREA_TILES):
            tile = self.tiles[i]
            if tile:
                x = (i % CHUNK_SIZE_TILES) * TILE_SIZE + self.pos.x - focus_pos.x
                y = (i // CHUNK_SIZE_TILES) * TILE_SIZE + self.pos.y - focus_pos.y
                
                if tile == 1: image = tile_images["rock"]
                else: image = tile_images["rock_wall"]
                window.blit(image, (x, y))
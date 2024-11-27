import json
from settings import *
from player import Player
from chunk import Chunk
from creature import SwimmingCreature, GroundCreature
from submarine import Submarine
from map import Map
from particles import Particles

class WorldObjects:
    def __init__(self, image_loader):
        self.image_loader = image_loader
        self.font = pg.font.SysFont("arial", 36)
        self.layer_text = self.font.render(LAYER_NAMES[0] + " zone", True, (255, 255, 255))

        self.layer_index = 0
        self.old_layer_index = 0
        self.fade_timer = FADE_TIMER
        self.new_layer_entered = True

        self.swimming_creature_types, self.sessile_creature_types = self.load_creatures()

        self.player = Player(PLAYER_STARTING_POS, image_loader.player, image_loader.tank)
        self.submarine = Submarine(SUBMARINE_STARTING_POS, image_loader.submarine)
        self.map = Map()

        self.chunks = self.generate_chunks()#[Chunk((0, 0)), Chunk((1, 0))]
        self.visited_chunks = []

        self.swimming_creatures = []
        self.swimming_creature_spawn_timer = random.randint(SWIMMING_CREATURE_SPAWN_TIMER_MIN, SWIMMING_CREATURE_SPAWN_TIMER_MAX)
        self.sessile_creatures = []
        #self.crab = CrawlingCreature(self.chunks[0], self.crawling_creature_types[0], self.image_loader.swimming_creatures)

        self.focus_pos = pg.Vector2()

        self.particles = Particles(self.focus_pos)

        #add all species to the journal, for debugging purposes only
        #for layer_swimming_creatures in self.swimming_creature_types:
        #    for swimming_creature in layer_swimming_creatures:
        #        self.player.journal.add_species(swimming_creature)
        #for layer_sessile_creatures in self.sessile_creature_types:
        #    for sessile_creature in layer_sessile_creatures:
        #        self.player.journal.add_species(sessile_creature)
    
    def update_focus_pos(self):
        #x
        if self.player.pos.x < SEMI_WINDOW_WIDTH:
            self.focus_pos.x = 0
        elif self.player.pos.x > WORLD_WIDTH - SEMI_WINDOW_WIDTH:
            self.focus_pos.x = WORLD_WIDTH - WINDOW_WIDTH
        else:
            self.focus_pos.x = self.player.pos.x - SEMI_WINDOW_WIDTH
        
        #y
        if self.player.pos.y < SEMI_WINDOW_HEIGHT:
            self.focus_pos.y = 0
        elif self.player.pos.y > WORLD_HEIGHT - SEMI_WINDOW_HEIGHT:
            self.focus_pos.y = WORLD_HEIGHT - WINDOW_HEIGHT
        else:
            self.focus_pos.y = self.player.pos.y - SEMI_WINDOW_HEIGHT
    
    def update(self, window, lmb_pressed, rmb_pressed, delta_t):
        self.update_focus_pos()
        self.update_spawn_timer(delta_t)

        if not self.new_layer_entered:
            self.old_layer_index = self.layer_index
        self.layer_index = self.get_layer_index()
        
        if self.old_layer_index != self.layer_index:
            self.new_layer_entered = True
            self.layer_text = self.font.render(LAYER_NAMES[self.layer_index] + " zone", True, (255, 255, 255))
        self.update_fade_timer(delta_t)
        
        collidable_tiles = [] #list of collidable tiles that are within range of player.
        visible_chunks = []
        for chunk in self.chunks:
            apparent_pos = chunk.pos - self.focus_pos
            #only draw chunk if it is within the window borders
            if apparent_pos.x + CHUNK_SIZE > 0 and apparent_pos.x < WINDOW_WIDTH and apparent_pos.y + CHUNK_SIZE > 0 and apparent_pos.y < WINDOW_HEIGHT:
                chunk.draw(window, self.focus_pos, self.image_loader.tiles)
                #adds the chunks collidable tiles to this list only when the chunk is in viewing range, so that the player's collision detection doesn't have to worry about tiles off the border. 
                collidable_tiles += chunk.collidable_tiles
                visible_chunks.append(chunk)
                if not chunk in self.visited_chunks:
                    self.spawn_sessile_creatures(chunk)
        
        self.particles.update(window, self.focus_pos, self.image_loader.particle, delta_t)

        #update swimming creatures
        for creature in self.swimming_creatures:
            self.update_swimming_creature(window, creature, lmb_pressed, delta_t)
        
        #draw sessile creatures
        for creature in self.sessile_creatures:
            self.update_sessile_creature(window, creature, lmb_pressed)
        
        self.submarine.draw(window, self.focus_pos)
        self.player.update(window, self.focus_pos, collidable_tiles, self.submarine, self.map.waypoint, self.image_loader.creatures, lmb_pressed, delta_t)
        
        #self.crab.update(window, self.focus_pos, collidable_tiles, delta_t)

        if self.player.boarded:
            self.map.update(window, self.chunks, lmb_pressed, rmb_pressed, self.submarine)
        
        window.blit(self.layer_text, (20, 20))
        
        self.visited_chunks = visible_chunks

        if self.player.oxygen <= 0:
            self.reset()
    
    def update_spawn_timer(self, delta_t):
        if self.swimming_creature_spawn_timer > 0:
            self.swimming_creature_spawn_timer -= delta_t
        else:
            self.spawn_swimming_creature()
            self.swimming_creature_spawn_timer = random.randint(SWIMMING_CREATURE_SPAWN_TIMER_MIN, SWIMMING_CREATURE_SPAWN_TIMER_MAX)
    
    def spawn_swimming_creature(self):
        #spawn a swimming creature of random type from a certain distance from player
        ran_angle = random.random() * 2 * math.pi
        x = SWIMMING_CREATURE_SPAWN_DIST * math.cos(ran_angle) + self.player.pos.x
        y = SWIMMING_CREATURE_SPAWN_DIST * math.sin(ran_angle) + self.player.pos.y
        
        #only a creature native to the current layer will spawn
        possible_types = self.swimming_creature_types[self.layer_index]

        ran_type = possible_types[random.randint(0, len(possible_types) - 1)]

        self.swimming_creatures.append(SwimmingCreature((x, y), ran_type, self.image_loader.creatures))
    
    def update_swimming_creature(self, window, creature, lmb_pressed, delta_t):
        creature.update(window, self.focus_pos, self.player, lmb_pressed, delta_t)
        if (creature.pos - self.player.pos).magnitude_squared() > CREATURE_DESPAWN_DIST * CREATURE_DESPAWN_DIST:
            self.swimming_creatures.remove(creature) #despawn the creature if it moves too far from player. This prevents the swimming creature list from growing too large.
        
        if (creature.pos - self.player.pos).magnitude_squared() < SPOOK_DIST * SPOOK_DIST and self.player.is_moving:
            creature.flee(self.player)
    
    def spawn_sessile_creatures(self, chunk):
        for _ in range(random.randint(10, 30)):
            #the creature will most likely be the dominant one of the chunk, however there is a 10% chance for it to be something else
            layer_index = self.get_layer_index(chunk.pos.y)
            possible_types = self.sessile_creature_types[layer_index]
            if random.random() < 0.1:
                type = possible_types[random.randint(0, len(possible_types) - 1)]
            else:
                for possible_type in possible_types:
                    if possible_type["name"] == chunk.dominant_sessile_creature:
                        type = possible_type
                        break
            self.sessile_creatures.append(GroundCreature(chunk, type, self.image_loader.creatures))
    
    def update_sessile_creature(self, window, creature, lmb_pressed):
        creature.update(window, self.focus_pos, self.player, lmb_pressed)
        if (creature.pos - self.player.pos).magnitude_squared() > CREATURE_DESPAWN_DIST * CREATURE_DESPAWN_DIST:
            self.sessile_creatures.remove(creature) #despawn the creature if it moves too far from player. This prevents the sessile creature list from growing too large.

    def generate_chunks(self):
        chunks = []
        for y in range(WORLD_HEIGHT_CHUNKS):
            for x in range(WORLD_WIDTH_CHUNKS):
                ran = random.random()
                if ran < CHUNK_DENSITY:
                    #only a creature native to the current layer will spawn
                    layer_index = self.get_layer_index(y * CHUNK_SIZE)
                    possible_types = self.sessile_creature_types[layer_index]
                    
                    dominant_sessile_creature = possible_types[random.randint(0, len(possible_types) - 1)]["name"]
                    chunks.append(Chunk((x, y), dominant_sessile_creature))
        return chunks

    def load_creatures(self):
        with open("creature_types.json") as file:
            data = json.load(file)
            swimming_creatures = self.seperate_based_on_layer(data["swimming_creatures"])
            sessile_creatures = self.seperate_based_on_layer(data["sessile_creatures"])
        return swimming_creatures, sessile_creatures
    
    @staticmethod
    def seperate_based_on_layer(creatures):
        seperated_creatures = [
            [], #epipelagic
            [], #mesopelagic
            [], #bathypelagic
            []  #abyssopelagic
        ]

        for creature in creatures:
            layer = creature["layer"]
            seperated_creatures[layer].append(creature)
        
        return seperated_creatures

    def reset(self):
        self.player.reset()
        self.submarine.pos = pg.Vector2(SUBMARINE_STARTING_POS)

    def get_layer_index(self, depth=None):
        if not depth:
            depth = self.player.pos.y
        
        for i in range(len(LAYER_DEPTH_VALS)):
            layer_depth = LAYER_DEPTH_VALS[i]
            if depth < layer_depth:
                return i - 1
        return 3

    def update_fade_timer(self, delta_t):
        if self.new_layer_entered:
            if self.fade_timer > 0:
                self.fade_timer -= delta_t
            else:
                self.fade_timer = FADE_TIMER
                self.new_layer_entered = False

    def get_bg_colour(self):
        if self.new_layer_entered:
            old_colour = pg.Vector3(LAYER_BG_COLOURS[self.old_layer_index])
            new_colour = pg.Vector3(LAYER_BG_COLOURS[self.layer_index])
            t = 1 - self.fade_timer / FADE_TIMER
            return old_colour + (new_colour - old_colour) * t
        else:
            return LAYER_BG_COLOURS[self.layer_index]
import pygame as pg
import math
import random

pg.font.init()

WINDOW_WIDTH = 1700
WINDOW_HEIGHT = 950
SEMI_WINDOW_WIDTH = WINDOW_WIDTH // 2
SEMI_WINDOW_HEIGHT = WINDOW_HEIGHT // 2

UI_FONT = pg.font.SysFont("arial", 20)
BUTTON_COLOUR = (201, 201, 201)

#BRIGHTNESS_HALF_LIFE = 1100
#BRIGHTNESS_DECAY_CONSTANT = -math.log(math.pow(0.5, 1 / BRIGHTNESS_HALF_LIFE)) #how quickly the brightness decreases with depth

TILE_SIZE = 64
CHUNK_SIZE_TILES = 25 #measured in tiles
CHUNK_AREA_TILES = CHUNK_SIZE_TILES * CHUNK_SIZE_TILES
CHUNK_SIZE = CHUNK_SIZE_TILES * TILE_SIZE

WORLD_WIDTH = 64000
WORLD_HEIGHT = 600000
#world dimensions measured in chunks
WORLD_WIDTH_CHUNKS = WORLD_WIDTH // CHUNK_SIZE
WORLD_HEIGHT_CHUNKS = WORLD_HEIGHT // CHUNK_SIZE
CHUNK_DENSITY = 0.06

PLAYER_DIMENSIONS = (50, 180)
PLAYER_STARTING_POS = (WORLD_WIDTH / 2, 300.0)
MAX_OXYGEN = 180000 #3 minutes
TANK_DIMENSIONS = (40, 209)
OXYGEN_BAR_DIMENSIONS = (20, 200)

SWIMMING_CREATURE_SPAWN_DIST = 1000
CREATURE_DESPAWN_DIST = 3000
SWIMMING_CREATURE_SPAWN_TIMER_MIN = 10000
SWIMMING_CREATURE_SPAWN_TIMER_MAX = 20000
SPOOK_FACTOR = 4.5 #a multiplier to the speed of a swimming creature when it is spooked by the player
SPOOK_DIST = 300 #the distance at which a swimming creature will get spooked by the player
DOCUMENT_DIST = 100

BOARDING_DIST = 250
SUBMARINE_STARTING_POS = (WORLD_WIDTH / 2, 600.0)

PARTICLE_COUNT = 30
PARTICLE_SPAWN_TIMER = 1000

#Depth values for the start of each layer
LAYER_DEPTH_VALS = [0, 20000, 100000, 400000]
LAYER_BG_COLOURS = [(20, 127, 201), (6, 37, 71), (1, 6, 28), (0, 1, 2)]
LAYER_NAMES = ["Epipelagic", "Mesopelagic", "Bathypelagic", "Abyssopelagic"]

FADE_TIMER = 2000 #time it takes for the background colour to transition when entering a different layer
from settings import pg, TILE_SIZE

class ImageLoader:
    def __init__(self):
        self.player = self.load("player")
        self.submarine = self.load("submarine")
        self.tank = self.load("tank")
        self.tiles = {
            "rock": self.load_tile("rock"),
            "rock_wall": self.load_tile("rock_wall")
        }
        self.creatures = {
            "clownfish": self.load("clownfish"),
            "salmon": self.load("salmon"),
            "mackerel": self.load("mackerel"),
            "moon_jellyfish": self.load("moon_jellyfish"),
            "compass_jelly": self.load("compassjelly"),
            "cutlassfish": self.load("cutlassfish"),
            "lanternfish": self.load("lanternfish"),
            "sabertooth_fish": self.load("sabertooth_fish"),
            "vampire_squid": self.load("vampire_squid"),
            "chimaera": self.load("chimaera"),
            "anglerfish": self.load("angler"),
            "cusk_eel": self.load("cusk_eel"),
            "dumbo_octopus": self.load("dumbooctopus"),
            "sea_anemone": self.load("sea_anemone"),
            "barnacles": self.load("barnacles"),
            "seagrass": self.load("seagrass"),
            "mussels": self.load("mussels"),
            "reef_coral": self.load("reef_coral"),
            "sponge": self.load("sponge"),
            "sea_pen": self.load("sea_pen"),
            "tube_worm": self.load("tube_worm"),
            "bubblegum_coral": self.load("bubblegum_coral"),
            "deep_crinoid": self.load("deep_crinoid")
        }
        self.particle = self.load("particle")
    
    def load(self, path):
        image = pg.image.load(f"assets/{path}.png").convert()
        image.set_colorkey((0, 0, 0))
        return image
    
    def load_tile(self, path):
        image = self.load(path)
        image = pg.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        return image
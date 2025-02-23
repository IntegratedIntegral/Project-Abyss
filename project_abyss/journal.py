from settings import *
from paragraph_render import render_paragraph

class Journal:
    def __init__(self):
        self.surf = pg.surface.Surface((700, 800))
        self.surf.fill((89, 89, 89))
        self.pos = pg.Vector2(1000, 70)

        self.info_panel = pg.surface.Surface((400, 200))
        self.info_panel.fill(BUTTON_COLOUR)

        self.species = []
        self.icon_positions = []

        self.icon_size = 96
        self.grid_width = self.surf.size[0] // self.icon_size

        self.font = pg.font.SysFont("arial", 16)
    
    def update(self, window, images, lmb_pressed):
        self.draw(window, images)
        self.select_species(lmb_pressed)
    
    def draw_species(self, index, images):
        species = self.species[index] #singular for species is species!

        image = images[species["image_id"]]
        size = image.size
        if size[0] > size[1]: #image is wider than it is tall
            height = size[1] / size[0] * self.icon_size
            image = pg.transform.scale(image, (self.icon_size, height))
            offset = pg.Vector2(0, (self.icon_size - height) / 2)
        else:
            width = size[0] / size[1] * self.icon_size
            image = pg.transform.scale(image, (width, self.icon_size))
            offset = pg.Vector2((self.icon_size - width) / 2, 0)
        
        self.surf.blit(image, self.icon_positions[index] + offset)
    
    def draw(self, window, images):
        for i in range(len(self.species)):
            self.draw_species(i, images)
        
        self.surf.blit(self.info_panel, (150, 600))
        window.blit(self.surf, self.pos)
    
    def add_species(self, species):
        i = len(self.species)
        self.species.append(species)
        self.icon_positions.append((self.icon_size * (i % self.grid_width), self.icon_size * (i // self.grid_width)))
    
    def select_species(self, lmb_pressed):
        if lmb_pressed:
            mouse_pos = pg.Vector2(pg.mouse.get_pos())
            for i in range(len(self.species)):
                icon_pos = self.icon_positions[i]
                rel_mouse_pos = mouse_pos - icon_pos - self.pos
                if rel_mouse_pos.x > 0 and rel_mouse_pos.x < self.icon_size and rel_mouse_pos.y > 0 and rel_mouse_pos.y < self.icon_size:
                    self.show_info(self.species[i])
    
    def show_info(self, species):
        self.info_panel.fill(BUTTON_COLOUR)
        
        title_surf = self.font.render(species["name"], True, (0, 0, 0))
        self.info_panel.blit(title_surf, (30, 8))
        
        desc_surf = render_paragraph(species["description"], self.font, 380)
        self.info_panel.blit(desc_surf, (10, 28))
    
    def reset(self):
        self.species = []
        self.icon_positions = []
        self.surf.fill((89, 89, 89))
        self.info_panel.fill((201, 201, 201))
import os
from settings import *
from image_loader import ImageLoader
from world_objects import WorldObjects
from main_menu import MainMenu
from pause_menu import PauseMenu
from save_menu import SaveMenu

class Main:
    def __init__(self):
        self.running = True

        pg.init()
        self.window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.mainmenu = MainMenu()
        self.mainmenu_active = True

        self.pausemenu = PauseMenu()
        self.pausemenu_active = False

        self.savemenu = SaveMenu()
        self.savemenu_active = False
        
        #pg.display.set_caption("Project Abyss (loading, please wait)")
        self.image_loader = ImageLoader()

        self.delta_t = 0
        
        self.lmb_pressed = False
        self.rmb_pressed = False

        pg.display.set_caption("Project Abyss")

        self.bg_colour = LAYER_BG_COLOURS[0]

        self.clock = pg.time.Clock()
    
    def load_world(self, save_data, save_name):
        self.world_objects = WorldObjects(save_data, save_name, self.image_loader)
    
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                self.world_objects.save()
        
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.lmb_pressed = True
                if event.button == 3:
                    self.rmb_pressed = True
            
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.lmb_pressed = False
                if event.button == 3:
                    self.rmb_pressed = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if not (self.mainmenu_active or self.savemenu_active): self.pausemenu_active = not self.pausemenu_active

    def run(self):
        while self.running:
            self.delta_t = self.clock.tick(60)

            self.check_events()

            if self.mainmenu_active:
                self.window.fill(self.bg_colour)
                self.mainmenu.update(self)
            elif self.pausemenu_active:
                self.pausemenu.update(self)
            elif self.savemenu_active:
                self.window.fill(self.bg_colour)
                self.savemenu.update(self)
            else:
                self.window.fill(self.bg_colour)
                self.bg_colour = self.world_objects.get_bg_colour()
                self.world_objects.update(self.window, self.lmb_pressed, self.rmb_pressed, self.delta_t)

            pg.display.flip()
        pg.quit()

if __name__ == "__main__":
    #dir_path = os.path.realpath(os.path.dirname(__file__))
    #print(dir_path)
    #os.chdir(dir_path)
    
    app = Main()
    app.run()
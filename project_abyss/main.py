import os
from settings import *
from image_loader import ImageLoader
from world_objects import WorldObjects
from main_menu import MainMenu
from pause_menu import PauseMenu

class Main:
    def __init__(self):
        self.running = True

        pg.init()
        self.window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.mainmenu = MainMenu()
        self.mainmenu_active = True

        self.pausemenu = PauseMenu()
        self.pausemenu_active = False
        
        pg.display.set_caption("Project Abyss (loading, please wait)")
        self.image_loader = ImageLoader()

        self.delta_t = 0

        self.world_objects = WorldObjects(self.image_loader)
        
        self.lmb_pressed = False
        self.rmb_pressed = False

        pg.display.set_caption("Project Abyss")

        self.bg_colour = LAYER_BG_COLOURS[0]

        self.clock = pg.time.Clock()
    
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
        
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
                    self.pausemenu_active = not self.pausemenu_active

    def run(self):
        while self.running:
            self.delta_t = self.clock.tick(60)

            self.check_events()

            if self.mainmenu_active:
                self.window.fill(self.bg_colour)
                self.mainmenu.update(self)
            elif self.pausemenu_active:
                self.pausemenu.update(self)
            else:
                self.window.fill(self.bg_colour)
                self.bg_colour = self.world_objects.get_bg_colour()
                self.world_objects.update(self.window, self.lmb_pressed, self.rmb_pressed, self.delta_t)

            pg.display.flip()
        pg.quit()

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    
    app = Main()
    app.run()

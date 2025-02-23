from settings import *
from button import Button

class MainMenu:
    def __init__(self):
        self.play_button = Button((140, 350), (180, 40), text="play")
        self.quit_button = Button((140, 410), (180, 40), text="quit")
    
    def update(self, app):
        self.play_button.update(app.window)
        self.quit_button.update(app.window)
        
        if self.play_button.pressed:
            app.mainmenu_active = False
        if self.quit_button.pressed:
            app.running = False
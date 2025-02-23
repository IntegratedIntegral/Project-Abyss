from settings import *
from button import Button

class PauseMenu():
    def __init__(self):
        self.resume_button = Button((760, 400), (180, 40), text="resume")
        self.exit_button = Button((760, 460), (180, 40), text="exit to main menu")
    
    def update(self, app):
        self.resume_button.update(app.window)
        self.exit_button.update(app.window)

        if self.resume_button.pressed:
            app.pausemenu_active = False
        if self.exit_button.pressed:
            app.mainmenu_active = True
            app.pausemenu_active = False
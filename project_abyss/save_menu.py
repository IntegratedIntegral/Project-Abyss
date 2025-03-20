from settings import *
from button import Button
import json
import os

class SaveMenu:
    def __init__(self):
        self.new_button = Button((140, 350), (180, 40), text="new game")
        self.save_buttons = self.generate_save_buttons()
    
    def generate_save_buttons(self):
        save_buttons = []
        saves = os.listdir("save_data")
        for i in range(len(saves)):
            save = saves[i]
            save_buttons.append(Button((140, 410 + 60 * i), (180, 40), text=save.rstrip(".json")))
        return save_buttons
    
    def update(self, app):
        self.new_button.update(app.window)

        if self.new_button.pressed:
            index = len(self.save_buttons)
            self.save_buttons.append(Button((140, 410 + 60 * index), (180, 40), text="game" + str(index)))

            data = {
                "player_pos": PLAYER_STARTING_POS,
                "submarine_pos": SUBMARINE_STARTING_POS,
                "layer": 0,
                "documented_species": [],
                "chunks": []
            }
            with open(f"save_data/game{index}.json", "x") as file:
                json.dump(data, file)
        
        for i in range(len(self.save_buttons)):
            button = self.save_buttons[i]
            button.update(app.window)
            if button.pressed:
                saves = os.listdir("save_data")
                save = saves[i]
                app.savemenu_active = False
                with open(f"save_data/{save}") as file:
                    save_data = json.load(file)
                app.load_world(save_data, save)
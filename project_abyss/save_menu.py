from settings import *
from button import Button
import json
import os

class SaveMenu:
    def __init__(self):
        self.new_button = Button((140, 350), (180, 40), text="new game")
        self.back_button = Button((340, 350), (180, 40), text="back")
        self.save_buttons, self.delete_buttons = self.generate_buttons()
    
    def generate_buttons(self):
        save_buttons = []
        delete_buttons = []
        saves = os.listdir("save_data")
        for i in range(len(saves)):
            save = saves[i]

            y = 410 + 60 * i
            save_buttons.append(Button((140, y), (180, 40), text=save.rstrip(".json")))
            delete_buttons.append(Button((340, y), (180, 40), text="delete"))
        return save_buttons, delete_buttons
    
    def update(self, app):
        self.new_button.update(app.window)
        self.back_button.update(app.window)

        #NEW SAVE BUTTON
        if self.new_button.pressed:
            index = len(self.save_buttons)
            y = 410 + 60 * index
            self.save_buttons.append(Button((140, y), (180, 40), text="game" + str(index)))
            self.delete_buttons.append(Button((340, y), (180, 40), text="delete"))

            data = {
                "player_pos": PLAYER_STARTING_POS,
                "submarine_pos": SUBMARINE_STARTING_POS,
                "layer": 0,
                "documented_species": [],
                "chunks": []
            }
            with open(f"save_data/game{index}.json", "x") as file:
                json.dump(data, file)
        
        #BACK BUTTON
        if self.back_button.pressed:
            app.savemenu_active = False
            app.mainmenu_active = True
        
        #LOAD AND DELETE BUTTONS
        for i in range(len(self.save_buttons)):
            save_button = self.save_buttons[i]
            save_button.update(app.window)
            if save_button.pressed:
                saves = os.listdir("save_data")
                save = saves[i]
                app.savemenu_active = False
                with open(f"save_data/{save}") as file:
                    save_data = json.load(file)
                app.load_world(save_data, save)
            
            delete_button = self.delete_buttons[i]
            delete_button.update(app.window)
            if delete_button.pressed:
                saves = os.listdir("save_data")
                save = saves[i]
                os.remove(f"save_data/{save}")
                self.save_buttons.remove(save_button)
                self.delete_buttons.remove(delete_button)
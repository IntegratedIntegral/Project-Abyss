from settings import *

class Button:
    def __init__(self, pos, size, text="", surf=None, colour=BUTTON_COLOUR):
        self.rect = pg.Rect(pos, size)
        
        if text:
            self.surf = pg.surface.Surface(size)
            self.surf.fill(colour)
            text_surf = UI_FONT.render(text, True, (0, 0, 0), bgcolor=colour)
            self.surf.blit(text_surf, ((size[0] - text_surf.size[0]) // 2, (size[1] - text_surf.size[1]) // 2))
        elif surf:
            self.surf = pg.transform.scale(surf, size)
        else:
            self.surf = pg.surface.Surface(size)
            self.surf.fill(colour)

        self.clicked = False
    
    def update(self, window):
        window.blit(self.surf, self.rect)

        mouse_pos = pg.mouse.get_pos()
        lmb_pressed = pg.mouse.get_just_pressed()[0]
        self.pressed = lmb_pressed and self.rect.collidepoint(mouse_pos)
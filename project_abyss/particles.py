from settings import *

class Particles:
    def __init__(self, focus_pos):
        self.particles = []
        for _ in range(PARTICLE_COUNT):
            self.spawn_particle(focus_pos)
        
        self.spawn_timer = PARTICLE_SPAWN_TIMER
    
    def update(self, window, focus_pos, image, delta_t):
        self.draw(window, focus_pos, image)
        self.update_timer(focus_pos, delta_t)
    
    def draw(self, window, focus_pos, image):
        for particle in self.particles:
            rect = pg.Rect((0, 0), (5, 5))
            rect.center = particle - focus_pos
            window.blit(image, rect)
    
    def spawn_particle(self, focus_pos):
        ran_x = random.randint(0, WINDOW_WIDTH) + focus_pos.x
        ran_y = random.randint(0, WINDOW_HEIGHT) + focus_pos.y
        self.particles.append((ran_x, ran_y))
    
    def update_timer(self, focus_pos, delta_t):
        if self.spawn_timer > 0:
            self.spawn_timer -= delta_t
        else:
            self.spawn_timer = PARTICLE_SPAWN_TIMER
            del self.particles[0]
            self.spawn_particle(focus_pos)
from .animation import *
import time

class AbcParticles:

    def __init__(self, dx, dy, x, y, enemies):
        #dx and dy is direction on Ox and Oy of movement vector. 1 is up and right, -1 is down and left
        self.dx = dx
        self.dy = dy
        self.x = 0
        self.y = 0
        self.iterative = False
        self.lifetime = 0
        self.enemies = enemies
        self.animation = None
        self.born_time = 0
        self.speed = 0

    def collide_script(self, person):
        pass

    def spell_animation(self, fps_num):
        pass
class DamageSpellParticle:

    def __init__(self, dx, dy,x, y, enemies):
        super().__init__(dx, dy, x, y, enemies)
        self.iterative = False
        self.lifetime = 5
        self.enemies = enemies
        self.animation = Animation("resources/particles_animation/damage_spell_particles", 1)
        self.born_time = time.time()
        self.speed = 0.2


    def collide_script(self, person):
        person.health -= 5

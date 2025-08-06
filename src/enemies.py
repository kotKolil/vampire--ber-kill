from pyray import *
from math import *

class AbcEnemy:
    def __init__(self, pos_x, pos_y):
        self.health = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.texture = ""
        self.damage = 0
        self.attack_radius = 0

    def ai_script(self, hero_clas):
        pass

class RobotEnemy(AbcEnemy):

    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.health = 50
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.texture = load_texture_from_image(load_image("resources/robot_enemy.png"))
        self.damage = 10
        self.attack_radius = 30

    def ai_script(self, hero_class):
        if (hero_class.player_pos_x - self.attack_radius < self.pos_x < hero_class.player_pos_x + self.attack_radius) and (hero_class.player_pos_y - self.attack_radius < self.pos_y < hero_class.player_pos_y  + self.attack_radius):
                hero_class.health -= self.damage
                hero_class.health -= 10
                return
        x1 = (hero_class.player_pos_x - self.pos_x) // abs(hero_class.player_pos_x - self.pos_x)
        y1 =  (hero_class.player_pos_y - self.pos_y) // abs(hero_class.player_pos_y - self.pos_y)
        self.pos_x += x1
        self.pos_y += y1



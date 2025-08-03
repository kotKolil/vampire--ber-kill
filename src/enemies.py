from pyray import *


class AbcEnemy:
    def __init__(self, pos_x, pos_y):
        self.health = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.texture = ""
        self.damage = 0

    def ai_script(self):
        pass

class RobotEnemy(AbcEnemy):

    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.health = 50
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.texture = load_texture_from_image(load_image("resources/robot_enemy.png"))
        self.damage = 10

    def ai_script(self):
        pass


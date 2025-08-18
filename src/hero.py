from math import *
from .animation import *

class Hero:
    def __init__(self, window_width, window_height):
        self.player_pos_x = window_width // 2
        self.player_pos_y = window_height // 2
        self.speed = 4
        self.attack_radius = 30
        self.blade_attack_damage = 60
        self.base_hp = 23453467
        self.base_mana = 60
        self.health = 23453467
        self.mana = 60
        self.state = "idle"
        self.current_spell = None
        self.texture  = load_texture_from_image(load_image("../resources/hero3.png"))

        self.idle_animation = Animation("resources/hero/idle", 3)
        self.texture = self.idle_animation.frames[0]
        self.right_run_animation = Animation("resources/hero/right_run", 3)
        self.left_run_animation = Animation("resources/hero/left_run", 3)
        self.attack_animation = Animation("resources/hero/attack", 30)
        self.death_animation = Animation("resources/hero/attack", 9)
        self.death_animation = Animation('resources/hero/death', 9)
        self.damage_animation = Animation("resources/hero/damage", 1000)


    def get_angle(self, mouse_pos_x, mouse_pos_y):
            dx = mouse_pos_x - self.player_pos_x
            dy = mouse_pos_y - self.player_pos_y
            angle = degrees(atan2(dy, dx))
            return angle if angle >= 0 else angle + 360

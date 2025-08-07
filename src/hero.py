from math import *

class Hero:
    def __init__(self, window_width, window_height, idle_animation, right_run_animation, left_run_animation, attack_animation):
        self.player_pos_x = window_width // 2
        self.player_pos_y = window_height // 2
        self.speed = 0.3
        self.attack_radius = 30
        self.blade_attack_damage = 10
        self.base_hp = 30
        self.base_mana = 60
        self.health = 30
        self.mana = 48
        self.state = "idle"

        self.idle_animation = idle_animation
        self.right_run_animation = right_run_animation
        self.left_run_animation = left_run_animation
        self.attack_animation = attack_animation
        self.texture = idle_animation.frames[0]


    def get_angle(self, mouse_pos_x, mouse_pos_y):
            dx = mouse_pos_x - self.player_pos_x
            dy = mouse_pos_y - self.player_pos_y
            angle = degrees(atan2(dy, dx))
            return angle if angle >= 0 else angle + 360

from pyray import *
from raylib import *
from random import *
from math import *

WIDTH = 666
HEIGHT = 666
PADDING = 30
ENEMIES = []
player_pos_x = WIDTH // 2
player_pos_y = HEIGHT // 2
player_speed = 0.5
ATTACK_RADIUS = 30
GUN_ATTACK_DAMAGE = 10

def check_border(X, Y, V_WIDTH, V_HEIGHT):
    if X > PADDING and X < V_WIDTH - PADDING and Y > PADDING and Y < V_HEIGHT - PADDING:
        return True
    return False

def generate_random_enemy():
    global ENEMIES

    pos_x = randint(0 + PADDING, WIDTH - PADDING)
    pos_y = randint(0 + PADDING, HEIGHT - PADDING)
    c = dict()
    c["pos_x"] = pos_x
    c["pos_y"] = pos_y
    c["health"] = 50
    ENEMIES.append(c)

def check_enemies():
    global ENEMIES, player_pos_y, player_pos_x

    for i in ENEMIES:
        if (player_pos_x - ATTACK_RADIUS < i["pos_x"] < player_pos_x + ATTACK_RADIUS and
            player_pos_y - ATTACK_RADIUS < i["pos_y"] < player_pos_y + ATTACK_RADIUS):
                        i["health"] -= GUN_ATTACK_DAMAGE
                        print(i["health"])
                        if i["health"] <= 0:
                            ENEMIES.remove(i)
                            return 0
                        return 1

init_window(WIDTH, HEIGHT, "vampire uber-killer")
floor_texture = load_texture_from_image(load_image("src/floor.png"))
hero_texture  = load_texture_from_image(load_image("src/hero.png"))

generate_random_enemy()
print(ENEMIES)

while not window_should_close():

    #key binds
    if is_key_down(KEY_RIGHT):
        if check_border(player_pos_x + player_speed, player_pos_y, WIDTH, HEIGHT):
            player_pos_x += player_speed
    if is_key_down(KEY_LEFT):
        if check_border(player_pos_x - player_speed, player_pos_y,  WIDTH, HEIGHT):
            player_pos_x -= player_speed
    if is_key_down(KEY_UP):
        if check_border(player_pos_x, player_pos_y - player_speed, WIDTH, HEIGHT):
            player_pos_y -= player_speed
    if is_key_down(KEY_DOWN):
        if check_border(player_pos_x, player_pos_y + player_speed, WIDTH, HEIGHT):
            player_pos_y += player_speed
    if is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
        print("nigger")
        check_enemies()

    #initing GUI
    begin_drawing()
    clear_background(WHITE)

    #rendering floor
    for x in range(0, WIDTH, floor_texture.width):
        for y in range(0, HEIGHT, floor_texture.height):
            draw_texture(floor_texture, x, y, WHITE)
    #rendering enemies
    for i in ENEMIES:
        pos_x = i["pos_x"]
        pos_y = i["pos_y"]
        draw_rectangle(pos_x, pos_y, 20, 20, BLACK)

    draw_texture(hero_texture, floor(player_pos_x), floor(player_pos_y), WHITE)
    draw_circle_lines(floor(player_pos_x), floor(player_pos_y), ATTACK_RADIUS, RED)
    draw_fps(10,10)

    end_drawing()
close_window()

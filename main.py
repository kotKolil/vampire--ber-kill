from raylib import *
from random import *
from math import *
from src.enemies import *

WIDTH = 666
HEIGHT = 666
PADDING = 30
ENEMIES = []
player_pos_x = WIDTH // 2
player_pos_y = HEIGHT // 2
player_speed = 0.3
ATTACK_RADIUS = 30
BLADE_ATTACK_DAMAGE = 10
MENU_ACTIVE = True
FLOOR_DROWN = False

def check_border(X, Y, V_WIDTH, V_HEIGHT):
    if X > PADDING and X < V_WIDTH - PADDING and Y > PADDING and Y < V_HEIGHT - PADDING:
        return True
    return False

def generate_random_enemy():
    c = RobotEnemy( randint(0 + PADDING, WIDTH - PADDING), randint(0 + PADDING, WIDTH - PADDING) )
    ENEMIES.append(c)


def check_enemies():



    global ENEMIES, player_pos_y, player_pos_x

    for i in ENEMIES:
        if abs(ceil(( (i.pos_x  - player_pos_x ) ** 2 + (i.pos_y- player_pos_y ) ** 2 ) ** 0.5)) < ATTACK_RADIUS:
            i.health-= BLADE_ATTACK_DAMAGE
            if i.health <= 0:
                ENEMIES.remove(i)
                return 0
            return 1

init_window(WIDTH, HEIGHT, "vampire uber-killer")
floor_texture = load_texture_from_image(load_image("resources/floor6.png"))
hero_texture  = load_texture_from_image(load_image("resources/hero.png"))
main_font = load_font("resources/alagard.ttf")

generate_random_enemy()
while not window_should_close():

    begin_drawing()
    clear_background(BLACK)

    #rendering main menu
    if MENU_ACTIVE:


        width, height =  measure_text_ex(main_font, "Vampire-uber-Killer", 20, 4).x, measure_text_ex(main_font, "Vampire-uber-Killer", 20, 4).y
        width1, height1 =  measure_text_ex(main_font, "press space to start", 10, 4).x, measure_text_ex(main_font, "press space to start", 10, 4).y

        draw_text_ex(main_font, "Vampire-uber-Killer", (WIDTH // 2 - width // 2, HEIGHT // 2 - height // 2), 20, 4,  GREEN)
        draw_text_ex(main_font, "press space to start", (WIDTH // 2 - width1 // 2, HEIGHT // 2 + height // 2) ,10, 4, GREEN)
        if is_key_down(KEY_SPACE):
            MENU_ACTIVE = False


    else:

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
            check_enemies()


        #rendering floor
        for x in range(0, WIDTH, floor_texture.width):
            for y in range(0, HEIGHT, floor_texture.height):
                draw_texture(floor_texture, x, y, WHITE)
            # print(FLOOR_DROWN)

        #rendering enemies
        for i in ENEMIES:
            # pos_x = i["pos_x"]
            # pos_y = i["pos_y"]
            # draw_texture(i["texture"], pos_x, pos_y, WHITE)
            draw_texture(i.texture, i.pos_x, i.pos_y, WHITE)

        draw_texture(hero_texture, floor(player_pos_x), floor(player_pos_y), WHITE)
        draw_circle_lines(floor(player_pos_x), floor(player_pos_y), ATTACK_RADIUS, RED)
        draw_fps(10,10)

    end_drawing()
close_window()

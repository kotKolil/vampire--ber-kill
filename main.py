from raylib import *
from random import *
from math import *
from src.enemies import *
from src.hero import *
from src.animation import *

WIDTH = 666
HEIGHT = 666
PADDING = 30
DEBUG = False
ENEMIES = []
IS_ATTACK = False

MENU_ACTIVE = True

def check_border(X, Y, V_WIDTH, V_HEIGHT):
    if X > PADDING and X < V_WIDTH - PADDING and Y > PADDING and Y < V_HEIGHT - PADDING:
        return True
    return False

def generate_random_enemy():
    c = RobotEnemy( randint(0 + PADDING, WIDTH - PADDING), randint(0 + PADDING, WIDTH - PADDING) )
    ENEMIES.append(c)


def check_enemies_on_damage():

    global ENEMIES

    for i in ENEMIES:
        # if ceil(( (i.pos_x + i.texture.width // 2  - hero.player_pos_x ) ** 2 + (i.pos_y + i.texture.height // 2 - hero.player_pos_y ) ** 2 ) ** 0.5) < hero.attack_radius or \
        #     ceil(( (i.pos_x - i.texture.width // 2  - hero.player_pos_x ) ** 2 + (i.pos_y - i.texture.height // 2 - hero.player_pos_y ) ** 2 ) ** 0.5) < hero.attack_radius:
        if (i.pos_x - i.texture.width // 2 - hero.attack_radius <= hero.player_pos_x <= i.pos_x + i.texture.width // 2 + hero.attack_radius) and (i.pos_y - i.texture.height // 2  - hero.attack_radius <= hero.player_pos_y <= i.pos_y + i.texture.height // 2 + hero.attack_radius):
            i.health-= hero.blade_attack_damage
            if i.health <= 0:
                ENEMIES.remove(i)
                return 0
            return 1

init_window(WIDTH, HEIGHT, "vampire uber-killer")
floor_texture = load_texture_from_image(load_image("resources/floor6.png"))
hero_texture  = load_texture_from_image(load_image("resources/hero3.png"))
main_font = load_font("resources/alagard.ttf")

hero_idle_animation = Animation("resources/hero/idle", 3)
hero_run_animation = Animation("resources/hero/right_run", 3)
hero_left_animation = Animation("resources/hero/left_run", 3)
attack_animation = Animation("resources/hero/attack", 9)
hero = Hero(WIDTH, HEIGHT, hero_idle_animation, hero_run_animation, hero_left_animation, attack_animation)

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

        hero.state = "idle"
        #key binds
        if is_key_down(KEY_RIGHT) or is_key_down(KEY_D):
            if check_border(hero.player_pos_x + hero.speed, hero.player_pos_y, WIDTH, HEIGHT):
                hero.state = "right_run"
                hero.player_pos_x += hero.speed
        if is_key_down(KEY_LEFT) or is_key_down(KEY_A):
            if check_border(hero.player_pos_x - hero.speed, hero.player_pos_y,  WIDTH, HEIGHT):
                hero.state = "left_run"
                hero.player_pos_x -= hero.speed
        if is_key_down(KEY_UP) or is_key_down(KEY_W):
            if check_border(hero.player_pos_x, hero.player_pos_y - hero.speed, WIDTH, HEIGHT):
                hero.state = "left_run"
                hero.player_pos_y -= hero.speed
        if is_key_down(KEY_DOWN) or is_key_down(KEY_S):
            if check_border(hero.player_pos_x, hero.player_pos_y + hero.speed, WIDTH, HEIGHT):
                hero.state = "right_run"
                hero.player_pos_y += hero.speed

        if is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
            IS_ATTACK = True
            check_enemies_on_damage()


        #rendering floor
        for x in range(0, WIDTH, floor_texture.width):
            for y in range(0, HEIGHT, floor_texture.height):
                draw_texture(floor_texture, x, y, WHITE)

        #rendering enemies
        for i in ENEMIES:
            draw_texture(i.texture, i.pos_x, i.pos_y, WHITE)

        #running AI scripts
        for i in ENEMIES:
            i.ai_script(hero)

        #rendering health bar
        draw_text_ex(main_font, f"HP {hero.health}", (WIDTH - 60 , 10), 15, 4, GREEN)

        #rendering debug info
        if DEBUG:
            draw_text_ex(main_font, f"fps: {get_fps()}", (10, 10), 15, 4, GREEN)
            draw_text_ex(main_font, f"player x:{ceil(hero.player_pos_x)} y:{ceil(hero.player_pos_y)} angle:{ceil(hero.get_angle(get_mouse_x(), get_mouse_y()))} IS_ATTACK {IS_ATTACK}", (10, 40), 15, 4, GREEN)
            draw_text_ex(main_font, f"mouse x:{ceil(get_mouse_x())} y:{ceil(get_mouse_y())}", (10, 70), 15, 4, GREEN)
            draw_circle_lines(floor(hero.player_pos_x + hero_texture.width // 2 ), floor(hero.player_pos_y + hero_texture.height // 2), hero.attack_radius, RED)


        if IS_ATTACK:
            draw_texture(
                        hero.attack_animation.get_current_frame(get_fps()),
                        floor( hero.player_pos_x), floor(hero.player_pos_y),
                        WHITE
                    )
            if hero.attack_animation.current_frame == 9:
                hero.attack_animation.current_frame = 0
                IS_ATTACK = False

        else:
            match hero.state:
                case "idle":
                    draw_texture(hero.idle_animation.get_current_frame(get_fps()),
                        floor( hero.player_pos_x), floor(hero.player_pos_y),
                        WHITE
                    )
                case "right_run":
                    draw_texture(
                        hero.right_run_animation.get_current_frame(get_fps()),
                        floor( hero.player_pos_x), floor(hero.player_pos_y),
                        WHITE
                    )
                case "left_run":
                    draw_texture(
                        hero.left_run_animation.get_current_frame(get_fps()),
                        floor( hero.player_pos_x), floor(hero.player_pos_y),
                        WHITE
                    )

    end_drawing()
close_window()

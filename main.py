from raylib import *
from src.enemies import *
from src.animation import *
from src.spell import *
import importlib, inspect
import audioread

WIDTH = 666
HEIGHT = 666
PADDING = 30
DEBUG = False
ENEMIES = []
IS_ATTACK = False
HP_BAR_WIDTH = 200
AI = True
MUSIC_START = time()
MAIN_MUSIC_THEME = "resources/audio/Between Levels.ogg"
CURRENT_MUSIC_PATH = MAIN_MUSIC_THEME
CURRENT_MUSIC_INFO = audioread.audio_open(CURRENT_MUSIC_PATH)

DEATH_MUSIC = "resources/audio/death.ogg"
DEATH_MUSIC_INFO = audioread.audio_open(DEATH_MUSIC)

SWITCH_SOUND = load_sound("resources/audio/switch.ogg")

MENU_ACTIVE = True
PAUSE = False
SPELLS_MENU = False

def check_border(X, Y, V_WIDTH, V_HEIGHT):
    if X > PADDING and X < V_WIDTH - PADDING and Y > PADDING and Y < V_HEIGHT - PADDING:
        return True
    return False

def get_element_index(arr, element):
    for i in range(len(arr)):
        if arr[i] == element:
            return i
    return None

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
                generate_random_enemy()
                if not (hero.base_hp < hero.health + i.base_hp // 4):
                    hero.health += i.base_hp // 4
                return 0
            return 1

init_window(WIDTH, HEIGHT, "vampire uber-killer")
init_audio_device()
set_window_state(FLAG_WINDOW_TOPMOST)
set_exit_key(KEY_Q)
set_target_fps(60)
floor_texture = load_texture_from_image(load_image("resources/floor6.png"))
hero_texture  = load_texture_from_image(load_image("resources/hero3.png"))
main_font = load_font("resources/alagard.ttf")

CURRENT_MUSIC = load_sound(CURRENT_MUSIC_PATH)
CURRENT_MUSIC_INFO = CURRENT_MUSIC_INFO
sword_sound = load_sound("resources/audio/sword.ogg")
c = load_sound("resources/death.ogg")

hero_idle_animation = Animation("resources/hero/idle", 3)
hero_run_animation = Animation("resources/hero/right_run", 3)
hero_left_animation = Animation("resources/hero/left_run", 3)
attack_animation = Animation("resources/hero/attack", 9)
death_animation = Animation('resources/hero/death', 9)
hero = Hero(WIDTH, HEIGHT, hero_idle_animation, hero_run_animation, hero_left_animation, attack_animation,
            death_animation)


spells = [ cls(hero, ENEMIES) for name, cls in inspect.getmembers(importlib.import_module("src.spell"), inspect.isclass) if cls.__module__ == 'src.spell' ][1:]
hero.current_spell = spells[0]
play_sound(CURRENT_MUSIC)
generate_random_enemy()
while not window_should_close():

    if time() - MUSIC_START > CURRENT_MUSIC_INFO.duration:
        MUSIC_START = time()
        play_sound(CURRENT_MUSIC)



    begin_drawing()
    clear_background(BLACK)

    if hero.health <= 0:
        if CURRENT_MUSIC_PATH != DEATH_MUSIC:
            CURRENT_MUSIC_PATH = DEATH_MUSIC
            stop_sound(CURRENT_MUSIC)
            CURRENT_MUSIC = load_sound(DEATH_MUSIC)
            CURRENT_MUSIC_INFO = DEATH_MUSIC_INFO
            MUSIC_START = time()
            play_sound(CURRENT_MUSIC)
        if hero.death_animation.current_frame < 18:
            draw_texture(hero.death_animation.get_current_frame(get_fps()),
                floor( hero.player_pos_x), floor(hero.player_pos_y),
                WHITE
            )

        else:
            width, height =  measure_text_ex(main_font, "Game Over. Press q to quit", 20, 4).x, measure_text_ex(main_font, "Game Over. Press q to quit", 20, 4).y
            draw_text_ex(main_font, "Game Over. Press q to quit", (WIDTH // 2 - width // 2, HEIGHT // 2 - height // 2), 20, 4,  GREEN)

    #rendering main menu
    elif MENU_ACTIVE:


        width, height =  measure_text_ex(main_font, "Vampire-uber-Killer", 20, 4).x, measure_text_ex(main_font, "Vampire-uber-Killer", 20, 4).y
        width1, height1 =  measure_text_ex(main_font, "press space to start", 10, 4).x, measure_text_ex(main_font, "press space to start", 10, 4).y

        draw_text_ex(main_font, "Vampire-uber-Killer", (WIDTH // 2 - width // 2, HEIGHT // 2 - height // 2), 20, 4,  GREEN)
        draw_text_ex(main_font, "press space to start", (WIDTH // 2 - width1 // 2, HEIGHT // 2 + height // 2) ,10, 4, GREEN)
        if is_key_down(KEY_SPACE):
            MENU_ACTIVE = False


    elif SPELLS_MENU:
        #game on pause

        #rendering floor
        for x in range(0, WIDTH, floor_texture.width):
            for y in range(0, HEIGHT, floor_texture.height):
                draw_texture(floor_texture, x, y, WHITE)

        #rendering enemies
        for i in ENEMIES:
            draw_texture(i.texture, floor(i.pos_x), floor(i.pos_y), WHITE)

        #rendering health bar
        draw_rectangle(WIDTH - HP_BAR_WIDTH - 10, 0 + 5, HP_BAR_WIDTH, 10, WHITE)
        draw_rectangle(WIDTH - HP_BAR_WIDTH - 10, 0 + 5, ceil(HP_BAR_WIDTH * (hero.health / hero.base_hp)), 10, RED)
        #rendering mana bar
        draw_rectangle(WIDTH - HP_BAR_WIDTH - 10, 0 + 25, HP_BAR_WIDTH, 10, WHITE)
        draw_rectangle(WIDTH - HP_BAR_WIDTH - 10, 0 + 25, ceil(HP_BAR_WIDTH * (hero.mana / hero.base_mana)), 10, BLUE)

        #rendering debug info
        if DEBUG:
            draw_text_ex(main_font, f"fps: {get_fps()}", (10, 10), 15, 4, GREEN)
            draw_text_ex(main_font, f"player x:{ceil(hero.player_pos_x)} y:{ceil(hero.player_pos_y)} angle:{ceil(hero.get_angle(get_mouse_x(), get_mouse_y()))} IS_ATTACK {IS_ATTACK}", (10, 40), 15, 4, GREEN)
            draw_text_ex(main_font, f"mouse x:{ceil(get_mouse_x())} y:{ceil(get_mouse_y())}", (10, 70), 15, 4, GREEN)
            draw_circle_lines(floor(hero.player_pos_x + hero_texture.width // 2 ), floor(hero.player_pos_y + hero_texture.height // 2), hero.attack_radius, RED)

        if is_key_down(KEY_ESCAPE):
            SPELLS_MENU = False


        #rendering hero
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

        #rendering spell menu
        draw_rectangle(0, HEIGHT - 100, WIDTH, 300, BLACK)
        draw_texture(hero.current_spell.icon, 30, HEIGHT - hero.current_spell.icon.height - 30, WHITE)
        draw_texture(hero.current_spell.icon, 30, HEIGHT - hero.current_spell.icon.height - 30, WHITE)
        width, height =  measure_text_ex(main_font, hero.current_spell.name, 20, 4).x, measure_text_ex(main_font, spells[0].name, 20, 4).y
        draw_text_ex(main_font, hero.current_spell.name, (WIDTH // 2 - width // 2, HEIGHT  - 100), 20, 4,  GREEN)
        width, height =  measure_text_ex(main_font, hero.current_spell.description, 14, 4).x, measure_text_ex(main_font, hero.current_spell.description, 14, 4).y
        draw_text_ex(main_font, hero.current_spell.description, (hero.current_spell.icon.width + 50, HEIGHT  - 50 - height), 14, 4,  GREEN)

        if is_key_pressed(KEY_ESCAPE):
            SPELLS_MENU = False
        if is_key_pressed(KEY_RIGHT):
            play_sound(SWITCH_SOUND)
            if get_element_index(spells, hero.current_spell) < len(spells) - 1:
                hero.current_spell = spells[1 + get_element_index(spells, hero.current_spell)]
        if is_key_pressed(KEY_LEFT):
            play_sound(SWITCH_SOUND)
            if get_element_index(spells, hero.current_spell) > 0:
                hero.current_spell = spells[get_element_index(spells, hero.current_spell) - 1]

    elif PAUSE:
            width, height =  measure_text_ex(main_font, "pause", 20, 4).x, measure_text_ex(main_font, "pause", 20, 4).y
            draw_text_ex(main_font, "pause", (WIDTH // 2 - width // 2, HEIGHT // 2 - height // 2), 20, 4,  GREEN)
            if is_key_pressed(KEY_ESCAPE):
                PAUSE = False
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
        if is_key_pressed(KEY_ESCAPE):
                PAUSE = True
        if is_key_pressed(KEY_TAB):
                SPELLS_MENU = True
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
            if hero.mana - hero.current_spell.mana_count >= 0:
                hero.mana -= hero.current_spell.mana_count
                hero.current_spell.script()
                hero.current_spell.long_script_start = time()
        #hiting enemies
        if is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
            play_sound(sword_sound)
            IS_ATTACK = True
            check_enemies_on_damage()


        #rendering floor
        for x in range(0, WIDTH, floor_texture.width):
            for y in range(0, HEIGHT, floor_texture.height):
                draw_texture(floor_texture, x, y, WHITE)

        #rendering enemies
        for i in ENEMIES:
            draw_texture(i.texture, floor(i.pos_x), floor(i.pos_y), WHITE)

        #running AI scripts
        if AI:
            for i in ENEMIES:
                i.ai_script(hero)

        #rendering health bar
        draw_rectangle(WIDTH - HP_BAR_WIDTH - 10, 0 + 5, HP_BAR_WIDTH, 10, WHITE)
        draw_rectangle(WIDTH - HP_BAR_WIDTH - 10, 0 + 5, ceil(HP_BAR_WIDTH * (hero.health / hero.base_hp)), 10, RED)
        #rendering mana bar
        draw_rectangle(WIDTH - HP_BAR_WIDTH - 10, 0 + 25, HP_BAR_WIDTH, 10, WHITE)
        draw_rectangle(WIDTH - HP_BAR_WIDTH - 10, 0 + 25, ceil(HP_BAR_WIDTH * (hero.mana / hero.base_mana)), 10, BLUE)

        #rendering debug info
        if DEBUG:
            draw_text_ex(main_font, f"fps: {get_fps()}", (10, 10), 15, 4, GREEN)
            draw_text_ex(main_font, f"player x:{ceil(hero.player_pos_x)} y:{ceil(hero.player_pos_y)} angle:{ceil(hero.get_angle(get_mouse_x(), get_mouse_y()))} IS_ATTACK {IS_ATTACK}", (10, 40), 15, 4, GREEN)
            draw_text_ex(main_font, f"mouse x:{ceil(get_mouse_x())} y:{ceil(get_mouse_y())}", (10, 70), 15, 4, GREEN)
            draw_text_ex(main_font, f"spell {hero.current_spell}", (10, 100), 15, 4, GREEN)
            draw_circle_lines(floor(hero.player_pos_x + hero_texture.width // 2 ), floor(hero.player_pos_y + hero_texture.height // 2), hero.attack_radius, RED)


        #rendering hero
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

        if hero.current_spell.long_script_start + hero.current_spell.long_script_time > time()  and \
                hero.current_spell.long_script_start != 0:
                    hero.current_spell.long_script()
                    hero.current_spell.spell_animation(get_fps())
        else:
            hero.current_spell.long_script_start = 0

    end_drawing()
close_window()

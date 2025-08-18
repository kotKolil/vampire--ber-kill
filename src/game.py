from raylib import *
from src.enemies import *
from src.spell import *
import importlib, inspect
import audioread
from time import time
from random import randint

class Game:

    def __init__(self):
        self.WIDTH = 666
        self.HEIGHT = 666
        self.PADDING = 30
        self.DEBUG = True
        self.ENEMIES = []
        self.PARTICLES = []
        self.MANA_SPEED = 0.05
        self.IS_ATTACK = False
        self.HP_BAR_WIDTH = 200
        self.AI = True
        self.MUSIC_START = time()
        self.MAIN_MUSIC_THEME = "resources/audio/Between Levels.ogg"
        self.CURRENT_MUSIC_PATH = self.MAIN_MUSIC_THEME
        self.CURRENT_MUSIC_INFO = audioread.audio_open(self.CURRENT_MUSIC_PATH)

        self.DEATH_MUSIC = "resources/audio/death.ogg"
        self.DEATH_MUSIC_INFO = audioread.audio_open(self.DEATH_MUSIC)

        self.SWITCH_SOUND = load_sound("resources/audio/switch.ogg")

        self.MENU_ACTIVE = True
        self.PAUSE = False
        self.SPELLS_MENU = False

        init_window(self.WIDTH, self.HEIGHT, "vampire uber-killer")
        init_audio_device()
        set_window_state(FLAG_WINDOW_TOPMOST)
        set_exit_key(KEY_Q)
        set_target_fps(60)
        self.floor_texture = load_texture_from_image(load_image("resources/floor6.png"))
        self.main_font = load_font("resources/alagard.ttf")

        self.CURRENT_MUSIC = load_sound(self.CURRENT_MUSIC_PATH)
        self.sword_sound = load_sound("resources/audio/sword.ogg")


        self.hero = Hero(self.WIDTH, self.HEIGHT)
        self.spells = [cls(self) for name, cls in inspect.getmembers(importlib.import_module("src.spell"), inspect.isclass) if cls.__module__ == 'src.spell'][1:]
        self.hero.current_spell = self.spells[0]
        play_sound(self.CURRENT_MUSIC)

    def check_border(self, X, Y, V_WIDTH, V_HEIGHT):
        if X > self.PADDING and X < V_WIDTH - self.PADDING and Y > self.PADDING and Y < V_HEIGHT - self.PADDING:
            return True
        return False

    def get_element_index(self, arr, element):
        for i in range(len(arr)):
            if arr[i] == element:
                return i
        return None

    def generate_random_enemy(self):
        c = RobotEnemy(randint(0 + self.PADDING, self.WIDTH - self.PADDING),
                       randint(0 + self.PADDING, self.HEIGHT - self.PADDING))
        self.ENEMIES.append(c)

    def check_enemies_on_damage(self):
        for i in self.ENEMIES[:]:
            if ((i.pos_x - i.texture.width // 2 - self.hero.attack_radius <= self.hero.player_pos_x <= i.pos_x + i.texture.width // 2 + self.hero.attack_radius)
                and (i.pos_y - i.texture.height // 2 - self.hero.attack_radius <= self.hero.player_pos_y <= i.pos_y + i.texture.height // 2 + self.hero.attack_radius)):
                i.health -= self.hero.blade_attack_damage
                if i.health <= 0:
                    self.ENEMIES.remove(i)
                    self.generate_random_enemy()
                    self.generate_random_enemy()
                    self.hero.health = min(self.hero.base_hp, self.hero.health + i.base_hp // 4)
                    return 0
                return 1

    def main_loop(self):
        self.generate_random_enemy()
        while not window_should_close():
            current_time = time()
            if current_time - self.MUSIC_START > self.CURRENT_MUSIC_INFO.duration:
                self.MUSIC_START = current_time
                play_sound(self.CURRENT_MUSIC)

            if self.hero.base_mana >= self.hero.mana:
                self.hero.mana += self.MANA_SPEED

            begin_drawing()
            clear_background(BLACK)

            if self.hero.health <= 0:
                if self.CURRENT_MUSIC_PATH != self.DEATH_MUSIC:
                    self.CURRENT_MUSIC_PATH = self.DEATH_MUSIC
                    stop_sound(self.CURRENT_MUSIC)
                    self.CURRENT_MUSIC = load_sound(self.DEATH_MUSIC)
                    self.CURRENT_MUSIC_INFO = self.DEATH_MUSIC_INFO
                    self.MUSIC_START = current_time
                    play_sound(self.CURRENT_MUSIC)
                if self.hero.death_animation.current_frame < 18:
                    draw_texture(self.hero.death_animation.get_current_frame(get_fps()),
                        floor(self.hero.player_pos_x), floor(self.hero.player_pos_y),
                        WHITE
                    )
                else:
                    text = "Game Over. Press q to quit"
                    text_size = measure_text_ex(self.main_font, text, 20, 4)
                    draw_text_ex(self.main_font, text,
                                (self.WIDTH // 2 - text_size.x // 2, self.HEIGHT // 2 - text_size.y // 2),
                                20, 4, GREEN)

            elif self.MENU_ACTIVE:
                title = "Vampire-uber-Killer"
                prompt = "press space to start"

                title_size = measure_text_ex(self.main_font, title, 20, 4)
                prompt_size = measure_text_ex(self.main_font, prompt, 10, 4)

                draw_text_ex(self.main_font, title,
                            (self.WIDTH // 2 - title_size.x // 2, self.HEIGHT // 2 - title_size.y // 2),
                            20, 4, GREEN)
                draw_text_ex(self.main_font, prompt,
                            (self.WIDTH // 2 - prompt_size.x // 2, self.HEIGHT // 2 + prompt_size.y),
                            10, 4, GREEN)
                if is_key_down(KEY_SPACE):
                    self.MENU_ACTIVE = False

            elif self.SPELLS_MENU:
                for x in range(0, self.WIDTH, self.floor_texture.width):
                    for y in range(0, self.HEIGHT, self.floor_texture.height):
                        draw_texture(self.floor_texture, x, y, WHITE)

                for i in self.ENEMIES:
                    draw_texture(i.texture, floor(i.pos_x), floor(i.pos_y), WHITE)

                draw_rectangle(self.WIDTH - self.HP_BAR_WIDTH - 10, 5, self.HP_BAR_WIDTH, 10, WHITE)
                draw_rectangle(self.WIDTH - self.HP_BAR_WIDTH - 10, 5,
                              ceil(self.HP_BAR_WIDTH * (self.hero.health / self.hero.base_hp)),
                              10, RED)
                draw_rectangle(self.WIDTH - self.HP_BAR_WIDTH - 10, 25, self.HP_BAR_WIDTH, 10, WHITE)
                draw_rectangle(self.WIDTH - self.HP_BAR_WIDTH - 10, 25,
                              ceil(self.HP_BAR_WIDTH * (self.hero.mana / self.hero.base_mana)),
                              10, BLUE)

                if self.DEBUG:
                    fps_text = f"fps: {get_fps()}"
                    pos_text = f"player x:{ceil(self.hero.player_pos_x)} y:{ceil(self.hero.player_pos_y)}"
                    mouse_text = f"mouse x:{ceil(get_mouse_x())} y:{ceil(get_mouse_y())}"

                    draw_text_ex(self.main_font, fps_text, (10, 10), 15, 4, GREEN)
                    draw_text_ex(self.main_font, pos_text, (10, 40), 15, 4, GREEN)
                    draw_text_ex(self.main_font, mouse_text, (10, 70), 15, 4, GREEN)

                    if len(self.hero.idle_animation.frames) > 0:
                        hero_tex = self.hero.idle_animation.frames[0]
                        draw_circle_lines(
                            floor(self.hero.player_pos_x + hero_tex.width // 2),
                            floor(self.hero.player_pos_y + hero_tex.height // 2),
                            self.hero.attack_radius, RED
                        )

                if self.IS_ATTACK:
                    draw_texture(
                        self.hero.attack_animation.get_current_frame(get_fps()),
                        floor(self.hero.player_pos_x), floor(self.hero.player_pos_y),
                        WHITE
                    )
                    if self.hero.attack_animation.current_frame == 9:
                        self.hero.attack_animation.current_frame = 0
                        self.IS_ATTACK = False
                else:
                    if self.hero.state == "idle":
                        draw_texture(self.hero.idle_animation.get_current_frame(get_fps()),
                            floor(self.hero.player_pos_x), floor(self.hero.player_pos_y),
                            WHITE
                        )
                    elif self.hero.state == "right_run":
                        draw_texture(
                            self.hero.right_run_animation.get_current_frame(get_fps()),
                            floor(self.hero.player_pos_x), floor(self.hero.player_pos_y),
                            WHITE
                        )
                    elif self.hero.state == "left_run":
                        draw_texture(
                            self.hero.left_run_animation.get_current_frame(get_fps()),
                            floor(self.hero.player_pos_x), floor(self.hero.player_pos_y),
                            WHITE
                        )

                draw_rectangle(0, self.HEIGHT - 100, self.WIDTH, 100, BLACK)
                draw_texture(self.hero.current_spell.icon, 30, self.HEIGHT - self.hero.current_spell.icon.height - 30, WHITE)

                name_size = measure_text_ex(self.main_font, self.hero.current_spell.name, 20, 4)
                draw_text_ex(self.main_font, self.hero.current_spell.name,
                            (self.WIDTH // 2 - name_size.x // 2, self.HEIGHT - 100),
                            20, 4, GREEN)

                desc_size = measure_text_ex(self.main_font, self.hero.current_spell.description, 14, 4)
                draw_text_ex(self.main_font, self.hero.current_spell.description,
                            (self.hero.current_spell.icon.width + 50,
                             self.HEIGHT - 80 + (20 - desc_size.y) // 2),
                            14, 4, GREEN)

                if is_key_pressed(KEY_ESCAPE):
                    self.SPELLS_MENU = False
                if is_key_pressed(KEY_RIGHT):
                    play_sound(self.SWITCH_SOUND)
                    idx = self.get_element_index(self.spells, self.hero.current_spell)
                    if idx is not None and idx < len(self.spells) - 1:
                        self.hero.current_spell = self.spells[idx + 1]
                if is_key_pressed(KEY_LEFT):
                    play_sound(self.SWITCH_SOUND)
                    idx = self.get_element_index(self.spells, self.hero.current_spell)
                    if idx is not None and idx > 0:
                        self.hero.current_spell = self.spells[idx - 1]

            elif self.PAUSE:
                text = "pause"
                text_size = measure_text_ex(self.main_font, text, 20, 4)
                draw_text_ex(self.main_font, text,
                            (self.WIDTH // 2 - text_size.x // 2, self.HEIGHT // 2 - text_size.y // 2),
                            20, 4, GREEN)
                if is_key_pressed(KEY_ESCAPE):
                    self.PAUSE = False

            else:
                self.hero.state = "idle"
                if is_key_down(KEY_RIGHT) or is_key_down(KEY_D):
                    if self.check_border(self.hero.player_pos_x + self.hero.speed, self.hero.player_pos_y, self.WIDTH, self.HEIGHT):
                        self.hero.state = "right_run"
                        self.hero.player_pos_x += self.hero.speed
                if is_key_down(KEY_LEFT) or is_key_down(KEY_A):
                    if self.check_border(self.hero.player_pos_x - self.hero.speed, self.hero.player_pos_y, self.WIDTH, self.HEIGHT):
                        self.hero.state = "left_run"
                        self.hero.player_pos_x -= self.hero.speed
                if is_key_down(KEY_UP) or is_key_down(KEY_W):
                    if self.check_border(self.hero.player_pos_x, self.hero.player_pos_y - self.hero.speed, self.WIDTH, self.HEIGHT):
                        self.hero.player_pos_y -= self.hero.speed
                if is_key_down(KEY_DOWN) or is_key_down(KEY_S):
                    if self.check_border(self.hero.player_pos_x, self.hero.player_pos_y + self.hero.speed, self.WIDTH, self.HEIGHT):
                        self.hero.player_pos_y += self.hero.speed

                if is_key_pressed(KEY_ESCAPE):
                    self.PAUSE = True
                if is_key_pressed(KEY_TAB):
                    self.SPELLS_MENU = True

                if is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
                    if self.hero.mana >= self.hero.current_spell.mana_count:
                        self.hero.mana -= self.hero.current_spell.mana_count
                        self.hero.current_spell.script()
                        self.hero.current_spell.long_script_start = time()

                if is_mouse_button_pressed(MOUSE_BUTTON_RIGHT) and self.hero.attack_animation.current_frame == 0:
                    play_sound(self.sword_sound)
                    self.IS_ATTACK = True
                    self.check_enemies_on_damage()

                for x in range(0, self.WIDTH, self.floor_texture.width):
                    for y in range(0, self.HEIGHT, self.floor_texture.height):
                        draw_texture(self.floor_texture, x, y, WHITE)

                for i in self.ENEMIES:
                    draw_texture(i.texture, floor(i.pos_x), floor(i.pos_y), WHITE)

                if self.AI:
                    for i in self.ENEMIES[:]:
                        if i.health <= 0:
                            self.ENEMIES.remove(i)
                            continue
                        i.ai_script(self.hero)

                for particle in self.PARTICLES[:]:
                    if (current_time - particle.born_time >= particle.lifetime) \
                            or particle.x < 0 or particle.y < 0 \
                            or particle.x > self.WIDTH or particle.y > self.HEIGHT:
                        self.PARTICLES.remove(particle)
                        continue

                    collided = False
                    for enemy in self.ENEMIES:
                        if ((enemy.pos_x - enemy.texture.width // 2 - 3 <= particle.x <= enemy.pos_x + enemy.texture.width // 2 + 3)
                            and (enemy.pos_y - enemy.texture.height // 2 - 3 <= particle.y <= enemy.pos_y + enemy.texture.height // 2 + 3)):
                            particle.collide_script(enemy)
                            self.PARTICLES.remove(particle)
                            break

                    draw_texture(particle.animation.get_current_frame(get_fps()),
                                 floor(particle.x),
                                 floor(particle.y),
                                 WHITE)
                    particle.x += particle.speed * particle.dx
                    particle.y += particle.speed * particle.dy

                draw_rectangle(self.WIDTH - self.HP_BAR_WIDTH - 10, 5, self.HP_BAR_WIDTH, 10, WHITE)
                draw_rectangle(self.WIDTH - self.HP_BAR_WIDTH - 10, 5,
                              ceil(self.HP_BAR_WIDTH * (self.hero.health / self.hero.base_hp)),
                              10, RED)
                draw_rectangle(self.WIDTH - self.HP_BAR_WIDTH - 10, 25, self.HP_BAR_WIDTH, 10, WHITE)
                draw_rectangle(self.WIDTH - self.HP_BAR_WIDTH - 10, 25,
                              ceil(self.HP_BAR_WIDTH * (self.hero.mana / self.hero.base_mana)),
                              10, BLUE)

                if self.DEBUG:
                    fps_text = f"fps: {get_fps()}"
                    pos_text = f"player x:{ceil(self.hero.player_pos_x)} y:{ceil(self.hero.player_pos_y)}"
                    mouse_text = f"mouse x:{ceil(get_mouse_x())} y:{ceil(get_mouse_y())}"
                    spell_text = f"spell {self.hero.current_spell.name}"

                    draw_text_ex(self.main_font, fps_text, (10, 10), 15, 4, GREEN)
                    draw_text_ex(self.main_font, pos_text, (10, 40), 15, 4, GREEN)
                    draw_text_ex(self.main_font, mouse_text, (10, 70), 15, 4, GREEN)
                    draw_text_ex(self.main_font, spell_text, (10, 100), 15, 4, GREEN)
                    draw_text_ex(self.main_font, str(len(self.ENEMIES)), (10, 120), 15, 4, GREEN)

                    if len(self.hero.idle_animation.frames) > 0:
                        hero_tex = self.hero.idle_animation.frames[0]
                        draw_circle_lines(
                            floor(self.hero.player_pos_x + hero_tex.width // 2),
                            floor(self.hero.player_pos_y + hero_tex.height // 2),
                            self.hero.attack_radius, RED
                        )

                if self.IS_ATTACK:
                    draw_texture(
                        self.hero.attack_animation.get_current_frame(get_fps()),
                        floor(self.hero.player_pos_x), floor(self.hero.player_pos_y),
                        WHITE
                    )
                    if self.hero.attack_animation.current_frame >= 9:
                        self.hero.attack_animation.current_frame = 0
                        self.IS_ATTACK = False
                else:
                    if self.hero.state == "idle":
                        draw_texture(self.hero.idle_animation.get_current_frame(get_fps()),
                            floor(self.hero.player_pos_x), floor(self.hero.player_pos_y),
                            WHITE
                        )
                    elif self.hero.state == "right_run":
                        draw_texture(
                            self.hero.right_run_animation.get_current_frame(get_fps()),
                            floor(self.hero.player_pos_x), floor(self.hero.player_pos_y),
                            WHITE
                        )
                    elif self.hero.state == "left_run":
                        draw_texture(
                            self.hero.left_run_animation.get_current_frame(get_fps()),
                            floor(self.hero.player_pos_x), floor(self.hero.player_pos_y),
                            WHITE
                        )
                    elif self.hero.state == "damaged":
                        draw_texture(
                            self.hero.damage_animation.get_current_frame(get_fps()),
                            floor(self.hero.player_pos_x), floor(self.hero.player_pos_y),
                            WHITE
                        )
                if (self.hero.current_spell.long_script_start > 0
                    and current_time < self.hero.current_spell.long_script_start + self.hero.current_spell.long_script_time):
                    self.hero.current_spell.long_script()
                    self.hero.current_spell.spell_animation(get_fps())
                else:
                    self.hero.current_spell.long_script_start = 0

            end_drawing()
        close_window()
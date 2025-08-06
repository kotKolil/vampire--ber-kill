from os import listdir
from os.path import isfile, join
from pyray import *

class Animation:

    def __init__(self, frames, frame_speed):
        frames_list = [join(frames, f) for f in listdir(frames) if isfile(join(frames, f))]
        self.frames = [ load_texture_from_image(load_image(i)) for i in frames_list]
        self.frames_counter = 0
        self.frame_speed = frame_speed
        self.current_frame = 0


    def get_current_frame(self, fps_num):
        self.frames_counter += 1
        if self.frames_counter >= (fps_num / self.frame_speed):
            self.frames_counter = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.current_frame = 0
        return self.frames[self.current_frame]


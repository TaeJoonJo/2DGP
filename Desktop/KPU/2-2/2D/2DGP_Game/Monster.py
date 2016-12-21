import random

from pico2d import *

class Monster:
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 30.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 2

    image = None

    Sound = None

    def __init__(self):
        self.frame = 0
        self.total_frames = 0.0
        self.sizex, self.sizey = 20, 20
        self.x = 850
        self.y = 70
        if Monster.image == None:
            Monster.image = load_image('dongle.png')
        if (Monster.Sound == None):
            Monster.Sound = load_wav('star_get.wav')
            Monster.Sound.set_volume(40)
    def update(self, frame_time, isnext):
        self.total_frames += Monster.FRAMES_PER_ACTION * Monster.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 6
        dir = 1
        if(isnext is True):
            dir = 1.5
        distance = Monster.RUN_SPEED_PPS * frame_time * dir
        self.x -= distance

    def draw(self):
        self.image.clip_draw(self.frame* 16, 0, 16, 16, self.x, self.y, 40, 40)

    def get_bb(self):
        return self.x - self.sizex, self.y - self.sizey, self.x + self.sizex, self.y + self.sizey

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

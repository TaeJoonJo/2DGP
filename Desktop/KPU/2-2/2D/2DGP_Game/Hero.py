import random

from pico2d import *

class Hero:
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 30.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3

    image = None
    RIGHT_RUN_image = None
    LEFT_RUN_image = None
    RIGHT_STAND_image = None
    LEFT_STAND_image = None

    RIGHT_RUN = 1               #Boy's Move
    LEFT_RUN = 2
    RIGHT_STAND = 3
    LEFT_STAND = 4
    JUMP = 5

    def __init__(self):
        self.x, self.y = 0, 100
        self.sizex, self.sizey = 25, 50
        self.dir = 0
        self.frame = 0
        self.total_frames = 0.0
        self.state = self.RIGHT_STAND
        self.ismove = False
        self.isjump = False
        self.isreach = False
        self.isNext = False
        #self.Hp = None

        self.Hp = [Hero_Hp(i) for i in range(5)]
        self.Hpnum = 5

        if Hero.RIGHT_RUN_image == None:
            Hero.RIGHT_RUN_image = load_image('CH_RIGHT_RUN.png')
        if Hero.LEFT_RUN_image == None:
            Hero.LEFT_RUN_image = load_image('CH_LEFT_RUN.png')
        if Hero.RIGHT_STAND_image == None:
            Hero.RIGHT_STAND_image = load_image('CH_RIGHT_STAND.png')
        if Hero.LEFT_STAND_image == None:
            Hero.LEFT_STAND_image = load_image('CH_LEFT_STAND.png')

    def update(self, frame_time, G_y, G_sizey):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        if(self.x > 500):
            self.dir = 0
            self.x = 500
            self.isNext = True
        elif(self.x < 0):
            self.dir = 0
            self.x = 0
        else:
            self.dir = 1
            self.isNext = False

        self.handle_state[self.state](self)
        self.total_frames += Hero.FRAMES_PER_ACTION * Hero.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 3

        distance = Hero.RUN_SPEED_PPS * frame_time
        self.x += (self.dir * distance)

        if (self.y <= 180 and self.isjump == True and self.isreach == False):   # reach highest
            self.y += 200 * frame_time
        if self.y >= 180:
            self.isreach = True
        if self.isreach == True:
            self.y -= 200 * frame_time
        if self.y <= G_y + G_sizey + self.sizey:
            self.isreach = False
            self.isjump = False

    def draw(self):
        self.image.clip_draw(self.frame * 34, 0, 33, 39, self.x, self.y, 80, 100)
        for hp in self.Hp:
            hp.draw()

    def handle_right_run(self):
        self.image = self.RIGHT_RUN_image
        self.dir = 1

    def handle_left_run(self):
        self.image = self.LEFT_RUN_image
        self.dir = -1

    def handle_right_stand(self):
        self.image = self.RIGHT_STAND_image
        self.ismove = False
        self.dir = 0

    def handle_left_stand(self):
        self.image = self.LEFT_STAND_image
        self.ismove = False
        self.dir = 0

    def handle_jump(self):
        pass

    handle_state = {
        RIGHT_RUN: handle_right_run,
        LEFT_RUN: handle_left_run,
        RIGHT_STAND: handle_right_stand,
        LEFT_STAND: handle_left_stand,
        JUMP: handle_jump
    }

    def get_bb(self):
        return self.x - self.sizex, self.y - self.sizey, self.x + self.sizex, self.y + self.sizey

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                self.state = self.LEFT_RUN
                self.ismove = True
            elif event.key == SDLK_RIGHT:
                self.state = self.RIGHT_RUN
                self.ismove = True
            elif event.key == SDLK_UP:
                if self.isjump == False:
                    self.isjump = True

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                self.state = self.LEFT_STAND

            elif event.key == SDLK_RIGHT:
                self.state = self.RIGHT_STAND

class Hero_Hp:
    image = None

    def __init__(self, Hpnum):
        self.x, self.y = Hpnum * 40 + 30, 550
        #if Hero_Hp == None:
        Hero_Hp.image = load_image('heart_full_32x32.png')

    def draw(self):
        self.image.draw(self.x, self.y)
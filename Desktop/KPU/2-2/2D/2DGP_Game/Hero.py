import random
import Tile
from Functions import *

LEFT_MOVE = -1
STOP_MOVE = 0
RIGHT_MOVE = 1

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

    JUMPHIGH = 100                  # 점프 높이

    image = None
    RIGHT_RUN_image = None
    LEFT_RUN_image = None
    RIGHT_STAND_image = None
    LEFT_STAND_image = None

    RIGHT_RUN = 1                   # Boy's Move
    LEFT_RUN = 2
    RIGHT_STAND = 3
    LEFT_STAND = 4
    JUMP = 5
    Jump_Sound = None

    def __init__(self, Level):
        self.x, self.y = 0, 100
        self.sizex, self.sizey = 25, 50
        self.dir = STOP_MOVE
        self.frame = 0
        self.total_frames = 0.0
        self.state = self.RIGHT_STAND
        self.ismove = False
        self.isNext = False

        # 점프시 사용
        self.tempy = 0
        self.isjump = False
        self.isreach = False
        self.jump_speed = 200

        # 피격시
        self.isSuper = False
        self.SuperTime = 0.0

        self.MaxHp = 0
        if Level == 0:
            self.MaxHp = 5
        else:
            self.MaxHp = 3

        self.Hpnum = self.MaxHp

        self.Hp = [Hero_Hp(i) for i in range(self.Hpnum)]

        if Hero.RIGHT_RUN_image == None:
            Hero.RIGHT_RUN_image = load_image('CH_RIGHT_RUN.png')
        if Hero.LEFT_RUN_image == None:
            Hero.LEFT_RUN_image = load_image('CH_LEFT_RUN.png')
        if Hero.RIGHT_STAND_image == None:
            Hero.RIGHT_STAND_image = load_image('CH_RIGHT_STAND.png')
        if Hero.LEFT_STAND_image == None:
            Hero.LEFT_STAND_image = load_image('CH_LEFT_STAND.png')
        if Hero.Jump_Sound == None:
            Hero.Jump_Sound = load_wav('hero_jumping.wav')
            Hero.Jump_Sound.set_volume(10)

    def update(self, frame_time, tile):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        if(self.x > 500):
            self.dir = STOP_MOVE
            self.x = 500
            self.isNext = True
        elif(self.x < 0):
            self.dir = STOP_MOVE
            self.x = 0
        else:
            self.dir = RIGHT_MOVE
            self.isNext = False

        self.handle_state[self.state](self)
        self.total_frames += Hero.FRAMES_PER_ACTION * Hero.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 3

        distance = Hero.RUN_SPEED_PPS * frame_time
        self.x += (self.dir * distance)

        if self.y <= self.tempy + Hero.JUMPHIGH and self.isjump is True and self.isreach is False:
            self.y += self.jump_speed * frame_time
        if self.y >= self.tempy + Hero.JUMPHIGH:
            self.isreach = True
        if self.isreach is True:
            self.y -= self.jump_speed * frame_time
        if self.y < tile.y + tile.sizey + self.sizey:
            self.isreach = False
            self.isjump = False

        if self.isSuper is True and self.SuperTime <= 5.0:
            self.SuperTime += 1.5 * frame_time
        elif self.SuperTime > 5.0:
            self.SuperTime = 0.0
            self.isSuper = False

    def draw(self):
        if self.isSuper is True:
            Rand_image = random.randint(1,3)
            if Rand_image is 1 or Rand_image is 2:
                self.image.clip_draw(self.frame * 34, 0, 33, 39, self.x, self.y, 80, 100)
        else:
            self.image.clip_draw(self.frame * 34, 0, 33, 39, self.x, self.y, 80, 100)

        for hp in self.Hp:
            hp.draw()

    def handle_right_run(self):
        self.image = self.RIGHT_RUN_image
        self.dir = RIGHT_MOVE

    def handle_left_run(self):
        self.image = self.LEFT_RUN_image
        self.dir = LEFT_MOVE

    def handle_right_stand(self):
        self.image = self.RIGHT_STAND_image
        self.dir = STOP_MOVE

    def handle_left_stand(self):
        self.image = self.LEFT_STAND_image
        self.dir = STOP_MOVE

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

    def handle_event(self, event, tiles):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                self.state = self.LEFT_RUN
                self.ismove = True
                for tile in tiles:
                    if MyCrysh_To_Tile(self, tile):
                        self.x = tile.x + tile.sizex + self.sizex
                        self.dir = STOP_MOVE
            elif event.key == SDLK_RIGHT:
                self.state = self.RIGHT_RUN
                self.ismove = True
                for tile in tiles:
                    if MyCrysh_To_Tile(self, tile):
                        self.x = tile.x - tile.sizex - self.sizex
                        self.dir = STOP_MOVE
            elif event.key == SDLK_UP:
                if self.isjump is False:
                    self.tempy = self.y
                    self.isjump = True
                    Hero.Jump_Sound.play(1)

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                self.state = self.LEFT_STAND

            elif event.key == SDLK_RIGHT:
                self.state = self.RIGHT_STAND

class Hero_Hp:
    image = None

    def __init__(self, Hpnum):
        self.x, self.y = Hpnum * 40 + 30, 550
        if Hero_Hp.image is None:
            Hero_Hp.image = load_image('heart_full_32x32.png')

    def draw(self):
        self.image.draw(self.x, self.y)
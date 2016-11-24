import random

from pico2d import *

LEFT_MOVE = -1
RIGHT_MOVE = 1

class Moon:
    image = None

    def __init__(self):
        self.x = 670
        self.y = 500
        self.speed = 5
        if Moon.image == None:
            Moon.image = load_image('platformertiles.png')
    def update(self, Hero_Dir, frame_time):
        #if ismove == 1:
        #    self.x += self.speed * frame_time
        if self.x <= 670:
            if Hero_Dir is LEFT_MOVE or RIGHT_MOVE:
                self.x += self.speed * frame_time * -Hero_Dir
        else:
            self.x = 670
    def draw(self):
        self.image.clip_draw(32 * 3, 32 * 2, 32, 32, self.x, self.y, 80, 80)

class BackGround:
    Backimage = None

    def __init__(self):
        self.star_time = 5.0
        self.star = [[0]*15 for i in range(20)]
        self.star_frame = [[0]*15 for i in range(20)]
        if BackGround.Backimage == None:
            BackGround.Backimage = load_image('platformertiles.png')

    def update(self, frame_time):
        if self.star_time >= 5:
            for i in range(20):
                for j in range(15):
                    self.star[i][j] = random.randint(1, 20)
                    self.star_frame[i][j] = random.randint(0,2)
                    self.star_time = 0
        self.star_time += 1.5 * frame_time

    def draw(self):
        self.Backimage.clip_draw(32 * 3, 32, 32, 32, 0, 0, 1600, 1200)                      #Back
        for i in range(20):
            for j in range(15):
                if self.star[i][j] == 1:
                    self.Backimage.clip_draw((32 * (5 + self.star_frame[i][j])), 32, 32, 32, i * 40, j * 40, 80, 80)  #star

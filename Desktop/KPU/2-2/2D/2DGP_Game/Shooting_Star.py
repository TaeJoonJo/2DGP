import random

from pico2d import *

class Shooting_Star:
    image = None

    APPEAR = 1
    DISAPPEAR = 0

    def __init__(self):
        self.x = random.randint(-200, 700)
        self.y = 600
        self.sizex = 15
        self.sizey = 15
        self.isstate = Shooting_Star.APPEAR
        self.speed = random.randint(200,300)
        self.size = 1
        if(Shooting_Star.image == None):
            Shooting_Star.image = load_image('Star.png')

    def update(self, frame_time, isNext):
        distance = self.speed * frame_time
        self.x += distance
        self.y -= distance
        if(isNext == True):
            self.x -= distance * 0.5
        if (self.x >= 800 or self.y <= 0):
            self.isstate = Shooting_Star.DISAPPEAR

    def draw(self):
        self.image.clip_draw(0, 0, 34, 34, self.x, self.y, 30 * self.size, 30 * self.size)

    def get_bb(self):
        return self.x - self.sizex, self.y - self.sizey, self.x + self.sizex, self.y + self.sizey

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
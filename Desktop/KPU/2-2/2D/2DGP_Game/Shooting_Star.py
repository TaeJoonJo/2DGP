import random

from pico2d import *

class Shooting_Star:
    starimage = None
    hpimage = None

    Star_Sound = None
    Hp_Sound = None

    APPEAR = 1
    DISAPPEAR = 0

    #Type
    STAR = 0
    HP = 1

    def __init__(self):
        self.x = random.randint(-200, 700)
        self.y = 600
        self.sizex = 15
        self.sizey = 15
        self.isstate = Shooting_Star.APPEAR
        self.speed = random.randint(200,300)
        self.size = 1
        self.type = Shooting_Star.STAR
        if(Shooting_Star.starimage == None):
            Shooting_Star.starimage = load_image('Star.png')
        if Shooting_Star.hpimage == None:
            Shooting_Star.hpimage = load_image('heart_full_32x32.png')
        if(Shooting_Star.Star_Sound == None):
            Shooting_Star.Star_Sound = load_wav('star_get.wav')
            Shooting_Star.Star_Sound.set_volume(40)
        if(Shooting_Star.Hp_Sound == None):
            Shooting_Star.Hp_Sound = load_wav('item_get.wav')
            Shooting_Star.Hp_Sound.set_volume(10)

    def update(self, frame_time, isNext):
        distance = self.speed * frame_time
        self.x += distance
        self.y -= distance
        if(isNext == True):
            self.x -= distance * 0.5
        if (self.x >= 800 or self.y <= 0):
            self.isstate = Shooting_Star.DISAPPEAR

        #if self.type is Shooting_Star.HP and self.isstate is Shooting_Star.DISAPPEAR:


    def draw(self):
        if self.type == Shooting_Star.STAR:
            self.starimage.clip_draw(0, 0, 34, 34, self.x, self.y, 30 * self.size, 30 * self.size)
        elif self.type == Shooting_Star.HP:
            self.hpimage.draw(self.x, self.y)

    def get_bb(self):
        return self.x - self.sizex, self.y - self.sizey, self.x + self.sizex, self.y + self.sizey

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
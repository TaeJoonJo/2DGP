import random

from pico2d import *

class Tile:
    image = None
    def __init__(self, xnum, ynum):
        self.frame = 0
        self.sizex, self.sizey = 50, 50
        self.x = xnum * 50
        self.y = ynum * 50
        if Tile.image == None:
            Tile.image = load_image('platformertiles.png')

    def update(self, frame_time, isNext, hero_speed):
        self.frame = (self.frame + 1) % 8
        if isNext == True:
            self.x -= hero_speed * frame_time

    def draw(self):
        self.image.clip_draw(32, 32*2, 32, 32, self.x, self.y, 100, 100)

    def get_bb(self):
        return self.x - self.sizex, self.y - self.sizey, self.x + self.sizex, self.y + self.sizey

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

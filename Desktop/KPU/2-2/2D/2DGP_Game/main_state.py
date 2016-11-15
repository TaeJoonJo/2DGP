import random
import json
import os

from Hero import Hero
from Tile import Tile
from BackGround import BackGround, Moon
from Shooting_Star import Shooting_Star

from pico2d import *

import game_framework
import title_state

name = "MainState"

boy = None
grass = None
background = None
moon = None
font = None
stars = None

def create_world():
    global hero, tile
    global background
    global moon
    global stars
    background = BackGround()
    hero = Hero()
    tile = Tile()
    moon = Moon()
    stars = [Shooting_Star() for i in range(10)]

def destroy_world():
    global hero, tile
    global background
    global moon
    global stars
    del (background)
    del (hero)
    del (tile)
    del (moon)
    del (stars)

def enter():
    game_framework.reset_time()
    create_world()
    #open_canvas()

def exit():
    destroy_world()

def pause():
    pass

def resume():
    pass

def handle_events(frame_time):
    events = get_events()
    for event in events:
        hero.handle_event(event)
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
            elif event.key == SDLK_LEFT:
                if (moon.x <= 670):
                    moon.speed = 3
            elif event.key == SDLK_RIGHT:
                if (moon.x >= 130):
                    moon.speed = -3
        #else:

current_time = get_time()

def update(frame_time):
    global current_time
    global stars
    background.update(hero.ismove, hero.state)
    for i in range(10):
        stars[i].update()
        if stars[i].isstate == 0:
            stars[i] = Shooting_Star()
    hero.update(frame_time)
    tile.update()
    moon.update(hero.ismove)

    #delay(0.05)

    frame_time = get_time() - current_time
    frame_rate = 1.0 / frame_time
    print("Frame Rate : %f fps, Frame Time : %f sec," % (frame_rate, frame_time))

    current_time += frame_time


def draw(framge_time):
    global stars
    clear_canvas()
    background.draw()
    for i in range(10):
        stars[i].draw()
    moon.draw()
    tile.draw()
    hero.draw()
    update_canvas()







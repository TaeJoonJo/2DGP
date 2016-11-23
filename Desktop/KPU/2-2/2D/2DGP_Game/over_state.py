import game_framework
import os
from pico2d import *

import main_state
import title_state

name = "OverState"
image = None

def enter():
    global image
    image = load_image('Game_Over.png')

def exit():
    global image
    del(image)

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(title_state)

def draw(frame_time):
    clear_canvas()
    image.clip_draw(0, 0, 256, 224, 400, 300, 800, 600)
    #image.draw(400, 300)
    update_canvas()

def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass



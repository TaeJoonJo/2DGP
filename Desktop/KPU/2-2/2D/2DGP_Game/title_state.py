import game_framework
import os
from pico2d import *

import main_state

name = "TitleState"
image = None
font = None

def enter():
    global image, font
    image = load_image('Main.png')
    font = load_font('ENCR10B.TTF', 20)

def exit():
    global image
    del(image)
    #close_canvas()

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)

def draw(frame_time):
    clear_canvas()
    image.clip_draw(0, 0, 1500, 850, 0, 0, 1600, 1200)
    font.draw(200, 100, 'Press Space To Play', (255,255,255))
    update_canvas()

def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass







import game_framework
import os
from pico2d import *

import main_state

START = 0
CHOICE = 1

NOMAL = 0
HARD = 1

name = "TitleState"
image = None
font = None
title_bgm = None
sound1 = None
sound2 = None
Star = None
S_x = 580
S_y = 150

State = START

Level = None

def enter():
    global image, font
    global title_bgm
    global Star
    global sound1, sound2
    global State
    title_bgm = load_music('Title.mp3')
    title_bgm.set_volume(90)
    title_bgm.repeat_play()
    image = load_image('Main.png')
    font = load_font('ENCR10B.TTF', 20)
    Star = load_image('title_star.png')
    sound1 = load_wav('Title_Sound1.wav')
    sound1.set_volume(30)
    sound2 = load_wav('Title_Sound2.wav')
    sound2.set_volume(30)
    State = START

def exit():
    global image
    global font
    global title_bgm
    global Star
    del(font)
    del(title_bgm)
    del(image)
    del(Star)
    #close_canvas()

def handle_events(frame_time):
    global State
    global S_x, S_y
    global Level
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE) and State is START:
                sound1.play()
                State = CHOICE
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE) and State is CHOICE:
                sound2.play()
                delay(0.5)
                if S_y == 150:
                    Level = NOMAL
                else:
                    Level = HARD
                game_framework.change_state(main_state)
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_UP:
                    if S_y == 150:
                        S_y = 100
                    else:
                        S_y += 50
                elif event.key == SDLK_DOWN:
                    if S_y == 100:
                        S_y = 150
                    else:
                        S_y -= 50

def draw(frame_time):
    clear_canvas()
    image.clip_draw(0, 0, 1500, 850, 0, 0, 1600, 1200)
    if State is START:
        font.draw(200, 100, 'Press Space Bar To Play', (255,255,255))
    elif State is CHOICE:
        font.draw(600, 150, 'NORMAL', (255, 255, 255))
        font.draw(600, 100, 'HARD', (255, 255, 255))
        Star.clip_draw(0, 0, 512, 512, S_x, S_y, 60, 60)
    update_canvas()

def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass







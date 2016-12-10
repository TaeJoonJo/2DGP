import random
import json
import os
import over_state

from pico2d import *
from Functions import *

from Hero import Hero, Hero_Hp
from Tile import Tile
from BackGround import BackGround, Moon
from Shooting_Star import Shooting_Star

import game_framework
import title_state

name = "MainState"

tile_num = 17
STARNUM = 7

bgm = None
isRect = False

hero = None
grass = None
background = None
moon = None
font = None
stars = None
tiles = None

def create_world():
    global hero
    global background
    global moon
    global stars
    global tiles
    global bgm
    bgm = load_music('For_River.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()
    background = BackGround()
    hero = Hero()
    moon = Moon()
    tiles = [Tile(i, 0) for i in range(17)]
    new_tile = Tile(17, 1)
    tiles.append(new_tile)
    stars = [Shooting_Star() for i in range(STARNUM)]

def destroy_world():
    global hero
    global background
    global moon   #
    global stars
    global tiles
    global bgm
    del (bgm)
    del (background)
    del (hero)
    del (moon)
    del (stars)
    del (tiles)

def enter():
    game_framework.reset_time()
    create_world()

def exit():
    destroy_world()

def pause():
    pass

def resume():

    pass

def handle_events(frame_time):
    global isRect
    events = get_events()
    for event in events:
        hero.handle_event(event)
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
            elif event.key == SDLK_LEFT:
                pass
            elif event.key == SDLK_RIGHT:
                pass
            elif event.key == SDLK_1:
                if(isRect == False):
                    isRect = True
                else:
                    isRect = False
        #else:

def Game_End_Check():
    global moon
    global hero

    if (hero.Hpnum) == 0:
        game_framework.push_state(over_state)
    elif moon.x <= 100:
        game_framework.push_state(over_state)   #


current_time = get_time()   #


def update(frame_time):
    global tile_num
    global stars
    global tiles
    global moon
    Snum = 0
    background.update(frame_time)

    Game_End_Check()

    for star in stars:
        star.update(frame_time, hero.isNext)
        if MyCrush(star, hero) and hero.isSuper is False:
            star.isstate = Shooting_Star.DISAPPEAR
            hero.Hp.pop()
            hero.Hpnum -= 1
            hero.isSuper = True

        if star.isstate == Shooting_Star.DISAPPEAR:
            stars.remove(star)
            new_star = Shooting_Star()
            stars.append(new_star)

    for tile in tiles:
        tile.update(frame_time, hero.isNext, Hero.RUN_SPEED_PPS)
        if Snum == 0:
            hero.update(frame_time, tile.y, tile.sizey)
            Snum += 1
        if MyCrush(hero, tile):
            hero.y = tile.y + tile.sizey + hero.sizey
        if(tile.x < 0 and tile_num == 17):
            tiles.remove(tile)
            tile_num -= 1
        if(tile_num < 17):
            new_tile = Tile(17, 0)
            tiles.append(new_tile)
            tile_num += 1
    #hero.update(frame_time)

    moon.update(hero.dir, frame_time)

    #delay(0.05)

    frame_rate = 1.0 / frame_time
    print("Frame Rate : %f fps, Frame Time : %f sec," % (frame_rate, frame_time))

def draw(framge_time):
    #global stars
    #hp = Hero_Hp(2)
    clear_canvas()
    background.draw()
    for star in stars:
        star.draw()
        if isRect == True:
            star.draw_bb()
    moon.draw()
    for tile in tiles:
        tile.draw()
        if isRect == True:
            tile.draw_bb()
    hero.draw()
    if isRect == True:
        hero.draw_bb()

    update_canvas()


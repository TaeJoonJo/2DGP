import random
import json
import os
import over_state

from Functions import *

from Hero import Hero, Hero_Hp
from Tile import Tile
from BackGround import BackGround, Moon
from Shooting_Star import Shooting_Star


from pico2d import *

import game_framework
import title_state

name = "MainState"

tile_num = 17
STARNUM = 7

hero = None
grass = None
background = None
moon = None
font = None
stars = None
tiles = None

isRect = True

def create_world():
    global hero
    global background
    global moon
    global stars
    global tiles
    background = BackGround()
    hero = Hero()
    #hero.Hp = (Hero_Hp(i) for i in range(3))
    moon = Moon()
    tiles = [Tile(i) for i in range(17)]
    stars = [Shooting_Star() for i in range(STARNUM)]

def destroy_world():
    global hero
    global background
    global moon   #
    global stars
    global tiles
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
                if (moon.x <= 670):
                    moon.speed = 3
            elif event.key == SDLK_RIGHT:
                if (moon.x >= 130):
                    moon.speed = -3
            elif event.key == SDLK_1:
                if(isRect == False):
                    isRect = True
                else:
                    isRect = False
        #else:

current_time = get_time()

def update(frame_time):
    global tile_num
    global stars
    global tiles
    Snum = 0
    background.update(frame_time)

    if hero.Hpnum == 0:
        game_framework.push_state(over_state)


    for star in stars:
        star.update(frame_time, hero.isNext)
        if MyCrush(star, hero):
            star.isstate = 0
            hero.Hp.pop()
            hero.Hpnum -= 1
        if star.isstate == 0:
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
            #hero.isreach = False
            #hero.isjump = False
        if(tile.x < 0 and tile_num == 17):
            tiles.remove(tile)
            tile_num -= 1
        if(tile_num < 17):
            new_tile = Tile(17)
            tiles.append(new_tile)
            tile_num += 1
    #hero.update(frame_time)
    moon.update(hero.ismove, frame_time)


    #delay(0.05)

    frame_rate = 1.0 / frame_time
    print("Frame Rate : %f fps, Frame Time : %f sec," % (frame_rate, frame_time))

def draw(framge_time):
    global stars
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
    #for Hp in hero.Hp:
    #    Hp.draw()
    #hp.drawa()
    update_canvas()







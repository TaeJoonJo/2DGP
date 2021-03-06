import random
import json
import os
import over_state
import end_state
import title_state

from pico2d import *
from Functions import *

from Hero import Hero, Hero_Hp
from Tile import Tile
from BackGround import BackGround, Moon
from Shooting_Star import Shooting_Star
from Monster import Monster

import game_framework
import title_state

name = "MainState"

Credit_Time = 0.0

Start_Credit = 0
Ending_Credit = 1
Heroine_Die_Image = None
Heroine_x = 0
Not_Credit = 2

Credit = Not_Credit

tile_num = 17

bgm = None
isRect = False

hero = None
grass = None
background = None
moon = None
font = None
stars = None
tiles = None
monsters = None

Level = 0

NORMAL = 0
HARD = 1

STARNUM = 0
MonsterNum = 0

Gametemp2 = 0
blanktile = 0
isBlank = True

def create_world():
    global hero
    global background
    global moon
    global stars
    global tiles
    global bgm
    global STARNUM
    global Level
    global monsters
    global Heroine_Die_Image
    global Credit
    global Heroine_x
    Credit = Not_Credit
    bgm = load_music('For_River.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()
    background = BackGround()
    moon = Moon()
    tiles = [Tile(i, 0) for i in range(17)]
    # new_tile = Tile(15, 1)
    # tiles.append(new_tile)
    Level = title_state.Level
    hero = Hero(Level)
    if Level == NORMAL:
        STARNUM = 7
    else:
        STARNUM = 12
    stars = [Shooting_Star() for i in range(STARNUM)]
    monsters = [Monster() for i in range(1)]
    Heroine_Die_Image = load_image('heroine_die.png')
    Heroine_x = 800
def destroy_world():
    global hero
    global background
    global moon   #
    global stars
    global tiles
    global bgm
    global monsters
    del (bgm)
    del (background)
    del (hero)
    del (moon)
    del (stars)
    del (tiles)
    del (monsters)

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
        if Credit is Not_Credit:
            hero.handle_event(event, tiles)
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
                if isRect is False:
                    isRect = True
                else:
                    isRect = False
        # else:

def Game_End_Check():
    global moon
    global hero
    global Credit

    if hero.Hpnum == 0:
        game_framework.push_state(over_state)
    elif moon.x <= 100:
        Credit = Ending_Credit
        #game_framework.push_state(end_state)

current_time = get_time()

def Ending_Credit_Update(frame_time):
    global hero
    global Heroine_x
    global Credit_Time
    if hero.state is not hero.RIGHT_STAND:
        hero.state = hero.RIGHT_STAND
    if hero.x >= 100:
        distance = Hero.RUN_SPEED_PPS * frame_time
        hero.x -= distance * 0.75
    else:
        Credit_Time += 1.0 * frame_time
    if Heroine_x >= 550:
        distance = Hero.RUN_SPEED_PPS * frame_time
        Heroine_x -= distance * 0.25
    if Credit_Time > 5.0:
        game_framework.push_state(end_state)


def update(frame_time):
    global tile_num
    global stars
    global tiles
    global moon
    global Gametemp2
    global blanktile
    global isBlank
    global monsters
    global MonsterNum
    Snum = 0
    background.update(frame_time)

    Game_End_Check()

    if Credit is Ending_Credit:
        Ending_Credit_Update(frame_time)

    for star in stars:
        star.update(frame_time, hero.isNext)
        if MyCrush(star, hero):                              # 별과 캐릭터 충돌
            if hero.isSuper is False:
                star.Star_Sound.play()
                star.isstate = Shooting_Star.DISAPPEAR
                if star.type is Shooting_Star.STAR and Credit is Not_Credit:
                    hero.Hp.pop()
                    hero.Hpnum -= 1
                    hero.isSuper = True
            if star.type is Shooting_Star.HP and hero.Hpnum < hero.MaxHp and Credit is Not_Credit:
                star.Hp_Sound.play()
                new_hp = Hero_Hp(hero.Hpnum)
                hero.Hpnum += 1
                star.isstate = Shooting_Star.DISAPPEAR
                hero.Hp.append(new_hp)

        if star.isstate == Shooting_Star.DISAPPEAR:             # 별 삭제후 추가
            stars.remove(star)
            new_star = Shooting_Star()
            Gametemp = random.randint(0, 10)
            if Gametemp is 1:
                new_star.type = Shooting_Star.HP
            stars.append(new_star)

    for monster in monsters:
        monster.update(frame_time, hero.isNext)
        if monster.x < 0 - monster.sizex:
            monsters.remove(monster)
            MonsterNum -= 1
        if MyCrush(hero, monster) and Credit is Not_Credit:
            if hero.isSuper is False:
                monster.Sound.play()
                hero.Hp.pop()
                hero.Hpnum -= 1
                hero.isSuper = True
    Gametemp3 = random.randint(0, 1000)
    if Gametemp3 == 512 and MonsterNum < 2 and Credit is Not_Credit:
        new_monster = Monster()
        monsters.append(new_monster)
        MonsterNum += 1

    for tile in tiles:                                          # 바닥과의 충돌처리
        tile.update(frame_time, hero.isNext, Hero.RUN_SPEED_PPS)
        if Snum == 0:
            hero.update(frame_time, tile)
            Snum += 1
        if MyCrush(hero, tile):
            hero.y = tile.y + tile.sizey + hero.sizey
        if tile.x < 0 :
            tiles.remove(tile)
            tile_num -= 1
        if tile_num < 17:
            if (Gametemp2 is not 3) or (blanktile >= 3):
                Gametemp2 = random.randint(1, 30)
                new_tile = Tile(17, 0)
                tiles.append(new_tile)
                blanktile = 0
                tile_num += 1
            elif (Gametemp2 is 3) and (blanktile < 3):
                blanktile += 1

    moon.update(hero.dir, frame_time)

    frame_rate = 1.0 / frame_time
    print("Moon : %d" % moon.x)

def draw(framge_time):
    clear_canvas()
    background.draw()
    for star in stars:
        star.draw()
        if isRect is True:
            star.draw_bb()
    moon.draw()
    for tile in tiles:
        tile.draw()
        if isRect is True:
            tile.draw_bb()
    for monster in monsters:
        monster.draw()
        if isRect is True:
            monster.draw_bb()
    hero.draw()
    if isRect is True:
        hero.draw_bb()

    if Credit is Ending_Credit:
        Heroine_Die_Image.clip_draw(0, 0, 27, 15, Heroine_x, 75, 100, 50)


    update_canvas()


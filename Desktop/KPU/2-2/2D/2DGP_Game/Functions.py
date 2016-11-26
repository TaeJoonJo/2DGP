from pico2d import *

def MyCrush(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def MyCrysh_To_Tile(a,b):                           # 타일과의 충돌체크는 나눈다.
    left_a, bottom_a, right_a, top_a = a.get_bb()      # 하단부만 충돌하도록
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

    pass
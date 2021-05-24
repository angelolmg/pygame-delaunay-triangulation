from math import atan2, degrees
from random import randint

def calcular_centroide_poly(poly):
    width = len(poly)
    if width == 0:
        return None

    x = 0
    y = 0

    for point in poly:
        x += point.x
        y += point.y

    return (int(x/width), int(y/width))

def sort_pontos_poly(poly):
    cx, cy = calcular_centroide_poly(poly)
    poly.sort(key=lambda vertice: degrees(atan2(vertice.x - cx, vertice.y - cy)))
    return poly

def inCircle (ax, ay, bx, by, cx, cy, dx, dy):
    ax_ = ax - dx
    ay_ = ay - dy
    bx_ = bx - dx
    by_ = by - dy
    cx_ = cx - dx
    cy_ = cy - dy

    ak = (ax_ * ax_) + (ay_ * ay_)
    bk = (bx_ * bx_) + (by_ * by_)
    ck = (cx_ * cx_) + (cy_ * cy_)

    
    det = (
        ((ax_* by_ * ck) + (ay_* bk * cx_) + (ak * bx_ * cy_)) -
        ((cx_* by_ * ak) + (cy_* bk * ax_) + (ck * bx_ * ay_))  
    )
    

    result = (det < 0)

    return result

def bound(low, high, value):
    return max(low, min(high, value))

def random_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))

def random_shade(shade, luminance):
    r, g, b = shade
    value = randint(-luminance, luminance)
    new_r, new_g, new_b = (r + value, g + value, b + value)
    return (bound(0, 255, new_r), bound(0, 255, new_g), bound(0, 255, new_b))

def get_shade(shade, alfa):
    r, g, b = shade
    luminance = int((1 - alfa) * 255)

    new_r, new_g, new_b = (r + luminance, g + luminance, b + luminance)
    return (bound(50, 255, new_r), bound(50, 255, new_g), bound(50, 255, new_b))
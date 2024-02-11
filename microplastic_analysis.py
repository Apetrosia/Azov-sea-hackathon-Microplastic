import cv2
import numpy as np
from math import sqrt
#from colorthief import ColorThief
#import os

COLORS = {
    (0,0,0): 'Black',
    #(122, 122, 122): 'Gray',
    (255, 255, 255): 'White',
    (255,0,0): 'Red',
    (0,255,0): 'Green',
    (0,0,255): 'Blue',
    (255,255,0): 'Yellow',
    (0, 255, 255): 'Aqua',
    (255, 0, 255): 'Purple',
    #(255,165,0): 'Orange'
}

def dist(v1, v2):
    return sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2 + (v1[2] - v2[2])**2)

def determine_color_category(color):
    min_dist = 1e9
    nearest_color = (0, 0, 0)
    for cl in COLORS.keys():
        v = list(cl)
        d = dist(v, color)
        #print(v, color, d)
        if d < min_dist:
            min_dist = d
            nearest_color = cl
    return COLORS[nearest_color]

def unique_count_app(a):
    colors, count = np.unique(a.reshape(-1,a.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax()]
def anylize_color(image):
    h, w = image.shape[:2]
    y, x = h//2, w//2
    if h < 12 or w < 12:
        center = image
    else:
        center = image[y - 5:y + 5, x - 5:x + 5]
    dominant_color = cv2.mean(center)[-2::-1]  # OpenCV возвращает BGRA, берем RGB
    #dominant_color = unique_count_app(image)
    #cv2.imwrite('$temp$.png', image)
    #color_thief = ColorThief('$temp$.png')
    #dominant_color = color_thief.get_color(quality=1)
    #print(dominant_color)
    color_category = determine_color_category(dominant_color)
    #os.remove('$temp$.png')
    return color_category


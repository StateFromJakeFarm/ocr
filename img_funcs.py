from PIL import Image
from os import listdir
from math import sqrt, floor
from basic_funcs import clear_folder
import os
import sys
import subprocess
import shutil
import glob

def get_char_bounds(img, high_lo=None):
    """Get the boundaries of the actual character within an image"""
    img_x, img_y = img.size
    pixels = img.load()

    # high-pass/low-pass filter
    if high_lo:
        for y in range(img_y):
            for x in range(img_x):
                if pixels[x,y] <= high_lo:
                    pixels[x,y] = 0
                else:
                    pixels[x,y] = 255

    bounds = [-1,-1,-1,-1]
    # start x, end x
    for x in range(img_x):
        saw_char = False
        for y in range(img_y):
            if bounds[0] == -1:
                if pixels[x,y] == 0:
                    bounds[0] = x
                    saw_char = True
            else:
                if pixels[x,y] == 0:
                    if x != img_x-1:
                        saw_char = True
                    else:
                        bounds[2] = x-1
                elif y == img_y-1 and not saw_char:
                    bounds[2] = x-1

        if bounds[0] != -1 and not saw_char:
            break

    # start y (from top downwards)
    y = 0
    while y < img_y:
        for x in range(img_x):
            if pixels[x,y] == 0:
                bounds[1] = y
                y = img_y
                break
        y += 1

    # end y (from bottom upwards)
    y = img_y-1
    while y >= 0:
        for x in range(img_x):
            if pixels[x,y] == 0:
                bounds[3] = y
                y = -1
                break
        y -= 1

    return bounds

def char_resize_square(path, new_path, side_len, high_lo=None):
    """Crop image to character and save as square bitmap"""
    img = None
    if type(path) is str:
        img = Image.open(path).convert('L')
    else:
        img = path

    # Get bounds of character within the image
    bounds = get_char_bounds(img, high_lo)

    # bad strip
    if -1 in bounds:
        return

    img = img.crop(tuple(bounds)).resize((side_len,side_len), Image.LANCZOS)
    img.convert('RGB').save(new_path)

def char_resize_area(path, new_path, area, high_lo=None):
    """Crop image to character and save as bitmap with certain area and same width/height ratio"""
    img = None
    if type(path) is str:
        img = Image.open(path).convert('L')
    else:
        img = path

    # Get bounds of character within the image
    bounds = get_char_bounds(img, high_lo)

    # bad strip
    if -1 in bounds:
        return    

    # Get the current ratio
    img_x = bounds[2] - bounds[0]
    img_y = bounds[3] - bounds[1]
    x_to_y = float(img_x) / float(img_y)

    # Get the new dimensions that will maintain the ratio with desired area
    new_x = int(floor(sqrt(area) * x_to_y))
    if new_x <= 0:
        new_x = 1

    new_y = int(floor(area / new_x))
    if new_y <= 0:
        new_y = 1

    img = img.crop(tuple(bounds)).resize((new_x, new_y), Image.LANCZOS)
    img.convert('RGB').save(new_path)

def create_formatted(raw_folder, bmp_folder, side_len):
    """Convert images of characters to properly-formatted images"""
    clear_folder(bmp_folder)

    for char in listdir(raw_folder):
        i = 0
        for f in listdir(os.path.join(raw_folder, char)):
            raw_path = os.path.join(raw_folder, char, f)
            bmp_path = os.path.join(bmp_folder, char+str(i)+'.bmp')
            print(raw_path + ' --(' + str(side_len) + 'x' + str(side_len) + ')-> ' + bmp_path)
            char_resize_square(raw_path, bmp_path, side_len)
            i += 1

    print('Training images prepared')

def find_chars(raw_path, found_folder, area, high_lo=50):
    """Slice up an image into its separate characters"""
    clear_folder(found_folder)

    img = Image.open(raw_path).convert('L')
    img_x, img_y = img.size
    pixels = img.load()

    for y in range(img_y):
        for x in range(img_x):
            if pixels[x,y] <= high_lo:
                pixels[x,y] = 0
            else:
                pixels[x,y] = 255

    bounds = [-1,0,img_x,img_y]
    i = 0
    for x in range(img_x):
        saw_char = False
        for y in range(img_y):
            if bounds[0] == -1:
                if pixels[x,y] == 0:
                    bounds[0] = x
                    saw_char = True
            else:
                if pixels[x,y] == 0:
                    saw_char = True
                elif y == img_y-1 and not saw_char:
                    bounds[2] = x-1

        if bounds[0] != -1 and not saw_char:
            i += 1
            char_resize_square(img.crop(tuple(bounds)), os.path.join(found_folder, str(i) + '.bmp'), area)
            bounds = [-1,0,img_x,img_y]

def get_grayscale_vals(img_file_path):
    img = Image.open(img_file_path).convert('L')
    grayscale_vals = [int(x) for x in list(img.getdata())]
    img.close()
    return grayscale_vals

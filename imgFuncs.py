from PIL import Image
from os import listdir
from math import sqrt, floor
from basicFuncs import clear_folder
import os
import sys
import subprocess
import shutil
import glob

def get_char_bounds(img, highLo=None):
    """Get the boundaries of the actual character within an image"""
    imgX, imgY = img.size
    pixels = img.load()

    # high-pass/low-pass filter
    if highLo:
        for y in range(imgY):
            for x in range(imgX):
                if pixels[x,y] <= highLo:
                    pixels[x,y] = 0
                else:
                    pixels[x,y] = 255

    bounds = [-1,-1,-1,-1]
    # start x, end x
    for x in range(imgX):
        saw_char = False
        for y in range(imgY):
            if bounds[0] == -1:
                if pixels[x,y] == 0:
                    bounds[0] = x
                    saw_char = True
            else:
                if pixels[x,y] == 0:
                    if x != imgX-1:
                        saw_char = True
                    else:
                        bounds[2] = x-1
                elif y == imgY-1 and not saw_char:
                    bounds[2] = x-1

        if bounds[0] != -1 and not saw_char:
            break

    # start y, end y
    for y in range(imgY):
        saw_char = False
        for x in range(imgX):
            if bounds[1] == -1:
                if pixels[x,y] == 0:
                    bounds[1] = y
                    saw_char = True
            else:
                if pixels[x,y] == 0:
                    if y != imgY-1:
                        saw_char = True
                    else:
                        bounds[3] = imgY-1
                elif x == imgX-1 and not saw_char:
                    bounds[3] = y-1

        if bounds[1] != -1 and not saw_char:
            break

    return bounds

def char_resize_square(path, new_path, side_len, highLo=None):
    """Crop image to character and save as square bitmap"""
    img = None
    if type(path) is str:
        img = Image.open(path).convert('L')
    else:
        img = path

    # Get bounds of character within the image
    bounds = get_char_bounds(img, highLo)

    # bad strip
    if -1 in bounds:
        return

    img = img.crop(tuple(bounds)).resize((side_len,side_len), Image.LANCZOS)
    img.convert('RGB').save(new_path)

def char_resize_area(path, new_path, area, highLo=None):
    """Crop image to character and save as bitmap with certain area and same width/height ratio"""
    img = None
    if type(path) is str:
        img = Image.open(path).convert('L')
    else:
        img = path

    # Get bounds of character within the image
    bounds = get_char_bounds(img, highLo)

    # bad strip
    if -1 in bounds:
        return    

    # Get the current ratio
    imgX = bounds[2] - bounds[0]
    imgY = bounds[3] - bounds[1]
    x_to_y = float(imgX) / float(imgY)

    # Get the new dimensions that will maintain the ratio with desired area
    newX = int(floor(sqrt(area) * x_to_y))
    if newX <= 0:
        newX = 1

    newY = int(floor(area / newX))
    if newY <= 0:
        newY = 1

    img = img.crop(tuple(bounds)).resize((newX, newY), Image.LANCZOS)
    img.convert('RGB').save(new_path)

def create_formatted(rawFolder, bmpFolder, area):
    """Convert images of characters to properly-formatted images"""
    clear_folder(bmpFolder)

    for char in listdir(rawFolder):
        i = 0
        for f in listdir(os.path.join(rawFolder, char)):
            raw_path = os.path.join(rawFolder, char, f)
            bmpPath = os.path.join(bmpFolder, char+str(i)+'.bmp')
            print(raw_path + ' --(area = ' + str(area) + ')-> ' + bmpPath)
            char_resize_square(raw_path, bmpPath, area)
            i += 1

    print('Training images prepared')

def find_chars(raw_path, found_folder, area, highLo=50):
    """Slice up an image into its separate characters"""
    clear_folder(found_folder)

    img = Image.open(raw_path).convert('L')
    imgX, imgY = img.size
    pixels = img.load()

    for y in range(imgY):
        for x in range(imgX):
            if pixels[x,y] <= highLo:
                pixels[x,y] = 0
            else:
                pixels[x,y] = 255

    bounds = [-1,0,imgX,imgY]
    i = 0
    for x in range(imgX):
        saw_char = False
        for y in range(imgY):
            if bounds[0] == -1:
                if pixels[x,y] == 0:
                    bounds[0] = x
                    saw_char = True
            else:
                if pixels[x,y] == 0:
                    saw_char = True
                elif y == imgY-1 and not saw_char:
                    bounds[2] = x-1

        if bounds[0] != -1 and not saw_char:
            i += 1
            char_resize_square(img.crop(tuple(bounds)), os.path.join(found_folder, str(i) + '.bmp'), area)
            bounds = [-1,0,imgX,imgY]

def get_grayscale_vals(img_file_path):
    img = Image.open(img_file_path).convert('L')
    grayscale_vals = [int(x) for x in list(img.getdata())]
    img.close()
    return grayscale_vals

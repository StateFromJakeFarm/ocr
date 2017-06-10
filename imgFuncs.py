from PIL import Image
from os import listdir
from basicFuncs import clear_folder
import os
import sys
import subprocess
import shutil
import glob

def make_char_square(path, new_path, side_len, highLo=None):
    """Crop image to character and save as square bitmap"""
    img = None
    if type(path) is str:
        img = Image.open(path).convert('L')
    else:
        img = path

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

    # bad strip
    if -1 in bounds:
        return

    img = img.crop(tuple(bounds)).resize((side_len,side_len), Image.LANCZOS)
    img.convert('RGB').save(new_path)

def create_formatted(rawFolder, bmpFolder, side_len):
    """Convert images of characters to properly-formatted images"""
    clear_folder(bmpFolder)

    for char in listdir(rawFolder):
        i = 0
        for f in listdir(os.path.join(rawFolder, char)):
            raw_path = os.path.join(rawFolder, char, f)
            bmpPath = os.path.join(bmpFolder, char+str(i)+'.bmp')
            print(raw_path + ' --(' + str(side_len) + 'x' + str(side_len) + ')-> ' + bmpPath + '                                                       ', end='\r')
            make_char_square(raw_path, bmpPath, side_len)
            i += 1

    print('\r                                                       \rTraining images prepared')

def full_img_bmp(raw_path, classify_folder, side_len, highLo):
    """Slice up an image into its separate characters"""
    clear_folder(classify_folder)

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
            make_char_square(img.crop(tuple(bounds)), os.path.join(classify_folder, str(i) + '.bmp'), side_len)
            bounds = [-1,0,imgX,imgY]

def get_grayscale_vals(img_file_path):
    img = Image.open(img_file_path).convert('L')
    grayscale_vals = [int(x) for x in list(img.getdata())]
    img.close()
    return grayscale_vals

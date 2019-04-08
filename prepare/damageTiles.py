from PIL import Image
import numpy as np
import cv2
import math
import os
import os.path as path
import sys


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
#ROOT_DIR = os.path.abspath("../")
sys.path.append(ROOT_DIR)

print(ROOT_DIR)
path = []
prueba1 = os.path.join(ROOT_DIR, "prueba1")
prueba2 = os.path.join(ROOT_DIR, "prueba2")

path = [prueba1, prueba2]

count = 0


def grabNamesImages():
    for file in path:
        files = os.listdir(file)
        for name in files:
            #imgs = []
            with open(file + '/image.txt', 'w') as f:
                for item in files:
                    if (item.endswith('.jpg')):
                        f.write("%s\n" % item)
            f.close()
        print("List of images, images.tx, was save in", file)


def load_image(filename):
    try:
        original = Image.open(filename)
        print("the size of the image is :")
        print(original.format,original.size)
        w, h = original.size
        size = w * h
        img = cv2.imread(filename)
        print(img.shape)
    except Exception as e:
        print(e)
        print ("Unable to load image")

    return size, img.shape, img


def size_tiles(num_pixels, w,h):
    num_tiles = int(round(num_pixels / (w * h)))
    num_tiles = max(1, num_tiles)
    #actual_tile_size = math.ceil(num_pixels / num_tiles)
    return num_tiles, w, h

def cutting_images(path,img_shape, offset, img ):
    for i in range(int(math.floor(img_shape[0] / (offset[1] * 1.0)))):
        for j in range(int(math.floor(img_shape[1] / (offset[0] * 1.0)))):
            start_y = offset[1] * i
            stop_y = offset[1] * (i + 1)
            start_x = offset[0] * j
            stop_x = offset[0] * (j + 1)
            cropped_img = img[start_y:stop_y,start_x:stop_x ]

            name =  (path + '/' + "tail" + str(i) + "_" + str(j) + ".png")
            if os.path.isfile(name):
                print("deleting an existent file --> dataset.json from /train")
                name = (path + '/' + "name" + str(i) + "_" + str(j) + ".png")
            cv2.imwrite(name, cropped_img)

def saving_images():
    print("saving-----")
    for dir in path:
        imgs_list = open(dir + '/image.txt', 'r').readlines()
        total = len(imgs_list)
        print(total)

        for img in imgs_list:
            if 'jpg' in img:
                #cutting_images(img_shape, offset, img)
                print("nice")

if __name__ == "__main__":

    grabNamesImages()

    for dir in path:
        imgs_list = open(dir + '/image.txt', 'r').readlines()

        for img in imgs_list:
            img_name = img.strip().split('/')[-1]
            filename = (dir +'/'+img_name)
            size, img_shape, img = load_image(filename)
            print("size : ",size)
            print("img_shape : ", img_shape)
            #print("img : ", img) #this is a full matrix of image

            num_tiles, w, h =  size_tiles(size, 1024, 1024)
            print("number of tile :",num_tiles)
            print("this is w :",w)
            print("this is h :", h)
            offset = (w, h)

            '''
            if not os.path.exists('prueba1/tails'):
                os.makedirs('prueba1/tails')
            '''

            cutting_images(dir, img_shape, offset, img)
            print('this is this image', filename)








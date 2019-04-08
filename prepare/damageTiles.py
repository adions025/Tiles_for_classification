from PIL import Image
import numpy as np
import cv2
import math
import os
import os.path as path


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

path = []
prueba1 = os.path.join(ROOT_DIR, "prueba1")
prueba2 = os.path.join(ROOT_DIR, "prueba2")
path = [prueba1, prueba2]
count = 0

img = "20180426_095752.jpg"

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
    except:
        print ("Unable to load image")
    return size, img.shape, img


def size_tiles(num_pixels, w,h):
    num_tiles = int(round(num_pixels / (w * h)))
    num_tiles = max(1, num_tiles)
    #actual_tile_size = math.ceil(num_pixels / num_tiles)
    return num_tiles, w, h

def cutting_images(img_shape, offset, img ):
    for i in range(int(math.floor(img_shape[0] / (offset[1] * 1.0)))):
        for j in range(int(math.floor(img_shape[1] / (offset[0] * 1.0)))):
            start_y = offset[1] * i
            stop_y = offset[1] * (i + 1)
            start_x = offset[0] * j
            stop_x = offset[0] * (j + 1)
            cropped_img = img[start_y:stop_y,start_x:stop_x ]
            cv2.imwrite("e_" + str(i) + "_" + str(j) + ".png", cropped_img)

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
            print(img)
            size, img_shape, img = load_image(img)
            print("size : ",size)
            print("img_shape : ", img_shape)
            #print("img : ", img) #this is a full matrix of image

            num_tiles, w, h =  size_tiles(size, 1024, 1024)
            print("number of tile :",num_tiles)
            print("this is w :",w)
            print("this is h :", h)
            offset = (w, h)
            cutting_images(img_shape, offset, img)





    print("saving-----")
    '''
    for dir in path:
        imgs_list = open(dir + '/image.txt', 'r').readlines()
        total = len(imgs_list)
        print(total)

        for img in imgs_list:
            if 'jpg' in img:
                # cutting_images(img_shape, offset, img)
                print("nice")
                cutting_images(img_shape, offset, img)
    '''


'''
image = Image.open('20180426_095752.jpg')
image.thumbnail((1024, 1024), Image.ANTIALIAS)
image.save('20180426_095752_resized2.jpg', 'JPEG', quality=88)
'''

'''

img = cv2.imread("20180426_095752_resized2.jpg")
img_shape = img.shape
print(img_shape)
tile_size = (256, 256)
offset = (256, 256)
'''



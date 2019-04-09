from PIL import Image
import numpy as np
import cv2
import math
import os
import os.path as path
import sys
import xml.etree.cElementTree as ET



ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
#ROOT_DIR = os.path.abspath("../")
sys.path.append(ROOT_DIR)

print(ROOT_DIR)
path = []
prueba1 = os.path.join(ROOT_DIR, "prueba1")
prueba2 = os.path.join(ROOT_DIR, "prueba2")

path = [prueba1, prueba2]

count = 0
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


def size_tiles(num_pixels, w,h):
    num_tiles = int(round(num_pixels / (w * h)))
    num_tiles = max(1, num_tiles)
    #actual_tile_size = math.ceil(num_pixels / num_tiles)
    return num_tiles, w, h

def cutting_images(path,img_shape, offset, img ):
    for i in range(int(math.floor(img_shape[0] / (offset[1] * 1.0)))):
        for j in range(int(math.floor(img_shape[1] / (offset[0] * 1.0)))):
            start_y = offset[1] * i #1024 * 0 = 0
            stop_y = offset[1] * (i + 1) #1024 * (0+1) = 1024
            start_x = offset[0] * j #1024 * 0 = 0
            stop_x = offset[0] * (j + 1) # 1024 *(1) 1024
            cropped_img = img[start_y:stop_y,start_x:stop_x ]

            name =  (path + '/' + "tail" + str(i) + "_" + str(j) + ".png")
            if os.path.isfile(name):
                print("exist this files")
                name = (path + '/' + "name" + str(i) + "_" + str(j) + ".png")
            cv2.imwrite(name, cropped_img)

def finding_annotations(path,img_shape, offset, img ,xmin, xmax, ymin, ymax):
    for i in range(int(math.floor(img_shape[0] / (offset[1] * 1.0)))):
        for j in range(int(math.floor(img_shape[1] / (offset[0] * 1.0)))):
            start_y = offset[1] * i
            stop_y = offset[1] * (i + 1)
            start_x = offset[0] * j
            stop_x = offset[0] * (j + 1)
            '''
            print("-----cccccc----")
            print("this is start_y: ", start_y)
            print("this is stop_y: ", stop_y)
            print("this is start_x: ", start_x)
            print("this is stop_x: ", stop_x)
            new = img[start_y:stop_y, start_x:stop_x]
            print("aa")
            #print(new)
            print("----cccccccccc-----")
            print(xmin, xmax)
            '''
            '''
            for i in (img[start_y:stop_y]):
                for j in (img[start_x:stop_x]):
            '''


            '''
            if(xmin < start_x and xmin < start_y and ymin < start_x and ymin < start_y or xmin < stop_x and xmin <stop_y\
                    and ymin < stop_x and ymin < stop_y):
                print("yes we are inside")

            if(xmin < start_x and xmin < start_y and ymin < start_x and ymin < start_y or xmin < stop_x and xmin <stop_y\
                    and ymin < stop_x and ymin < stop_y):
                print("yes we are inside")

            if(xmax < stop_x and xmax < stop_y and ymax < stop_x and ymax < stop_y and xmax > start_x and xmax > start_y\
                    and ymax> start_x and ymax>start_y):
                print("we are inside 2")

            '''
            first = (xmin, ymin)
            second= (xmin, ymax)
            third = (xmax, ymin)
            fourth = (xmax, ymax)


            t_first = (start_x, start_y)
            t_second = (start_x, stop_y)
            t_third = (stop_x, start_y)
            t_fourth = (stop_x, stop_y)
            print("---------------------------------------------------------------------------------")
            print("tile: ", [i],[j])
            print("here start ananotations points---")


            print(first)
            print(second)
            print(third)
            print(fourth)

            print("here start tiles points---")

            print(t_first)
            print(t_second)
            print(t_third)
            print(t_fourth)

            if(start_x < xmax) and (stop_x>xmin) and (start_y < ymax) and (stop_y > ymin):
                print("here_adonis")

            print("---------------------------------------------------------------------------------")

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

            namexml = (img_name.split('.jpg')[0])
            xml_n = namexml + '.xml'

            print("this is xml_n: ", xml_n)

            tree = ET.ElementTree(file=dir + '/' + xml_n)
            root = tree.getroot()
            counterObject, xmin, xmax, ymin, ymax = {}, {}, {}, {}, {}

            for child_of_root in root:
                if child_of_root.tag == 'object':
                    for child_of_object in child_of_root:
                        if child_of_object.tag == 'name':
                            category_id = child_of_object.text
                            print("this is the damage: ", category_id)

                        if child_of_object.tag == 'bndbox':
                            for child_of_root in child_of_object:
                                if child_of_root.tag == 'xmin':
                                    xmin[category_id] = int(child_of_root.text)
                                    print("this is de xmin: ", xmin[category_id])

                                if child_of_root.tag == 'xmax':
                                    xmax[category_id] = int(child_of_root.text)
                                    print("this is de xmax: ", xmax[category_id])


                                if child_of_root.tag == 'ymin':
                                    ymin[category_id] = int(child_of_root.text)
                                    print("this is de ymin: ", ymin[category_id])


                                if child_of_root.tag == 'ymax':
                                    ymax[category_id] = int(child_of_root.text)
                                    print("this is de ymax: ", ymax[category_id])


                    finding_annotations(dir, img_shape, offset, img,xmin[category_id],xmax[category_id],ymin[category_id],ymax[category_id])







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
            #cv2.imwrite(name, cropped_img)

def finding_annotations(path,img_shape, offset, img ,xmin, xmax, ymin, ymax):
    for i in range(int(math.floor(img_shape[0] / (offset[1] * 1.0)))):
        for j in range(int(math.floor(img_shape[1] / (offset[0] * 1.0)))):
            start_y = offset[1] * i
            print("---------")
            print( "this is start_y: ",start_y)
            print("---------")

            stop_y = offset[1] * (i + 1)
            print("---------")
            print("this is stop_y: ", stop_y)
            print("---------")

            start_x = offset[0] * j

            print("---------")
            print("this is start_x: ", start_x)
            print("---------")

            stop_x = offset[0] * (j + 1)

            print("---------")
            print("this is stop_x: ", stop_x)
            print("---------")
            print(xmin, xmax)
            if(xmin >= start_x and xmin >= start_y and ymin >= start_x and ymin >= start_y ):
                print("si entro")
            if(xmin,ymin) >= (start_x,start_y):
                print("entra")
            print("q pasa :",(xmin, ymin),(start_x, start_y))

            if(xmax<= stop_x and xmax<=start_y and ymin<=stop_x and ymin<=start_y):
                print("si entro 2")

            if (xmax,ymin) <= (stop_x,start_y):
                print("entra 2")

            print("q pasa 2: ",(xmax, ymin),(stop_x, start_y))

            if(xmin>=stop_x and xmin>=stop_y and ymax>=start_x and ymax>=stop_y):
                print("si entro 3")

            if(xmax<=stop_x and xmax<= stop_y and ymax <= stop_x and ymax<=stop_y):
                print("si entro 4")

            if (xmin,ymin) >= (start_x,start_y) and (xmax,ymin) <= (stop_x,start_y) \
                    or (xmin,ymax) >= (start_x,stop_y) and (xmax,ymax) <= (stop_x,stop_y):
                print("manono")
                cropped_img = img[start_y:stop_y,start_x:stop_x ]
                name = (path + '/' + "tail" + str(i) + "_" + str(j) + ".png")
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

            num_tiles, w, h =  size_tiles(size, 2000, 2000)
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
                                    print("this is de xmiX: ", xmax[category_id])


                                if child_of_root.tag == 'ymin':
                                    ymin[category_id] = int(child_of_root.text)
                                    print("this is de ymin: ", ymin[category_id])


                                if child_of_root.tag == 'ymax':
                                    ymax[category_id] = int(child_of_root.text)
                                    print("this is de ymax: ", ymax[category_id])


                    finding_annotations(dir, img_shape, offset, img,xmin[category_id],xmax[category_id],ymin[category_id],ymax[category_id])







'''
damageTiles.py

Tiles the image and for each tile, it will calculate if there is an annotation
inside, it makes use of the functions of "min of the maxes"and "max of the min",
from here we detect, if we have annotation in tile, and that percentage of annotation
in the tile, and create different folders for each type of these annotations.


Written by Adonis Gonzalez
------------------------------------------------------------

usage:
$ python damageTiles.py [-h] [--weight N] [--height N] [--threshold N]

 default values
 1  weight = 1500
 2. height = 1500
 3. threshold = 10

'''


from PIL import Image
import numpy as np
import cv2
import math
import os
import os.path as path
import sys
import xml.etree.cElementTree as ET
import argparse


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(ROOT_DIR)

print(ROOT_DIR)
path = []
#folder1 = os.path.join(ROOT_DIR, "prueba1")
folder2 = os.path.join(ROOT_DIR, "all")

path = [folder2]

def load_image(filename):
    """Loads an image, reads it and returns image size,
        dimension and a numpy array of this image.

    filename: the name of the image
    """
    try:
        img = cv2.imread(filename)
        print("(H, W, D) = (height, width, depth)")
        print("shape: ",img.shape)
        h, w, d = img.shape
        #size = h * w
    except Exception as e:
        print(e)
        print ("Unable to load image")

    return img.shape, img


def size_tiles(img_shape, offset):
    """Calculates the total number of tiles in an image, rounding down, which
       means that incomplete tiles will not be taken into the calculation.

    img_shape: is the dimension of the image (H,W,D), i dont use depth.
    offset: is heigh and weigth given, [0][1] as tuple.
    """
    num_tiles_w = (int(math.floor(img_shape[0] / (offset[1] * 1.0))))
    num_tiles_h = (int(math.floor(img_shape[1] / (offset[0] * 1.0))))
    num_tiles = num_tiles_h * num_tiles_w
    return num_tiles


def tiling_images(path,img_shape, offset, img ,xmin, xmax, ymin, ymax, name_damage, img_name,threshold,dic_damages):
    """Cut the images in diferents tails,
       the size of each tile is given by agurment or paramenter - in this case offset[0],[1]
       And, in the same iteration is checking on each tile if there is annotation (damage), is this is True
       creates a folder(s) for each type of damage, but also checks the percentage of annotation inside of
       each tile, with the threshold given or using default value = 10 is compared if the annotation in the
       tile is lower than the value of threshold, in case to be True, proceeds to create a folder for
       small damages, if it is greater creates a folder and saves the images with annotations in their
       corresponding folder. In the last case if there is no damage or annotation in the tile, it is saved
       in a folder no_damage.

    path: in this path it will be save the image.
    img_shape: is the dimension of the image (H,W,D), i dont use depth.
    offset: is heigh and weigth given, [0][1] as tuple.
    img: array of the image.
    xmin, xmax, ymin, ymax : coordinates in xml file (annotations).
    name_damage: given in xml file.
    img_name: the name how it will be save it.
    threshold: a value given to separate small damage in other folders  10 per default.
    """

    for i in range(int(math.floor(img_shape[0] / (offset[1] * 1.0)))):
        for j in range(int(math.floor(img_shape[1] / (offset[0] * 1.0)))):

            start_y = offset[1] * i #1024 * 0 = 0
            stop_y = offset[1] * (i + 1) #1024 * (0+1) = 1024
            start_x = offset[0] * j #1024 * 0 = 0
            stop_x = offset[0] * (j + 1) # 1024 *(0+1)= 1024
            cropped_img = img[start_y:stop_y,start_x:stop_x ]
            #------------------------------------------#

            tmp_w = min(stop_x, xmax) - max(start_x,xmin)
            tmp_h = min(stop_y, ymax) - max(start_y,ymin)
            annotation_dim =  (tmp_w * tmp_h)
            tile_dim = offset[0] * offset[1]

            tile_percent = (float(annotation_dim) / float(tile_dim))
            thresh = (tile_percent * 100)
            #-------------------------------------------#
            one_damage = (path + "/" + name_damage + '/' + img_name + str(i) + "_" + str(j) + ".jpg")
            multi_damage = (path + "/" + "mutiple_damage" + '/' + img_name + str(i) + "_" + str(j) + ".jpg")
            small_damage = (path + "/" + "small_damage" + '/' + img_name + str(i) + "_" + str(j) + ".jpg")
            no_damage = (path + '/' + "no_damage" + '/' + img_name + str(i) + "_" + str(j) + ".jpg")

            #two annotations or mor
            if (len(total_annotation) > 1):
                if (tmp_w >= 0) and (tmp_h >= 0):  # check is there is annotations
                    if (thresh > threshold):  #percentage of threshold is bigger
                        if (i, j) in dic_damages:  # more thant one damage
                            if dic_damages[(i, j)] == name_damage:  # 2 damages == same type
                                if not os.path.exists(path + "/" + name_damage):
                                    os.mkdir(path + "/" + name_damage)
                                    print("folder created: ", name_damage)
                                    cv2.imwrite(one_damage, cropped_img)
                                else:
                                    cv2.imwrite(one_damage, cropped_img)
                            if dic_damages[(i, j)] != name_damage:  # 2 damages != different type
                                print("different damage")
                                if not os.path.exists(path + "/" + "mutiple_damage"):
                                    os.mkdir(path + "/" + "mutiple_damage")
                                    print("folder created: ", "mutiple_damage")
                                    cv2.imwrite(multi_damage, cropped_img)
                                else:
                                    cv2.imwrite(multi_damage, cropped_img)
                        if (len(total_annotation) > 1) and not (i, j) in dic_damages:
                            dic_damages[(i, j)] = name_damage
                            print(dic_damages[(i, j)])
                    # small damage
                    if (tmp_w >= 0) and (tmp_h >= 0) and thresh < threshold:
                        if not os.path.exists(path + "/" + "small_damage"):
                            os.mkdir(path + "/" + "small_damage")
                            print("folder created: ", "small_damage")
                            cv2.imwrite(small_damage, cropped_img)
                        else:
                            cv2.imwrite(small_damage, cropped_img)

            #only one annotation
            if (len(total_annotation) == 1):
                if (thresh > 1):
                    if (tmp_w >= 0) and (tmp_h >= 0):
                        if not os.path.exists(path + "/" + name_damage):
                            os.mkdir(path + "/" + name_damage)
                            print("folder created: ", name_damage)
                            cv2.imwrite(one_damage, cropped_img)
                        else:
                            cv2.imwrite(one_damage, cropped_img)

                    if not (tmp_w >= 0) and not (tmp_h >= 0):
                        if not os.path.exists(path + "/" + "no_damage"):
                            os.mkdir(path + "/" + "no_damage")
                            print("folder created: ", "no_damage")
                            cv2.imwrite(no_damage, cropped_img)
                        else:
                            cv2.imwrite(no_damage, cropped_img)
                else:

                    if not os.path.exists(path + "/" + "small_damage"):
                        os.mkdir(path + "/" + "small_damage")
                        print("folder created: ", "small_damage")
                        cv2.imwrite(small_damage, cropped_img)
                    else:
                        cv2.imwrite(small_damage, cropped_img)

            #no annotation, no damage
            if not (tmp_w >= 0) and not (tmp_h >= 0):
                if not os.path.exists(path + "/" + "no_damage"):
                    os.mkdir(path + "/" + "no_damage")
                    print("folder created: ", "no_damage")
                    cv2.imwrite(no_damage, cropped_img)
                else:
                    cv2.imwrite(no_damage, cropped_img)


def couting_annotations_in_tiles(path,img_shape, offset, img ,xmin, xmax, ymin, ymax, name_damage, img_name,threshold,dic_damages, total_annotation,dic_damages2,dic_damages3 ):
    dic_4 = {}
    for i in range(int(math.floor(img_shape[0] / (offset[1] * 1.0)))):
        for j in range(int(math.floor(img_shape[1] / (offset[0] * 1.0)))):
            start_y = offset[1] * i
            stop_y = offset[1] * (i + 1)
            start_x = offset[0] * j
            stop_x = offset[0] * (j + 1)
            tmp_w = min(stop_x, xmax) - max(start_x, xmin)
            tmp_h = min(stop_y, ymax) - max(start_y, ymin)

            print("---------------------------------------------------------------------------------")
            print("tile: ", [i],[j])
            if (tmp_w >= 0) and (tmp_h >= 0):
                #dic_damages3[(i, j)] = name_damage
                #dic_damages3.update({name_damage:([i,j])})
                #dic_damages2= dic_damages2(zip(name_damage,[(i,j)]))
                dic_4[(i, j)] = name_damage
                dic_4 = dic_4.copy()

            print("---------------------------------------------------------------------------------")
    dic_damages2[name_damage] = dic_4.copy().keys()
    print(dic_damages2)


    for key, val in dic_damages2.items():
        print("manolos")
        print (key, "=>", val)


def debug_tiles(path,img_shape, offset, img ,xmin, xmax, ymin, ymax, name_damage, img_name,threshold,dic_damages, total_annotation):
    """This function allow debug each tile.

    img_shape: is the dimension of the image (H,W,D), i dont use depth
    offset: is heigh and weigth given, [0][1] as tuple
    img: array of the image
    xmin, xmax, ymin, ymax : coordinates in xml file (annotations)
    name_damage: given in xml file
    img_name: the name how it will be save it
    """

    for i in range(int(math.floor(img_shape[0] / (offset[1] * 1.0)))):
        for j in range(int(math.floor(img_shape[1] / (offset[0] * 1.0)))):
            start_y = offset[1] * i
            stop_y = offset[1] * (i + 1)
            start_x = offset[0] * j
            stop_x = offset[0] * (j + 1)

            #------------------------------------------#
            tmp_w = min(stop_x, xmax) - max(start_x,xmin)
            tmp_h = min(stop_y, ymax) - max(start_y,ymin)

            tmp_w_h =  tmp_w * tmp_h
            first_mul =(stop_x - start_x)
            second_mul = (stop_y - start_y)
            tmp_m = first_mul * second_mul
            # ------------------------------------------#
            cropped_img = img[start_y:stop_y, start_x:stop_x]

            print("---------------------------------------------------------------------------------")
            print("tile: ", [i],[j])
            print(len(total_annotation))
            p = (float(tmp_w_h) / float(tmp_m))
            th = p * 100
            if (tmp_w >= 0) and (tmp_h >= 0): #compruebo si hay anotacin
                    print("--->>>>>>IN THIS TILE THERE IS DAMAGE<<<<<<<----")

            print("---------------------------------------------------------------------------------")



def saving_only_annotations(path,img ,xmin, xmax, ymin, ymax,name_damage, img_name):
    """save only the annotation, this is only if you want to check where is exactly
       the annotation in you image, using xml coordinates.

    path: in this path it will be save the image
    img: array of the image
    xmin, xmax, ymin, ymax : coordinates in xml file (annotations)
    name_damage: given in xml file
    img_name: the name how it will be save it
    """
    name = (path + '/'+ name_damage+"_"+img_name+ "adionis_.jpg")
    annotation = img[ymin:ymax, xmin:xmax]
    cv2.imwrite(name, annotation)
    print("saving image")


def grab_images(path):
    """"makes a list of the files in each of the paths given, paths [ ]is a list of
        directories, reads these and searches for images with jpg extension, also saves
        this list in a file images.txt in each of those paths.
    """
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
        print("---------------------------------------------------------------------------------")
        print("--INFO IMAGE                                                                   --")
        print("---------------------------------------------------------------------------------")


if __name__ == "__main__":


    WEIGHT = 1000
    HEIGHT = 1000
    THRESHOLD = 1

    parser = argparse.ArgumentParser(description='_Process dataset_')
    parser.add_argument('--weight',required=False,
                        default=WEIGHT,
                        metavar="N",
                        type=int,
                        help='weigth 1500')

    parser.add_argument('--height', required=False,
                        default=HEIGHT,
                        metavar="N",
                        type=int,
                        help='height 1500')

    parser.add_argument('--threshold', required=False,
                        default=THRESHOLD,
                        metavar="N",
                        type=int,
                        help='threshold < 10, percentage damage in tile lower than 10 will save'
                             'in small_damage')

    args = parser.parse_args()
    grab_images(path)

    for dir in path:
        imgs_list = open(dir + '/image.txt', 'r').readlines()

        for img in imgs_list:
            dic_damages = {}#saving (i,j):name_damage //to check is there is two damage
            dic_damages2 = {}
            dic_damages3 ={}
            img_name = img.strip().split('/')[-1]
            filename = (dir +'/'+img_name)
            img_shape, img = load_image(filename)
            offset = (args.weight, args.height)
            num_tiles =  size_tiles(img_shape, offset)

            print("number of tile :",num_tiles)
            print("this is widgth tile :", args.weight)
            print("this is heigth tile :", args.height)
            print('this is this image', filename)

            only_img = (img_name.split('.jpg')[0])
            xml_n = only_img + '.xml'


            tree = ET.ElementTree(file=dir + '/' + xml_n)
            root = tree.getroot()
            xmin, xmax, ymin, ymax = {}, {}, {}, {}
            total_annotation = []

            #check the number of annotation for each image
            for child_of_root in root:
                if child_of_root.tag == 'object':
                    for child_of_object in child_of_root:
                        if child_of_object.tag == 'name':
                            name = child_of_object.text
                            total_annotation.append(name)

            #start iterate for each annotation
            for child_of_root in root:
                if child_of_root.tag == 'object':
                    for child_of_object in child_of_root:
                        if child_of_object.tag == 'name':
                            category_id = child_of_object.text
                            name_damage=(category_id.split(' ')[0]) #just for use SD intead SD1 levels
                            print("------------------")
                            print("INFO-ANNOTATION")
                            print("------------------")
                            print("this is the damage: ", name_damage)
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

                    tiling_images(dir, img_shape, offset, img, xmin[category_id], xmax[category_id],
                                  ymin[category_id], ymax[category_id], name_damage, only_img, THRESHOLD, dic_damages)


                    #couting_annotations_in_tiles(dir, img_shape, offset, img,xmin[category_id],xmax[category_id],ymin[category_id],
                     #           ymax[category_id],name_damage, only_img,THRESHOLD, dic_damages, total_annotation,dic_damages2, dic_damages3)



                    #debug_tiles(dir, img_shape, offset, img,xmin[category_id],xmax[category_id],ymin[category_id],
                     #           ymax[category_id],name_damage, only_img,THRESHOLD, dic_damages, total_annotation)



                    #saving_only_annotations(dir, img,xmin[category_id],xmax[category_id],
                     #                   ymin[category_id],ymax[category_id],name_damage, only_img)





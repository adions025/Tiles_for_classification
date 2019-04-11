'''
damageTiles.py

Written by Adonis Gonzalez
------------------------------------------------------------

Usage:
$ usage: damageTiles.py [--weight N] [--height N]

 default values
 1  weight = 1500
 2. height = 1500
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
#ROOT_DIR = os.path.abspath("../")
sys.path.append(ROOT_DIR)

print(ROOT_DIR)
path = []
#folder1 = os.path.join(ROOT_DIR, "prueba1")
folder2 = os.path.join(ROOT_DIR, "prueba2")

path = [folder2]

def load_image(filename):
    try:
        img = cv2.imread(filename)
        print("(H, W, D) = (height, width, depth)")
        print("shape: ",img.shape)
        h, w, d = img.shape
        size = h * w
        #print(img.shape)
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
        print("---------------------------------------------------------------------------------")
        print("--INFO IMAGE                                                                   --")
        print("---------------------------------------------------------------------------------")



def size_tiles(num_pixels, w,h):
    num_tiles = int(round(math.floor(num_pixels / (w * h))))
    num_tiles = max(1, num_tiles)
    #actual_tile_size = math.ceil(num_pixels / num_tiles)
    #num_tiles = math.floor(num_pixels / num_tiles)
    return num_tiles, w, h

def cutting_images(path,img_shape, offset, img ,xmin, xmax, ymin, ymax, name_damage, img_name):
    for i in range(int(math.floor(img_shape[0] / (offset[1] * 1.0)))):
        for j in range(int(math.floor(img_shape[1] / (offset[0] * 1.0)))):
            start_y = offset[1] * i #1024 * 0 = 0
            stop_y = offset[1] * (i + 1) #1024 * (0+1) = 1024
            start_x = offset[0] * j #1024 * 0 = 0
            stop_x = offset[0] * (j + 1) # 1024 *(0+1)= 1024
            cropped_img = img[start_y:stop_y,start_x:stop_x ]

            if (start_x < xmax) and (stop_x > xmin) and (start_y < ymax) and (stop_y > ymin):
                print("here_adonis")
                if not os.path.exists(path+"/"+name_damage):
                    os.mkdir(path+"/"+name_damage)
                    print("folder created: ",name_damage)
                    name = (path+"/"+name_damage + '/' + img_name  + str(i) + "_" + str(j) + ".jpg")
                    cv2.imwrite(name, cropped_img)
                else:
                    name = (path+"/"+name_damage + '/' +img_name +  str(i) + "_" + str(j) + ".jpg")
                    cv2.imwrite(name, cropped_img)
            else:
                if not os.path.exists(path + "/" + "no_damage"):
                    os.mkdir(path + "/" + "no_damage")
                    name = (path + '/'+"no_damage" +  '/'+img_name + str(i) + "_" + str(j) + ".jpg")
                    cv2.imwrite(name, cropped_img)
                else:
                    name = (path + '/' + "no_damage" + '/' + img_name  + str(i) + "_" + str(j) + ".jpg")
                    cv2.imwrite(name, cropped_img)


def debug_tiles(path,img_shape, offset, img ,xmin, xmax, ymin, ymax):

    for i in range(int(math.floor(img_shape[0] / (offset[1] * 1.0)))):
        for j in range(int(math.floor(img_shape[1] / (offset[0] * 1.0)))):
            start_y = offset[1] * i
            stop_y = offset[1] * (i + 1)
            start_x = offset[0] * j
            stop_x = offset[0] * (j + 1)

            #annotation points
            first = (xmin, ymin)
            #first = [xmin, ymin]
            second= (xmin, ymax)
            third = (xmax, ymin)
            fourth = (xmax, ymax)

            '''
            
            1)              3)
            |---------------|
            |               |
            |               |    
            |---------------|
            2)              4)
        
            '''
            #tiles points
            t_first = (start_x, start_y)
            t_second = (start_x, stop_y)
            t_third = (stop_x, start_y)
            t_fourth = (stop_x, stop_y)

            dim_tile = offset[0] * offset[1]
            annotation = img[ymin:ymax, xmin:xmax] #this is the annotation
            cropped_img = img[start_y:stop_y, start_x:stop_x]#it works - [each tile of the image]
            cropped_annotation_left = img[ymin:ymax, xmin:stop_x]#it works [if]
            cropped_annotation_right = img[ymin:ymax, start_x:xmax]#it works

            h_annotation_l = cropped_annotation_left.shape[0]
            w_annotation_l = cropped_annotation_left.shape[1]
            dim_annotation_l = (h_annotation_l * w_annotation_l)
            percent_tile_l = ((dim_annotation_l * 100)/dim_tile)

            h_annotation_r = cropped_annotation_right.shape[0]
            w_annotation_r = cropped_annotation_right.shape[1]
            dim_annotation_r = (h_annotation_r * w_annotation_r)
            percent_tile_r = ((dim_annotation_r * 100)/dim_tile)

            #------------------------------------------#
            tmp_w = min(stop_x, xmax) - max(start_x,xmin)
            tmp_h = min(stop_y, ymax) - max(start_y,ymin)

            tmp_w_h =  tmp_w * tmp_h
            first_mul =(stop_x - start_x)
            second_mul = (stop_y - start_y)

            tmp_m = first_mul * second_mul




            print("---------------------------------------------------------------------------------")
            print("tile: ", [i],[j])

            if (tmp_w >= 0) and (tmp_h >= 0):
                p = (float(tmp_w_h) / float(tmp_m))
                print("here")
                print(p)
                print(tmp_w)
                print(tmp_h)
                print("this is w* h", tmp_w_h)
                print("this is tmp_m = first_mul * second_mul", tmp_m)

            print("shape of tile", cropped_img.shape)
            print("Ano in 1 tile_left", cropped_annotation_left.shape)
            print("Ano in 1 tile_rigth", cropped_annotation_right.shape)

            print("size of tile in this annotation: ", dim_annotation_l)
            print("percentage of anno in 1 tile    :", percent_tile_l)
            print("percentage of anno in 2 tile    :", percent_tile_r)

            print("----here start ananotations points---")
            print(first)
            print(second)
            print(third)
            print(fourth)
            print("---here start tiles points---")
            print(t_first)
            print(t_second)
            print(t_third)
            print(t_fourth)

            #annotation = img[ymin:ymax, xmin:xmax]

            #print(np.array(annotation,cropped_img))

            #if (annotation.all() == cropped_img.all()):
             #   print("son iguel")

            if (start_x < xmax) and (stop_x > xmin) and (start_y < ymax) and (stop_y > ymin):
                print("--->>>>>>IN THIS TILE THERE IS DAMAGE<<<<<<<----")
            print("---------------------------------------------------------------------------------")



def saving_only_annotations(path,img ,xmin, xmax, ymin, ymax,name_damage, img_name):
    name = (path + '/'+ name_damage+"_"+img_name+ "adionis_.jpg")
    annotation = img[ymin:ymax, xmin:xmax]
    cv2.imwrite(name, annotation)
    print("saving image")




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



    #weight, height = argv
    WEIGHT = 1000
    HEIGHT = 1000

    parser = argparse.ArgumentParser(description='Process dataset for image classification')

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
    '''
    parser.add_argument('--threshold', required=False,
                        default=HEIGHT,
                        metavar="N",
                        type=int,
                        help='threshold < 10')
    '''



    args = parser.parse_args()

    grabNamesImages() # this is for create a imagelist.txt

    for dir in path:
        imgs_list = open(dir + '/image.txt', 'r').readlines()

        for img in imgs_list:
            img_name = img.strip().split('/')[-1]
            filename = (dir +'/'+img_name)
            size, img_shape, img = load_image(filename)
            print("number of pixels: ",size)
            #print("img : ", img) #this is a full matrix of image

            num_tiles, w, h =  size_tiles(size, args.weight, args.height)

            print("number of tile :",num_tiles)
            print("this is widgth tile :", w)
            print("this is heigth tile :", h)
            offset = (w, h)

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
                            name_damage=(category_id.split(' ')[0]) #just for use SD intead SD1 levels
                            print("------------------")
                            print("INFO-ANNOTATION")
                            print("------------------")
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


                    debug_tiles(dir, img_shape, offset, img,xmin[category_id],xmax[category_id],
                                        ymin[category_id],ymax[category_id])

                    cutting_images(dir, img_shape, offset, img, xmin[category_id], xmax[category_id],
                                         ymin[category_id], ymax[category_id], name_damage, img_name)

                    #saving_only_annotations(dir, img,xmin[category_id],xmax[category_id],
                     #                   ymin[category_id],ymax[category_id],name_damage, namexml)





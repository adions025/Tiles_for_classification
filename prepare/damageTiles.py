'''
damageTiles.py



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
folder2 = os.path.join(ROOT_DIR, "full")

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


def cutting_images(path,img_shape, offset, img ,xmin, xmax, ymin, ymax, name_damage, img_name,threshold):
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

            #if (start_x < xmax) and (stop_x > xmin) and (start_y < ymax) and (stop_y > ymin):
            if (tmp_w >= 0) and (tmp_h >= 0) and thresh > threshold:

                if not os.path.exists(path+"/"+name_damage):
                    os.mkdir(path+"/"+name_damage)
                    print("folder created: ",name_damage)
                    name = (path+"/"+name_damage + '/' + img_name  + str(i) + "_" + str(j) + ".jpg")
                    cv2.imwrite(name, cropped_img)
                else:
                    name = (path+"/"+name_damage + '/' +img_name +  str(i) + "_" + str(j) + ".jpg")
                    cv2.imwrite(name, cropped_img)

            elif (tmp_w >= 0) and (tmp_h >= 0) and thresh < threshold:

                if not os.path.exists(path+"/"+"small_damage"):
                    os.mkdir(path+"/"+"small_damage")
                    print("folder created: ","small_damage")
                    name = (path+"/"+"small_damage" + '/' + img_name  + str(i) + "_" + str(j) + ".jpg")
                    cv2.imwrite(name, cropped_img)
                else:
                    name = (path+"/"+"small_damage" + '/' +img_name +  str(i) + "_" + str(j) + ".jpg")
                    cv2.imwrite(name, cropped_img)

            else:

                if not os.path.exists(path + "/" + "no_damage"):
                    os.mkdir(path + "/" + "no_damage")
                    print("folder created: ","no_damage")
                    name = (path + '/' + "no_damage" + '/' + img_name + str(i) + "_" + str(j) + ".jpg")
                    cv2.imwrite(name, cropped_img)
                else:
                    name = (path + '/' + "no_damage" + '/' + img_name + str(i) + "_" + str(j) + ".jpg")
                    cv2.imwrite(name, cropped_img)
                print("hola")



def debug_tiles(img_shape, offset, img ,xmin, xmax, ymin, ymax):
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
            '''
            
            cropped_annotation_right = img[ymin:ymax, start_x:xmax]#it works
            h_annotation_l = cropped_annotation_left.shape[0]
            w_annotation_l = cropped_annotation_left.shape[1]
            dim_annotation_l = (h_annotation_l * w_annotation_l)
            percent_tile_l = ((dim_annotation_l * 100)/dim_tile)

            h_annotation_r = cropped_annotation_right.shape[0]
            w_annotation_r = cropped_annotation_right.shape[1]
            dim_annotation_r = (h_annotation_r * w_annotation_r)
            percent_tile_r = ((dim_annotation_r * 100)/dim_tile)
            
            '''
            #------------------------------------------#
            tmp_w = min(stop_x, xmax) - max(start_x,xmin)
            tmp_h = min(stop_y, ymax) - max(start_y,ymin)

            tmp_w_h =  tmp_w * tmp_h
            first_mul =(stop_x - start_x)
            second_mul = (stop_y - start_y)

            tmp_m = first_mul * second_mul
            print("this is min(stop_x, xmax)", stop_x, xmax)
            print("this is max(start_x, xmin)", start_x, xmin)

            print("this is min(stop_y, ymax)", (stop_y, ymax))
            print("this is max(start_y,ymin)", (start_y,ymin))

            print(first_mul)

            print("---------------------------------------------------------------------------------")
            print("tile: ", [i],[j])

            if (tmp_w >= 0) and (tmp_h >= 0):

                p = (float(tmp_w_h) / float(tmp_m))
                th = p * 100

                if (th > 10):
                    print("es mayor que 10")
                print("here")
                print("Percentage of annotation in tile = ", p*100)
                print("wigth of annotation in tile", tmp_w)
                print("heigth of annotation in tile", tmp_h)
                print("this is w * h", tmp_w_h)
                print("this is tmp_m = first_mul * second_mul", tmp_m)

            print("shape of tile", cropped_img.shape)
            print("Ano in 1 tile_left", cropped_annotation_left.shape)

            if (start_x < xmax) and (stop_x > xmin) and (start_y < ymax) and (stop_y > ymin):
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


def grabNamesImages():
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


    WEIGHT = 1000
    HEIGHT = 1000
    THRESHOLD = 1

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

    parser.add_argument('--threshold', required=False,
                        default=THRESHOLD,
                        metavar="N",
                        type=int,
                        help='threshold < 10, percentage damage in tile lower than 10 will save'
                             'in small_damage')

    args = parser.parse_args()
    grabNamesImages() # this is for create a imagelist.txt

    for dir in path:
        imgs_list = open(dir + '/image.txt', 'r').readlines()

        for img in imgs_list:
            img_name = img.strip().split('/')[-1]
            filename = (dir +'/'+img_name)
            img_shape, img = load_image(filename)
            #print("img : ", img) #this is a full matrix of image
            print(type(img))
            offset = (args.weight, args.height)
            num_tiles =  size_tiles(img_shape, offset)

            print("number of tile :",num_tiles)
            print("this is widgth tile :", args.weight)
            print("this is heigth tile :", args.height)


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


                    debug_tiles(img_shape, offset, img,xmin[category_id],xmax[category_id],
                                        ymin[category_id],ymax[category_id])

                    cutting_images(dir, img_shape, offset, img, xmin[category_id], xmax[category_id],
                                         ymin[category_id], ymax[category_id], name_damage, img_name,THRESHOLD)

                    #saving_only_annotations(dir, img,xmin[category_id],xmax[category_id],
                     #                   ymin[category_id],ymax[category_id],name_damage, namexml)





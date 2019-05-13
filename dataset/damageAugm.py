"""
damageAugmentation
just to balance our dataset after the tiling process



Written by Adonis Gonzalez
------------------------------------------------------------
"""
import os,sys
from keras.preprocessing.image import ImageDataGenerator,array_to_img, img_to_array, load_img
import math
import random
import numpy as np
from shutil import copyfile


ROOT_DIR = os.path.abspath("../")
sys.path.append(ROOT_DIR)

tiles = os.path.join(ROOT_DIR, "dataset/tiles")
data = os.path.join(ROOT_DIR, "dataset/data2")

print(tiles)

datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='constant')
class_size=100

subdirs = []
for dir in os.listdir(tiles):
    subdirs.append(dir)

dict = {}
for subdir in subdirs:
    subdir_fullpath = os.path.join(tiles, subdir)

    list_class = os.listdir(subdir_fullpath)
    for img in list_class:
        list_class = os.listdir(subdir_fullpath)
        count_class = len(os.listdir(subdir_fullpath))

        print(count_class)
        ratio = math.floor(class_size / count_class) - 1
        print("this is ratio", ratio)
        print(count_class,count_class*(ratio+1))

        img = load_img(os.path.join(subdir_fullpath, img))

        x = img_to_array(img)
        x = x.reshape((1,) + x.shape)
        i = 0

        if count_class <= 100:
            if not os.path.exists(data):
                os.makedirs(data)

            dest_dir = os.path.join(data, subdir)

            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)


            for batch in datagen.flow(x, batch_size=1, save_to_dir=dest_dir, save_format='jpg'):
                i += 1
                if i > ratio:
                    break


        else:
            dest_dir = os.path.join(data, subdir)
            if not os.path.exists(data):
                os.makedirs(data)


            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)


            files = os.listdir(subdir_fullpath)
            print(files)
            #index = random.randrange(0, len(files))
            index = np.random.choice(len(files), 100, replace=False)
            print(index)

            for x in index:
                print(files[x])
                file_to_copy = os.path.join(subdir_fullpath, files[x])
                print(file_to_copy)
                copyfile(file_to_copy, dest_dir+"/"+files[x])

            break





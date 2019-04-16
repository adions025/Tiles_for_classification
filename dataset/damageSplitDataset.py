"""
damageSplitDataset
-------------------


Written by Adonis Gonzalez
------------------------------------------------------------
"""
import sys
import os
import random
from shutil import copyfile

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(ROOT_DIR)
print(ROOT_DIR)
path = []

folder1 = os.path.join(ROOT_DIR, "tiles")

print(folder1)



data = os.path.join(ROOT_DIR, "data")
path0 = os.path.join(ROOT_DIR, "data/train")
path1 = os.path.join(ROOT_DIR, "data/val")


def img_train_test_split(img_source_dir, train_size):

    if not (isinstance(img_source_dir, str)):
        raise AttributeError('img_source_dir must be a string')

    if not os.path.exists(img_source_dir):
        raise OSError('img_source_dir does not exist')

    if not (isinstance(train_size, float)):
        raise AttributeError('train_size must be a float')

    # Set up empty folder structure if not exists
    if not os.path.exists(data):
        os.makedirs(data)
    else:
        if not os.path.exists(path0):
            os.makedirs(path0)
        if not os.path.exists(path1):
            os.makedirs(path1)

    subdirs = []
    for subdir in os.listdir(img_source_dir):
        subdirs.append(subdir)

    for subdir in subdirs:
        subdir_fullpath = os.path.join(img_source_dir, subdir)

        if len(os.listdir(subdir_fullpath)) == 0:
            print(subdir_fullpath + ' is empty')
            break

        train_subdir = os.path.join(path0, subdir)
        print("---------")
        print(train_subdir)
        print("---------")
        validation_subdir = os.path.join(path1, subdir)

        if not os.path.exists(train_subdir):
            os.makedirs(train_subdir)

        if not os.path.exists(validation_subdir):
            os.makedirs(validation_subdir)

        train_counter = 0
        validation_counter = 0

        for filename in os.listdir(subdir_fullpath):
            if filename.endswith(".jpg"):
                fileparts = filename.split('.')

                if random.uniform(0, 1) <= train_size:
                    copyfile(os.path.join(subdir_fullpath, filename),
                             os.path.join(train_subdir, str(train_counter) + '.' + fileparts[1]))
                    train_counter += 1
                else:
                    copyfile(os.path.join(subdir_fullpath, filename),
                             os.path.join(validation_subdir, str(validation_counter) + '.' + fileparts[1]))
                    validation_counter += 1

        print('Copied ' + str(train_counter) + ' images to data/train/' + subdir)
    print('Copied ' + str(validation_counter) + ' images to data/validation/' + subdir)

if __name__ == "__main__":

    img_train_test_split(folder1, 0.8)
#112 + 41 + 35


"""

mAP

Written by Adonis Gonzalez
------------------------------------------------------------

"""
import sys
import os

#PATHS
ROOT_DIR = os.path.abspath("../")
sys.path.append(ROOT_DIR)
tiles_folder = os.path.join(ROOT_DIR, "dataset/results")
print(tiles_folder)



def read_csv_file(path):
    imgs_list = open(path + '/results.csv', 'r').readlines()
    return imgs_list


def list_dirs(path):
    subdirs = []
    for subdir in os.listdir(path):
        subdirs.append(subdir)
        print(subdir)
    return subdirs



if __name__ == "__main__":

    subdirs = list_dirs(tiles_folder)

    for subdir in subdirs:
        subdir_fullpath = os.path.join(tiles_folder, subdir)
        print(subdir_fullpath)

        imgs_list = read_csv_file(subdir_fullpath)
        print(imgs_list)
        break



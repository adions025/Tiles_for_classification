"""

mAP

Written by Adonis Gonzalez
------------------------------------------------------------

"""
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

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
    return subdirs

def save_histogram_mAP(dict_precision):
    labels, total = [], []
    for key, item in dict_precision.items():
        labels.append(key)
        total.append(item)

    x = np.arange(len(labels))
    plt.bar(x, height=total)
    plt.xticks(x + .5, labels)
    # plt.show()
    plt.savefig(tiles_folder + '/' + 'mAP1.png')
    print("---saving----")


if __name__ == "__main__":

    subdirs = list_dirs(tiles_folder)
    mAP_calculate = 0.0
    dict_precision = {}

    for subdir in subdirs:
        subdir_fullpath = os.path.join(tiles_folder, subdir)
        imgs_list = read_csv_file(subdir_fullpath)

        tp = 0
        fp = 0

        for img in imgs_list:
            img_name = img.strip().split('/')[-1]
            only_prediction = (img_name.split(' - ')[1])
            only_label = (only_prediction.split(' : ')[0])
            #---------------------------------------------
            # Because of the name folder
            if subdir == 'B&C':
                if only_label == 'b c':
                    only_label = 'B&C'

            if subdir == 'Erosion':
                if only_label == 'erosion':
                    only_label = 'Erosion'

            if subdir == 'no_damage':
                if only_label == 'no damage':
                    only_label = 'no_damage'

            if subdir == 'SD':
                if only_label == 'sd':
                    only_label = 'SD'

            if subdir == 'Dirt':
                if only_label == 'dirt':
                    only_label = 'Dirt'
            # ---------------------------------------------

            #counting TP, FP
            if subdir == only_label:
                print("this one", only_label)
                tp = tp + 1
            else :
                print("this no: ", only_label)
                fp = fp + 1
            #print (only_label)

        print("---------------------------")
        print("TP, FP",tp, fp)
        precision = (float(tp) / float(tp +fp))
        float(precision)
        dict_precision.update({subdir:precision})
        print("---------------------------")

        mAP_calculate = mAP_calculate +  precision
        float(mAP_calculate)

    print("this is mAP_calculate: ", mAP_calculate)
    print(mAP_calculate)
    mAP = mAP_calculate / float(len(subdirs))
    float(mAP)
    print(mAP)
    print(dict_precision)

    save_histogram_mAP(dict_precision)






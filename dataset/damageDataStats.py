import sys
import os
import matplotlib.pyplot as plt
import numpy as np

ROOT_DIR = os.path.abspath("../")
sys.path.append(ROOT_DIR)

folder2 = os.path.join(ROOT_DIR, "dataset/tiles")

subdirs = []

for dir in os.listdir(folder2):
    subdirs.append(dir)

dict = {}
for subdir in subdirs:
    subdir_fullpath = os.path.join(folder2, subdir)
    count_class = len(os.listdir(subdir_fullpath))
    list_class = os.listdir(subdir_fullpath)

    dict.update({subdir:count_class})
    print("------------------------------------")
    print("this is ", subdir)
    print(list_class,count_class)
    print("------------------------------------")
print(dict)

labels, total = [], []
for key, item in dict.items():
    labels.append(key)
    total.append(item)


x = np.arange(5)
plt.bar(x, height= total)
plt.xticks(x+.5, labels)
plt.savefig(folder2)


''''
    with open(folder2 + '/ab.csv', 'a') as f:
        f.write('%s, %s\n' % (subdir, os.listdir(subdir_fullpath)))
        # '%d %d' % (1, 2)

f.close()
'''
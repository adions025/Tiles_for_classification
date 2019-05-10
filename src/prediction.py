"""

Predictions for tiles


Written by Adonis Gonzalez
------------------------------------------------------------

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys, os
import time
import csv

import numpy as np
import tensorflow as tf
import cv2
from PIL import Image, ImageFont, ImageDraw
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def load_graph(model_file):

  with tf.device('/gpu:0'):
    graph = tf.Graph()
    graph_def = tf.GraphDef()
    with open(model_file, "rb") as f:
      graph_def.ParseFromString(f.read())
    with graph.as_default():
      tf.import_graph_def(graph_def)

    return graph


def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
				input_mean=0, input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(file_reader, channels = 3,
                                       name='png_reader')
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                  name='gif_reader'))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
  else:
    image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                        name='jpeg_reader')
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0);
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result


def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label


def grabNamesImages(path):
  files = os.listdir(path)
  print(files)
  with open(path + "/" + 'image.txt', 'w') as f:
    for item in files:
      if (item.endswith('.jpg')):
        f.write("%s\n" % item)
  f.close()
  print("List of images, images.tx, was save in", path)


if __name__ == "__main__":

  ROOT_DIR = os.path.abspath("../")
  sys.path.append(ROOT_DIR)

  folder2 = os.path.join(ROOT_DIR, "dataset/tiles")
  results_dir = os.path.join(ROOT_DIR, "dataset/results3")
  model_file = os.path.join(ROOT_DIR, "src/tf_files2/retrained_graph.pb")

  label_file = "tf_files/retrained_labels.txt"
  input_height = 299
  input_width = 299
  input_mean = 128
  input_std = 128
  input_layer = "Mul"
  output_layer = "final_result"

  font = os.path.join(ROOT_DIR, "font/FiraMono-Medium.otf")
  print(font)
  font = ImageFont.truetype(font, 30)

  subdirs = []
  for subdir in os.listdir(folder2):
    subdirs.append(subdir)

  for subdir in subdirs:
    subdir_fullpath = os.path.join(folder2, subdir)
    print("here")
    print(subdir_fullpath)

    create_dir = os.path.join(results_dir, subdir)

    if not os.path.exists(create_dir):
      os.makedirs(create_dir)

    grabNamesImages(subdir_fullpath)
    imgs_list = open(subdir_fullpath + '/image.txt', 'r').readlines()

    with open(create_dir + "/" + "results.csv", 'a') as f:
      for image_name in imgs_list:

        img_name = image_name.strip().split('/')[-1]
        file_path = (subdir_fullpath+"/"+img_name)
        only_img = (img_name.split('.jpg')[0])

        img = Image.open(file_path)
        draw = ImageDraw.Draw(img)

        graph = load_graph(model_file)
        t = read_tensor_from_image_file(file_path,
                                    input_height=input_height,
                                    input_width=input_width,
                                    input_mean=input_mean,
                                    input_std=input_std
                                  )
        input_name = "import/" + input_layer
        output_name = "import/" + output_layer
        input_operation = graph.get_operation_by_name(input_name);
        output_operation = graph.get_operation_by_name(output_name);

        best_result = {}

        with tf.Session(graph=graph) as sess:
          start = time.time()
          results = sess.run(output_operation.outputs[0],
                            {input_operation.outputs[0]: t})
          end=time.time()
          results = np.squeeze(results)

          top_k = results.argsort()[-5:][::-1]
          labels = load_labels(label_file)

          print('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))
          template = "{} (score={:0.5f})"
          for i in top_k:
            #print(template.format(labels[i], results[i]))
            best_result.update({labels[i]:results[i]})

          best = max((best_result.values()))

          for x, j in best_result.items():
            if j == best:
              labeling = x
          last = str(labeling + " : " + str(best))
          draw.text((0, 0), last, fill=(0, 0, 0), font=font) #
          img.save(create_dir+"/"+img_name)
          results_in_file = str(only_img +' - '+ last)
        f.write(results_in_file+'\n')




    f.close()

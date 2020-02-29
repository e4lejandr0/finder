#!/usr/bin/env python

import os
import glob

import cv2
import numpy as np
import tensorflow as tf

def crop(image, new_width, new_height):
    image_height = len(image)
    image_width = len(image[0])
    offset_y = 0 # image_height/2 - new_height/2
    offset_x = 0 #image_width/2 - new_width/2

    print(f"({offset_x},{offset_y})")
    print(f"{new_height} + {new_width}")
    return image[offset_y:offset_y+new_height, offset_x:offset_x+new_width]

def import_dir(path):
    training_images = []
    for fpath in glob.glob(f"{path}/*"):
        if not os.path.isfile(fpath):
            continue
        print(f"importing {fpath}")
        image_data = cv2.imread(fpath)
        training_images.append(crop(image_data, 1080, 1080))

    return np.asarray(training_images)
    
def main():
    PROJECT_DIR = os.getenv('PROJECT_DIR')
    IMG_WIDTH = 1080
    IMG_HEIGHT = IMG_WIDTH

    training_labels = ['good', 'bad']
    #training_images = import_dir(f"{PROJECT_DIR}/data/images/good")
    image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    training_data = image_generator.flow_from_directory(
        directory = f"{PROJECT_DIR}/data/images",
        batch_size = 10,
        shuffle = True,
        target_size = (IMG_HEIGHT, IMG_WIDTH),
        classes = training_labels
    )
    #trainignp.append(training_images.append(import_dir(f"{PROJECT_DIR}/data/images/bad"))

    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(2)
    ])

    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )

    model.fit_generator(training_data, training_labels, epochs=10)
                        


if __name__ == '__main__':
    main()

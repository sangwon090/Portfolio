from tensorflow.keras.preprocessing.image import array_to_img, img_to_array, load_img
from tensorflow.keras.callbacks import ModelCheckpoint
from datetime import datetime

import tensorflow as tf
import pandas as pd
import numpy as np
import os
import imageio
import sklearn.model_selection
import sklearn.preprocessing

sounds = ['air_conditioner','car_horn','children_playing','dog_bark','drilling','engine_idling','gun_shot','jackhammer','siren','street_music']
images = []
labels = []

with open('./UrbanSound8K.csv', newline='') as csv_file:
    data = csv_file.readlines()

    for index, row in enumerate(data):
        if index == 0:
            continue
            
        row = row.split(',')
        t = row[7].replace('\n', '')
        temp = row[0].replace('wav', 'png')
        img = img_to_array(load_img(f'./out/fold{row[5]}/{temp}'))
        images.append(img.reshape((1,)+img.shape))
        labels.append(int(row[6]))

x = np.array(images)
y = np.array(labels)
z = tf.keras.utils.to_categorical(sklearn.preprocessing.LabelEncoder().fit_transform(y))

num_rows = 369
num_columns = 496
num_channels = 3

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, z, test_size=0.2, random_state=42)
x_train = x_train.reshape(x_train.shape[0], num_rows, num_columns, num_channels)
x_test = x_test.reshape(x_test.shape[0], num_rows, num_columns, num_channels)
num_labels = z.shape[1]
filter_size = 2

model = tf.keras.Sequential()
model.add(tf.keras.layers.Conv2D(filters=16,kernel_size=2, input_shape=(num_rows, num_columns, num_channels), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Conv2D(filters=32,kernel_size=2, activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Conv2D(filters=64,kernel_size=2, activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Conv2D(filters=128,kernel_size=2, activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.GlobalAveragePooling2D())
model.add(tf.keras.layers.Dense(num_labels, activation='softmax'))
model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
model.summary()

timer_start = datetime.now()
model.fit(x_train, y_train, batch_size=8, epochs=72, validation_data=(x_test, y_test), verbose=1)
print(f'학습이 완료됨: {datetime.now() - timer_start}')

score = model.evaluate(x_test, y_test, verbose=0)
print("학습 후 정확도: %.4f%%" % score[1] * 100)
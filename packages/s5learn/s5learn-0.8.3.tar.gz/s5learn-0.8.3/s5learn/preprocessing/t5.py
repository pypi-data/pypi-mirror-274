def t5():

    print("""
    
    ## Tensorflow Operations

import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, optimizers, datasets
from matplotlib import pyplot as plt
import numpy as np

## Dataset
(x_train_raw, y_train_raw), (x_test_raw, y_test_raw) = datasets.mnist.load_data()


# Convert the labels into one-hot codes.
num_classes = 10
y_train = keras.utils.to_categorical(y_train_raw, num_classes)
y_test = = keras.utils.to_categorical(y_test_raw, num_classes)


# Convert a 28 x 28 image to a 784 x 1 vector.
x_train = x_train_raw.reshape(60000, 784)
x_test = x_test_raw.reshape(10000, 784)


# Normalize image pixel values.
x_train = x_train.astype('float32')/255
x_test = x_test.astype('float32')/255


# Create a deep neural network (DNN) model that consists of three fully connected layers and two ReLU activation functions.
model = keras.Sequential([
layers.Dense(512, activation='relu', input_dim = 784),
layers.Dense(256, activation='relu'),
layers.Dense(124, activation='relu'),
layers.Dense(num_classes, activation='softmax')])
model.summary()


Optimizer = optimizers.Adam(0.001)
model.compile(loss=keras.losses.categorical_crossentropy, optimizer=Optimizer, metrics=['accuracy'])

# Fit the training data to the model by using the fit method.
model.fit(x_train, y_train, batch_size=128, epochs=10, verbose=1)

## Model Evaluation
score = model.evaluate(x_test, y_test, verbose=0)


## Saving Model
logdir='./mnist_model'
if not os.path.exists(logdir):
	os.mkdir(logdir)
model.save(logdir+'/final_DNN_model.h5')



#############################################################################
######################## CNN CONSTRUCTION ###################################
#############################################################################


model=keras.Sequential()
model.add(keras.layers.Conv2D(filters=32,kernel_size = 5,strides = (1,1), padding = 'same',activation = tf.nn.relu,input_shape = (28,28,1)))
model.add(keras.layers.MaxPool2D(pool_size=(2,2), strides = (2,2), padding = 'valid'))
model.add(keras.layers.Conv2D(filters=64,kernel_size = 3,strides = (1,1),padding = 'same',activation = tf.nn.relu))
model.add(keras.layers.MaxPool2D(pool_size=(2,2), strides = (2,2), padding = 'valid'))
model.add(keras.layers.Dropout(0.25))
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(units=128,activation = tf.nn.relu))
model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Dense(units=10,activation = tf.nn.softmax))

# Expand data dimensions to adapt to the CNN model.
X_train=x_train.reshape(60000,28,28,1)
X_test=x_test.reshape(10000,28,28,1)
model.compile(optimizer="adam",loss="categorical_crossentropy",metrics=['accuracy'])
model.fit(x=X_train,y=y_train,epochs=5,batch_size=128)

test_loss,test_acc=model.evaluate(x=X_test,y=y_test)
print("Test Accuracy %.2f"%test_acc)

## Saving Model
logdir='./mnist_model'
if not os.path.exists(logdir):
	os.mkdir(logdir)
model.save(logdir+'/final_CNN_model.h5')
    
    """)
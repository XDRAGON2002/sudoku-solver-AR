import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
import cv2
import numpy as np
import os

# data = keras.datasets.mnist

# (train_image,train_label),(test_image,test_label) = data.load_data()
# train_image = train_image.reshape(train_image.shape[0],28,28,1)
# test_image = test_image.reshape(test_image.shape[0],28,28,1)
# train_image = train_image / 255
# test_image = test_image / 255

def SHOW(img):

    cv2.imshow("img",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

images = []
labels = []
for dirs in os.listdir(".\\Digits") :
    for image in os.listdir(os.path.join(".\\Digits",dirs)) :
        img_path = os.path.join(".\\Digits",dirs,image)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        img = cv2.resize(img,(32,32))
        img = np.array(img)
        img = img.astype("float32")
        img /= 255
        images.append(img)
        labels.append(int(dirs))
        # break

images = np.array(images)
labels = np.array(labels)
images = images.reshape(-1,32,32,1)
# print(images.shape)
# print(labels.shape)

train_image,test_image,train_label,test_label = train_test_split(images,labels,test_size = 0.2)

# print(train_image.shape)
# print(train_label.shape)

cnn_model = keras.Sequential([
    keras.layers.Conv2D(32,(3,3),activation = "relu",input_shape = (32,32,1)),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Conv2D(64,(3,3),activation = "relu"),
    keras.layers.Conv2D(64,(3,3),activation = "relu"),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Flatten(),
    keras.layers.Dense(100,activation = "relu"),
    keras.layers.Dense(10,activation = "softmax")
])
cnn_model.compile(optimizer = "adam",loss = "sparse_categorical_crossentropy",metrics = ["accuracy"])
cnn_model.fit(train_image,train_label,epochs = 15)
cnn_loss,cnn_acc = cnn_model.evaluate(test_image,test_label)
# print(cnn_acc)

cnn_model.save("ocr_model.h5")
new_model = keras.models.load_model("ocr_model.h5")
loss, acc = new_model.evaluate(test_image,test_label)
# print(acc)
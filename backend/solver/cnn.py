import tensorflow as tf
from tensorflow import keras

data = keras.datasets.mnist

(train_image,train_label),(test_image,test_label) = data.load_data()
train_image = train_image.reshape(train_image.shape[0],28,28,1)
test_image = test_image.reshape(test_image.shape[0],28,28,1)
train_image = train_image / 255
test_image = test_image / 255


cnn_model = keras.Sequential([
    keras.layers.Conv2D(32,(3,3),activation = "relu",input_shape = (28,28,1)),
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

cnn_model.save("ocr_model.h5")
new_model = keras.models.load_model("ocr_model.h5")
loss, acc = new_model.evaluate(test_image,test_label)
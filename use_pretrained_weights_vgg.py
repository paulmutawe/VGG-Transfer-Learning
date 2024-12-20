from __future__ import print_function, division
from builtins import range, input

from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image

from tensorflow.keras.preprocessing.image import ImageDataGenerator

from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt

from glob import glob

IMAGE_SIZE = [100, 100]

epochs = 5
batch_size = 32

train_path = '/Users/paulmutawe/Downloads/archive (2)/fruits-360_dataset_original-size/fruits-360-small/Training'
valid_path = '/Users/paulmutawe/Downloads/archive (2)/fruits-360_dataset_original-size/fruits-360-small/Validation'

image_files = glob(train_path + '/*/*.jp*g')
valid_image_files = glob(valid_path + '/*/*.jp*g')

folders = glob(train_path + '/*')

plt.imshow(image.img_to_array(image.load_img(np.random.choice(image_files))).astype('uint8'))
plt.show()

vgg = VGG16(input_shape = IMAGE_SIZE + [3], weights = 'imagenet', include_top = False)

for layer in vgg.layers:
    layer.trainable = False

x = Flatten()(vgg.output)

prediction = Dense(len(folders), activation = 'softmax')(x)

model = Model(inputs = vgg.input, outputs = prediction)

model.summary()

model.compile(
    loss = 'categorical_crossentropy',
    optimizer = 'rmsprop',
    metrics = ['accuracy']
)

gen = ImageDataGenerator(
    rotation_range = 20,
    width_shift_range = 0.1,
    height_shift_range = 0.1,
    shear_range = 0.1,
    zoom_range = 0.2,
    horizontal_flip = True,
    vertical_flip = True,
    preprocessing_function = preprocess_input
)

test_gen = gen.flow_from_directory(valid_path, target_size = IMAGE_SIZE)
print(test_gen.class_indices)
labels = [None] * len(test_gen.class_indices)
for k, v in test_gen.class_indices.items():
    labels[v] = k

for x, y in test_gen:
    print("min:", x[0].min(), "max:", x[0].max())
    plt.title(labels[np.argmax(y[0])])
    plt.imshow(x[0])    
    plt.show()
    break

train_generator = gen.flow_from_directory(
    train_path,
    target_size = IMAGE_SIZE,
    shuffle = True,
    batch_size = batch_size,
)

valid_generator = gen.flow_from_directory(
    valid_path,
    target_size = IMAGE_SIZE,
    shuffle = True,
    batch_size = batch_size,
)

r = model.fit(
    train_generator,
    validation_data = valid_generator,
    epochs = epochs,
    steps_per_epoch = len(image_files) // batch_size,
    validation_steps = len(valid_image_files) // batch_size,
)

def get_confusion_matrix(data_path, N):
    print("Generating confusion matrix", N)
    predictions = []
    targets = []
    i = 0

    for x, y in gen.flow_from_directory(data_path, target_size=IMAGE_SIZE, shuffle=False, batch_size=batch_size * 2):
        i += 1
        if i % 50 == 0:
            print(f"Processed {i} batches")

        # Predict the class for each image batch
        p = model.predict(x)
        p = np.argmax(p, axis=1)

        # True labels (targets)
        y = np.argmax(y, axis=1)

        # Append to the lists
        predictions = np.concatenate((predictions, p))
        targets = np.concatenate((targets, y))

        if len(targets) >= N:
            break

    # Generate and return the confusion matrix
    cm = confusion_matrix(targets[:N], predictions[:N])
    return cm

cm = get_confusion_matrix(train_path, len(image_files))
print(cm)
valid_cm = get_confusion_matrix(valid_path, len(valid_image_files))
print(valid_cm)

plt.plot(r.history['loss'], label = 'train loss')
plt.plot(r.history['val_loss'], label = 'val loss')
plt.legend()
plt.show()

plt.plot(r.history['accuracy'], label = 'train acc')
plt.plot(r.history['val_accuracy'], label = 'val acc')
plt.legend()
plt.show()

from util import plot_confusion_matrix
plot_confusion_matrix(cm, labels, title = 'Train confusion matrix')
plot_confusion_matrix(valid_cm, labels, title = 'Validation confusion matrix')





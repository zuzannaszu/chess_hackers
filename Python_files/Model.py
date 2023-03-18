import tensorflow as tf
import cv2 as cv
import numpy as np


model_path = "/home/thierry/code/zuzannaszu/chess_hackers/Model/chessmodel.h5"

classes = {'blackempty': 0,
 'black_ki': 1,
 'black_p': 2,
 'whiteempty': 3,
 'white_ki': 4,
 'white_p': 5}

def select_image(imgs_path):
    cv_imgs = []
    for img in imgs_path:
        n= cv.imread(img)
        b,g,r = cv.split(n)
        rgb_img = cv.merge([r,g,b])
        cv_imgs.append(rgb_img)
    return cv_imgs

def generate_dict(model, cv_imgs, imgs_path):
    out_dict = {}
    for idx, img in enumerate(cv_imgs):
        img_array =cv.resize(img, dsize=(160, 120), interpolation=cv.INTER_CUBIC).astype(dtype='float64')
        img_array /= 255.0
        img_array = np.expand_dims(img_array, axis=0)
        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions)
        class_labels = list(classes.keys())
        predicted_class_label = class_labels[predicted_class_index]
        coor = imgs_path[idx][-6:-4]
        if predicted_class_label not in ['blackempty','whiteempty']:
            out_dict[coor] = predicted_class_label
    return out_dict

def prep_imgs(imgs):
    images = []
    for img in imgs:
        img = tf.image.resize(img, [120,160])
        img = np.copy(tf.keras.preprocessing.image.img_to_array(img))
        img = np.copy(np.expand_dims(img, axis=0))
        img /= 255.0
        img = np.expand_dims(img, axis=0)
        images.append(img)
    images = np.concatenate(images, axis=0)
    return images

def make_predict(model, images, imgs_path):
    out_dict = {}
    for i, img in enumerate(images):
        predictions = model.predict(img)
        predicted_class_index = np.argmax(predictions)
        class_labels = list(classes.keys())
        predicted_class_label = class_labels[predicted_class_index]
        coor = imgs_path[i][-6:-4]
        if predicted_class_label not in ['blackempty','whiteempty']:
            out_dict[coor] = predicted_class_label
    return out_dict

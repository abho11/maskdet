import os
import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine
import cv2
import mtcnn
from keras.models import load_model
sys.path.append('..')
from utils import get_face, l2_normalizer, normalize, save_pickle, plt_show, get_encode

def fun():
    encoder_model = r'facenet_keras copy.h5'
    people_dir = r'./main/static/people'
    encodings_path = r'encodings.pkl'



    required_size = (160, 160)
    encoding_dict = dict()

    face_detector = mtcnn.MTCNN()
    face_encoder = load_model(encoder_model)

    for person_name in os.listdir(people_dir):
        person_dir = os.path.join(people_dir, person_name)
        encodes = []
        for img_name in os.listdir(person_dir):
            img_path = os.path.join(person_dir, img_name)
            img = cv2.imread(img_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = face_detector.detect_faces(img_rgb)
            if results:
                res = max(results, key=lambda b: b['box'][2] * b['box'][3])
                face, _, _ = get_face(img_rgb, res['box'])
                
                face = normalize(face)
                face = cv2.resize(face, required_size)
                encode = face_encoder.predict(np.expand_dims(face, axis=0))[0]
                encodes.append(encode)
        if encodes:
            encode = np.sum(encodes, axis=0)
            encode = l2_normalizer.transform(np.expand_dims(encode, axis=0))[0]
            encoding_dict[person_name] = encode       

    save_pickle(encodings_path, encoding_dict)        
    
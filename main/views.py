from django.shortcuts import render
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials 
from bson.json_util import dumps
import cv2 
import os
from run import fun
from scipy.spatial.distance import cosine
import mtcnn
from keras.models import load_model
from utils import *
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from datetime import date,datetime

os.environ['OPENCV_IO_MAX_IMAGE_PIXELS']=str(2**64)

cred=credentials.Certificate("finalyearnmit-firebase-adminsdk-sk5ac-a5da39de07.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://finalyearnmit-default-rtdb.firebaseio.com/'})
ref=db.reference("defaulters")

def home(request):
 
 l=[]
 k=ref.order_by_key().get()
 
 for m,n in k.items():
  l.append(n)
 json_data = dumps(l, indent = 2)  

 with open('main/static/app.json', 'w') as file:
    file.write(json_data)     
 
 return render(request,'home.html')

'''
def capture(request):
 
 if request.method == "POST":
   cam = cv2.VideoCapture(0)
   if not cam.isOpened():
       print("Error opening Video File.")
   temp = request.POST.get("your_name")
   directory = './main/static/people/'+temp +'/'
   if not os.path.exists(directory):
    os.makedirs(directory) 
   name = directory +temp+ '.jpg' 
   try : 
    while True :
         
      ret,frame = cam.read()
      cv2.imshow('frame', frame)
      if ret:
         if cv2.waitKey(1) & 0xFF == ord('s'): 
               print ('Creating...' + name) 
               cv2.imwrite(name, frame)
               cam.release()
               cv2.destroyAllWindows()
               fun()
               return render(request,'home.html')

         elif cv2.waitKey(1) & 0xFF == ord('q'):   
                  cam.release()
                  cv2.destroyAllWindows()
                  fun()
                  return render(request,'home.html')
         
      else :
         return render(request,'home.html')
   except:
    print("Video has ended.") 
    return render(request,'home.html')     


def test(request): 
 if request.method == "POST":   
    
    names_dict = {}

    def detect_and_predict_mask(face_,face_detector, maskNet,pt_1, pt_2):
        faces = []
        locs = []
        face = cv2.resize(face_, (224, 224))
        face = img_to_array(face)
        face = preprocess_input(face)
        faces.append(face)
        location = pt_1+pt_2
        locs.append(location)
        if len(faces) > 0:
            faces = np.array(faces, dtype="float32" )
            preds = maskNet.predict(faces, batch_size=32)
        return (preds,locs)

    def recognize(img,
                detector,
                encoder,
                encoding_dict,
                mask_detector,
                recognition_t=0.4,
                confidence_t=0.99,
                required_size=(160, 160) ):

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = detector.detect_faces(img_rgb)
        for res in results:
            if res['confidence'] < confidence_t:
                continue
            face, pt_1, pt_2 = get_face(img_rgb, res['box'])
            encode = get_encode(encoder, face, required_size)
            encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
            name = 'unknown'

            distance = float("inf")
            for db_name, db_encode in encoding_dict.items():
                dist = cosine(db_encode, encode)
                if dist < recognition_t and dist < distance:
                    name = db_name
                    distance = dist
            if name == 'unknown':
                cv2.rectangle(img, pt_1, pt_2, (0, 0, 255), 2)
                cv2.putText(img, name, pt_2, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
            else:
                if(name not in names_dict.keys())  :
                    date1=date.today()
                    d1=date1.strftime("%d-%m-%Y")
                    t1=datetime.now().time()
                    t2 = t1.strftime("%H:%M")
                    data = {'Name': name,'Date': d1,'Time':t2}
                    ref.push(data)
    
                names_dict[name] = 1
                cv2.rectangle(img, pt_1, pt_2, (0, 255, 0), 2)
                cv2.putText(img, name + f'__{distance:.2f}', (pt_2[0]-130, pt_2[1]+30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 255, 0), 2)


            (preds,locs) = detect_and_predict_mask(face,face_detector,mask_detector,pt_1, pt_2)
            for  pred,loc in  zip(preds,locs):
                (mask, withoutMask) = pred
                (startX, startY, endX, endY) = loc
                #print(mask, withoutMask)
                if mask > withoutMask:
                    label = "Thank You. Mask On."
                    color = (0, 255, 0)
                else:
                    label = "No Face Mask Detected"
                    color = (0, 0, 255)

                cv2.putText(frame, label, (startX-50, startY - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            i = 0
            for n in names_dict.keys():
                cv2.putText(frame, n, (10, i+30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
                i = i+ 20

        return img

    
    try :
        encoder_model =  r'facenet_keras copy.h5'
        encodings_path = r'encodings.pkl'
        mask_detection_model = r'mask_detector.model'
        
        face_detector = mtcnn.MTCNN()

        mask_detector = load_model(mask_detection_model)
        face_encoder = load_model(encoder_model)
        encoding_dict = load_pickle(encodings_path)

        vc = cv2.VideoCapture(0)
        while vc.isOpened():
            ret, frame = vc.read()
            if not ret:
                print("no frame:(")
                break
            frame = recognize(frame, face_detector, face_encoder, encoding_dict,mask_detector)

            cv2.imshow('camera', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                vc.release()
                cv2.destroyAllWindows()
                break
        return render(request,'home.html')        
    except :
        return render(request,'home.html')    
'''
def clearTable(request):
    d = open('./main/static/app.json', "w+")
    d.truncate()
    d.close()
    return render(request,'home.html') 


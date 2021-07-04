from datetime import date
from django.shortcuts import render
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials 
from bson.json_util import dumps
from firebase_admin import auth
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import threading
import cv2
from time import sleep
import logging as log


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

def capture(request):
   
   
   log.basicConfig(filename='webcam.log',level=log.INFO)

   video_capture = cv2.VideoCapture(0)
   

   while True:
      if not video_capture.isOpened():
         print('Unable to load camera.')
         sleep(5)
         pass

      # Capture frame-by-frame
      ret, frame = video_capture.read()

      # Display the resulting frame
      cv2.imshow('Video', frame)

      if cv2.waitKey(1) & 0xFF == ord('s'): 

         check, frame = video_capture.read()
         cv2.imshow("Capturing", frame)
         cv2.imwrite(filename='saved_img.jpg', img=frame)
         video_capture.release()
      
         cv2.destroyAllWindows()

         return render(request,'home.html')
      elif cv2.waitKey(1) & 0xFF == ord('q'):
         print("Turning off camera.")
         video_capture.release()
         print("Camera off.")
         print("Program ended.")
         cv2.destroyAllWindows()
         return render(request,'home.html')

      # Display the resulting frame
      cv2.imshow('Video', frame)

   # When everything is done, release the capture
   video_capture.release()
   cv2.destroyAllWindows()
'''   
   key = cv2. waitKey(1)
   webcam = cv2.VideoCapture(0)
   sleep(2)
   while True:
      try:
         check, frame = webcam.read()
         print(check) #prints true as long as the webcam is running
         print(frame) #prints matrix values of each framecd 
         cv2.imshow("/main/static/Capturing", frame)
         key = cv2.waitKey(1)
         if key == ord('s'): 
               cv2.imwrite(filename="/main/static/saved_img.jpg", img=frame)
               webcam.release()
               cv2.destroyAllWindows()
               return render(request,'home.html')
                 
         elif key == ord('q'):
               webcam.release()
               cv2.destroyAllWindows()
               return render(request,'home.html')
               
      
      except(KeyboardInterrupt):
         print("Turning off camera.")
         webcam.release()
         cv2.destroyAllWindows()
         return render(request,'home.html')
          
'''
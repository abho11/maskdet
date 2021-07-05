from django.shortcuts import render
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials 
from bson.json_util import dumps
import cv2
import os


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
 if request.method == "POST":
   cam = cv2.VideoCapture(0)
   temp = request.POST.get("your_name")
   directory = './main/static/people/'+temp +'/'
   if not os.path.exists(directory):
    os.makedirs(directory) 
   while(True):
         
      ret,frame = cam.read()
      cv2.imshow('frame', frame)
      if ret:
         if cv2.waitKey(1) & 0xFF == ord('s'): 
               name = directory +temp+ '.jpg'
               print ('Creating...' + name) 
               cv2.imwrite(name, frame)
               cam.release()
               cv2.destroyAllWindows()
               return render(request,'home.html')

         elif cv2.waitKey(1) & 0xFF == ord('q'):   
                  cam.release()
                  cv2.destroyAllWindows()
                  return render(request,'home.html')
    
      else :
       return render(request,'home.html')

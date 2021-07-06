from django.shortcuts import render
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials 
from bson.json_util import dumps
import cv2 as cv
import os
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


def capture(request):
 if request.method == "POST":
   cam = cv.VideoCapture(0)
   if not cam.isOpened():
       print("Error opening Video File.")
   temp = request.POST.get("your_name")
   directory = './main/static/people/'+temp +'/'
   if not os.path.exists(directory):
    os.makedirs(directory) 
   name = directory +temp+ '.jpg' 
   #try : 
   while True :
         
      ret,frame = cam.read()
      cv.imshow('frame', frame)
      if ret:
         if cv.waitKey(1) & 0xFF == ord('s'): 
               print ('Creating...' + name) 
               cv.imwrite(name, frame)
               cam.release()
               cv.destroyAllWindows()
               return render(request,'home.html')

         elif cv.waitKey(1) & 0xFF == ord('q'):   
                  cam.release()
                  cv.destroyAllWindows()
                  return render(request,'home.html')
   
      else :
         return render(request,'home.html')
   #except:
   # print("Video has ended.") 
    #return render(request,'home.html')     

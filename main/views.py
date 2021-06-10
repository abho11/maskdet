from datetime import date
from django.shortcuts import render
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials 
from bson.json_util import dumps
from firebase_admin import auth



cred=credentials.Certificate("finalyearnmit-firebase-adminsdk-sk5ac-a5da39de07.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://finalyearnmit-default-rtdb.firebaseio.com/'})
ref=db.reference("defaulters")


def home(request):
 '''
 l=[]
 k=ref.order_by_key().get()
 
 for m,n in k.items():
  l.append(n)
 json_data = dumps(l, indent = 2)  
 print(json_data)    
 with open('main/static/app.json', 'w') as file:
    file.write(json_data)     
'''
 return render(request,'home.html')



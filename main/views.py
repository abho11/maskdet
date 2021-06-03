from datetime import date
from django.shortcuts import render
import pyrebase
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials 
from bson.json_util import dumps
import json
from json2html import *

from prettytable import PrettyTable
cred=credentials.Certificate("finalyearnmit-firebase-adminsdk-sk5ac-a5da39de07.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://finalyearnmit-default-rtdb.firebaseio.com/'})
ref=db.reference("defaulters")

config = {
    "apiKey": "AIzaSyD52GoFN5cJANgqPGQoQJSXBGzGx2-rSP4",
    "authDomain": "finalyearnmit.firebaseapp.com",
    "databaseURL": "https://finalyearnmit-default-rtdb.firebaseio.com",
    "projectId": "finalyearnmit",
    "storageBucket": "finalyearnmit.appspot.com",
    "messagingSenderId": "98178635428",
    "appId": "1:98178635428:web:e63109ee6627cd3437b831",
    "measurementId": "G-QL8C77J6NK"
}

firebase = pyrebase.initialize_app(config)
database=firebase.database()


def home(request):
  
    
    
 l=[]
 k=ref.order_by_key().get()
 
 for m,n in k.items():
    print( n)
    l.append(n)
    print(l)
 json_data = dumps(l, indent = 2)  
 print(json_data)    
 with open('main/static/app.json', 'w') as file:
    file.write(json_data)     
 x=json2html.convert(json = json_data)
 return render(request,'home.html')



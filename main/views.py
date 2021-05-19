from datetime import date
from django.shortcuts import render
import pyrebase



config = {
    "apiKey": "AIzaSyDApLG9x8dCakpoyvzNDZc0kCx2lui1wgg",
    "authDomain": "test-3f380.firebaseapp.com",
    "databaseURL": "https://test-3f380-default-rtdb.firebaseio.com",
    "projectId": "test-3f380",
    "storageBucket": "test-3f380.appspot.com",
    "messagingSenderId": "1094542591459",
    "appId": "1:1094542591459:web:9be05b403f91caa2428cd6",
    "measurementId": "G-BVXMLJGGYH"
}

firebase = pyrebase.initialize_app(config)
database=firebase.database()


def home(request):
    n = database.child('name').get().val()
    d = database.child('date').get().val()
    t=  database.child('time').get().val()
    return render(request,"home.html",{"n":n,"d":d, "t":t })

    
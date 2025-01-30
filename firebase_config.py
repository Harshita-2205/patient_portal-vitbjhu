import pyrebase

firebase_config = {
    "apiKey": "AIzaSyApztxAGaSX7dTNcdd72lljKDJYsYHUtrg",
    "authDomain": "patientportal-bb819.firebaseapp.com",
    "databaseURL": "https://YOUR_PROJECT_ID.firebaseio.com",
    "projectId": "patientportal-bb819",
    "storageBucket": "patientportal-bb819.appspot.com",
    "messagingSenderId": "YOUR_SENDER_ID",
    "appId": "YOUR_APP_ID"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
storage = firebase.storage()

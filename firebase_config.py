import pyrebase

# Firebase Configuration
firebase_Config = {
  "apiKey": "AIzaSyApztxAGaSX7dTNcdd72lljKDJYsYHUtrg",
  "authDomain": "patientportal-bb819.firebaseapp.com",
    "databaseURL":"https://console.firebase.google.com/u/0/project/patientportal-bb819/firestore/databases/patientdocs/data/~2FDocuments",
  "projectId": "patientportal-bb819",
  "storageBucket": "patientportal-bb819.firebasestorage.app",
  "messagingSenderId": "288006779718",
  "appId":"1:288006779718:web:3273f88529bc5b97deeb47",
  "measurementId":"G-R9WTQWDVTL"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_Config)

# Firebase Authentication
auth = firebase.auth()

# Firebase Database
db = firebase.database()

# Firebase Storage
storage = firebase.storage()

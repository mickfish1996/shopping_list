import firebase_admin
from firebase_admin import credentials

class Get_key():
     
    def __init__(self):
        self.cred = credentials.Certificate("shoping-list-cf7ed-firebase-adminsdk-e2bto-1dfe5984cc.json")
        
    def return_key(self):
        return self.cred
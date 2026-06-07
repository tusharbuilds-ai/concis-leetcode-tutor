import firebase_admin
import os
from dotenv import load_dotenv
from core.LogManager import log
from firebase_admin import credentials, db 
from core.LogManager import log

load_dotenv()


class FirebaseService:
    def __init__(self):
        try:
            cred = credentials.Certificate(
                {
                    "type":"service_account",
                    "project_id":os.getenv("FIREBASE_PROJECT_ID"),
                    "client_email":os.getenv("FIREBASE_CLIENT_EMAIL"),
                    "private_key":os.getenv("FIREBASE_PRIVATE_KEY").replace("\n\n","\n"),
                    "token_uri":"https://oauth2.googleapis.com/token"
                }
            )

            firebase_admin.initialize_app(cred,{
                "databaseURL":os.getenv("FIREBASE_URL")
            })

            self.users_ref = db.reference("/users")

            log.info("Connected to database")


        except Exception as FirebaseException:
            log.exception(f"Can't connect to the database currently! | {FirebaseException}")




firebase_conn = FirebaseService()

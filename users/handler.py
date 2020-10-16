from firebase_admin import firestore
from users.models import UserFS
from firebase_admin import auth

class UserHandler:
    def __init__(self):
        db = firestore.client()
        self.collection = db.collection("users")

    def get_fs_user(self, uid):
        doc = self.collection.document(uid).get()
        return UserFS.from_dict(doc.to_dict())

    @staticmethod
    def disable_user(uid):
        auth.update_user(uid, disabled=True)

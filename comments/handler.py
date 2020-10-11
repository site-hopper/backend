import uuid

from firebase_admin import firestore
from google.cloud.firestore_v1 import DocumentReference, DocumentSnapshot

import model
from .models import CommentFS
from typing import Dict


class CommentHandler:
    def __init__(self, domain, route):
        self._db = firestore.client()
        self._collection = self._db.collection("domains").document(domain).collection("routes").document(route). \
            collection("comments")

    def get_all_comment(self, limit_comment=None, limit_reply=None, level_reply=1):
        comments_collection = self._collection.stream()
        list_comment = []
        for comment_doc in comments_collection:
            comment = self._load_comment(comment_doc, self._collection, level=level_reply)
            list_comment.append(comment)
        return list_comment

    def _load_comment(self, comment: DocumentSnapshot, comments_collection, level):
        comment_dict = comment.to_dict()
        comment_dict["id"] = comment.id
        reply_collection = comments_collection.document(comment.id).collection("comments")
        if len(reply_collection.get()) > 0:
            self._load_collection(reply_collection, comment_dict, level=level)
        print(comment_dict)
        return CommentFS.from_dict(comment_dict)

    def _load_collection(self, reply_collection, comment_dict, level=0, max_level=1):
        list_reply = []
        for reply in reply_collection.get():
            reply_dict = reply.to_dict()
            reply_dict["id"] = reply.id
            sub_reply_collection = reply_collection.document(reply.id).collection("comments")
            if level < max_level and len(sub_reply_collection.get()) > 0:
                self._load_collection(sub_reply_collection, reply_dict, level=level)
            list_reply.append(reply_dict)
        comment_dict["list_reply"] = list_reply

    def add_comment(self, icomment):
        # TODO: add reference to user
        print(dict(icomment))
        ocomment = CommentFS(body=icomment.body, rating=icomment.rating, commenter=dict(icomment.commenter))
        try:
            comment_id = uuid.uuid4().hex
            print(ocomment.to_dict())
            self._collection.document(comment_id).set(ocomment.to_dict())
            return comment_id
        # TODO: handle particular exceptions
        except:
            raise Exception(f"Error adding comment")

    def update_comment(self, icomment):
        try:
            update_comment = dict(icomment)
            update_comment.pop("domain")
            update_comment.pop("route")

            comment_ref = self._collection.document(icomment.id)
            comment_ref.update(update_comment)
            return icomment.id
        except:
            raise Exception(f"Error updating comment")

    def add_reply(self, ireply):
        collection = self._collection
        ireply_dict = dict(ireply)
        ireply_dict["list_parent"] = []
        for parent_id in ireply.list_parent:
            ireply_dict["list_parent"].append(parent_id.hex)
            collection = collection.document(parent_id.hex).collection("comments")
        reply_id = uuid.uuid4().hex
        ireply_dict["commenter"] = dict(ireply_dict["commenter"])
        print(ireply_dict)
        collection.document(reply_id).set(ireply_dict)

    @staticmethod
    def get_comment_ref_path(domain, route, comment_uuid):
        return f"domains/{domain}/routes/{route}/comments/{comment_uuid}/"

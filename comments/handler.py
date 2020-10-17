import uuid

from firebase_admin import firestore
from google.cloud.firestore_v1 import DocumentSnapshot, ArrayUnion
from comments.schema.votes import Vote, RemoveVote
from users.models import User
from .models import CommentFS
import fireo

from .orm_models.models import Comment, Commenter
from users.orm_models.models import User as FSUser


class CommentHandler:
    def __init__(self, domain, route):
        self._db = firestore.client()
        # TODO: try to do it once
        fireo.connection(client=self._db)
        self._collection_name = Comment.collection_name
        self._collection = self._db.collection("domains").document(domain).collection("routes").document(route). \
            collection("comments")
        self.base_key = f"domains/{domain}/routes/{route}"

    def get_all_comment(self, limit=None):
        list_comment = []
        comment_collection = Comment.collection.parent(self.base_key).fetch(limit=limit)
        for comment in comment_collection:
            list_reply = []
            self._load_reply(f"{self.base_key}/comments/{comment.id}", list_reply,level=0, max_level=1)
            comment.list_reply = list_reply
            list_comment.append(comment.to_dict())
        return list_comment

    def _load_reply(self, key, list_reply, level, max_level):
        _list_reply = Comment.collection.parent(key).fetch()
        level+=1
        for reply in _list_reply:
            list_reply.append(reply.to_dict())
            if level<max_level:
                self._load_reply(f"{key}/comments/{reply.id}", list_reply, level=level, max_level=max_level)

    def add_comment(self, icomment, user_id):
        # TODO: add reference to user
        user = FSUser.collection.get(f"{FSUser.collection_name}/{user_id}")

        ocomment = Comment.from_dict(dict(icomment))
        ocomment.commenter = Commenter(first_name=user.first_name,last_name=user.last_name,id=user.id)

        comment_id = str(uuid.uuid4())
        ocomment.id = comment_id
        ocomment.parent = self.base_key
        ocomment.save()

        # Add comment id to user
        user.list_comment = ArrayUnion([ocomment.key])
        user.update()

        return comment_id
        # TODO: handle particular exceptions

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

    def delete_comment(self, list_id):
        key = self.base_key
        for id in list_id:
            key += f"/{self._collection_name}/{id}"
        Comment.collection.delete(key)
        return key

    def add_reply(self, ireply, user_id):
        user = FSUser.collection.get(f"{FSUser.collection_name}/{user_id}")
        ocomment = Comment.from_dict(dict(ireply))
        ocomment.commenter = Commenter(first_name=user.first_name,last_name=user.last_name,id=user.id)
        ocomment.list_parent = []
        key = self.base_key
        for parent_id in ireply.list_parent:
            ocomment.list_parent.append(parent_id)
            key += f"/comments/{parent_id}"

        reply_id = str(uuid.uuid4())
        ocomment.id = reply_id
        ocomment.parent = key
        ocomment.save()

        # Add reply key to user
        user.list_comment = ArrayUnion([ocomment.key])
        user.update()

        return reply_id

    def add_vote(self, vote: Vote, user: User):
        collection = self._collection
        comment_doc = None
        for parent_id in vote.list_parent:
            comment_doc = collection.document(parent_id.hex)
            collection = comment_doc.collection("comments")
        vote_map = {"up": vote.up}
        comment_doc.update({
            'votes.'+user.uid: vote_map
        })

    def remove_vote(self, remove_vote: RemoveVote, user: User):
        collection = self._collection
        comment_doc = None
        for parent_id in remove_vote.list_parent:
            comment_doc = collection.document(parent_id.hex)
            collection = comment_doc.collection("comments")
        deleteVote = {'votes.'+user.uid: firestore.firestore.DELETE_FIELD}
        comment_doc.update(deleteVote)

    @staticmethod
    def get_comment_ref_path(domain, route, comment_uuid):
        return f"domains/{domain}/routes/{route}/comments/{comment_uuid}/"

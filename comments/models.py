from datetime import datetime


class CommentFS:
    def __init__(self, body=None, commenter= None, rating=None, list_reply=None, parent=None):
        self.body = body
        self.commenter = commenter
        self.rating = rating
        self.list_reply = list_reply
        self.parent = parent
        self.created_on = datetime.now()

    @staticmethod
    def from_dict(source):
        comment = CommentFS()
        if source.get("parent",None):
            source.pop("parent")
        comment.__dict__.update(source)
        return comment

    def to_dict(self):
        return vars(self)

    def __repr__(self):
        return f"body:{self.body} by {self.commenter} on {self.created_on}"




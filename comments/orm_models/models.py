from fireo.models import Model
from fireo.fields import TextField, NumberField, NestedModel, ListField

from users.orm_models.models import User


class Commenter(Model):
    first_name = TextField()
    last_name = TextField()
    profile_pic = TextField()

    class Meta:
        collection_name = "users"


class Comment(Model):
    body = TextField(required=True)
    commenter = NestedModel(Commenter)
    list_parent = ListField
    list_comments = ListField

    class Meta:
        collection_name = "comments"

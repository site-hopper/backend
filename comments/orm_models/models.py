from fireo.models import Model
from fireo.fields import TextField, NumberField, NestedModel, ListField

from users.orm_models.models import User


class Comment(Model):
    body = TextField(required=True)
    commenter = NestedModel(User)
    list_parent = ListField
    list_comments = ListField
    class Meta:
        collection_name = "comments"

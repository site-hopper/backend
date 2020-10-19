from fireo.models import Model
from fireo.fields import TextField, NumberField, NestedModel, ListField, boolean_field, map_field

from users.orm_models.models import User


class Comment(Model):
    body = TextField(required=True)
    commenter = NestedModel(User)
    list_parent = ListField
    list_comments = ListField
    votes = map_field

    class Meta:
        collection_name = "comments"

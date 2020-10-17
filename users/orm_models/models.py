from fireo.models import Model
from fireo.fields import TextField, ListField


class User(Model):
    first_name = TextField()
    last_name = TextField()
    profile_pic = TextField()
    list_comment = ListField()

    class Meta:
        collection_name = "users"


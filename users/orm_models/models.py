from fireo.models import Model
from fireo.fields import TextField


class User(Model):
    first_name = TextField()
    last_name = TextField()
    profile_pic = TextField()

    class Meta:
        collection_name = "users"

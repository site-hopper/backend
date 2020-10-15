class User:
    def __init__(self, uid):
        self.uid = uid
    uid: str


class UserFS:
    def __init__(self, first_name="", last_name="", id=""):
        self.first_name = first_name
        self.last_name = last_name
        self.id = id

    @staticmethod
    def from_dict(source):
        user = UserFS()
        user.__dict__.update(source)
        return user

    def to_dict(self):
        return vars(self)
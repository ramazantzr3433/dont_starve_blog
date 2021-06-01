from hashlib import sha256

from bson import ObjectId
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin


class User(UserMixin):
    user_id: None
    user: None
    db: None

    def __init__(self):
        self.db = current_app.db

    @staticmethod
    def get_user(_user):
        """

        :param _user:
        :return:
        """
        db = current_app.db
        user = db.admin.find_one({'_id': ObjectId(_user)})
        if user is not None:
            u = User()
            u.user = user
            u.user_id = str(user.get('_id'))
            return u
        else:
            return AnonUser()

    def get_id(self):
        return self.user_id

    def login_user(self, username, password):
        """

        :param username: string
        :param password: hashed string
        :return: User
        """
        db_user = self.db.admin.find_one(
            {'username': username, 'password': sha256(password.encode('utf-8')).hexdigest()})
        print(db_user)
        if db_user is not None:
            u = User.get_user(str(db_user.get('_id')))
        else:
            u = AnonUser()
        return u

    def get_contacts(self):
        return self.db.contact.find()

    def get_gallerys(self):
        return self.db.gallery.find()

    def read_contact(self, _id):
        self.db.contact.update({'_id': ObjectId(_id)}, {
            '$set': {
                'is_active': False
            }
        })

    def image_activity(self, _id):
        image = self.db.gallery.find_one({'_id': ObjectId(_id)})
        self.db.gallery.update({'_id': ObjectId(_id)}, {
            '$set': {
                'is_active': not image.get('is_active')
            }
        })


class AnonUser(AnonymousUserMixin):
    def __init__(self):
        pass

    @staticmethod
    def __dict__():
        print('User not find')
        return {
            '_id': None,
            'username': "Anon",
            'is_active': False
        }

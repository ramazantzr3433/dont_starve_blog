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
            Bu fonksiyon veritabanından admin kullanıcısını çeker.
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
        """
            Bu fonksiyon giriş yapan kullanıcının id'sini geri verir.
        :return:
        """
        return self.user_id

    def login_user(self, username, password):
        """
            Bu fonksiyon admin sayfasına giriş yapmanızı sağlar.
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
        """
            Bu fonksiyon sayfa üzerinden gönderilen mesajları gösterir.
        :return:
        """
        return self.db.contact.find()

    def get_gallerys(self):
        """
            Bu fonksiyon sayfa üzerindeki gallery sayfasındaki resimleri gösterip göstermeyeceğinizi ayarlar.
        :return:
        """
        return self.db.gallery.find()

    def get_blogs(self):
        """
            Bu fonksiyon sayfadaki blog yazılarını çeker.
        :return:
        """
        return self.db.blog.find()

    def get_blog(self, _id):
        """
            Bu fonksiyon sayfadaki blog yazısını düzenlemenizi sağlar.
        :param _id:
        :return:
        """
        return self.db.blog.find_one({'_id': ObjectId(_id)})

    def remove_blog(self, _id):
        """
            Bu fonksiyon sayfadaki blog yazısını silmenizi sağlar.
        :param _id:
        :return:
        """
        self.db.blog.remove({'_id': ObjectId(_id)})

    def update_blog(self, _id, posted_blog):
        """
            Bu fonksiyon sayfadaki blog yazısını düzenlemenizi sağlar.
        :param _id:
        :param posted_blog:
        :return:
        """
        return self.db.blog.update({'_id': ObjectId(_id)}, {'$set': posted_blog})

    def new_blog(self, posted_blog):
        """
            Bu fonksiyon sayfaya yeni blog yazısı ekler.
        :param posted_blog:
        :return:
        """
        self.db.blog.insert(posted_blog)

    def read_contact(self, _id):
        """
            Bu fonksiyon sayfadan gelen iletişim yazısının okundu bilgisini günceller.
        :param _id:
        :return:
        """
        self.db.contact.update({'_id': ObjectId(_id)}, {
            '$set': {
                'is_active': False
            }
        })

    def image_activity(self, _id):
        """
            Bu fonksiyon gallery sayfasındaki resimlerin görününrlüğünü ayarlar.
        :param _id:
        :return:
        """
        image = self.db.gallery.find_one({'_id': ObjectId(_id)})
        self.db.gallery.update({'_id': ObjectId(_id)}, {
            '$set': {
                'is_active': not image.get('is_active')
            }
        })

    def blog_activity(self, _id):
        """
            Bu fonksiyon blog sayfasındaki yazıların görününrlüğünü ayarlar.
        :param _id:
        :return:
        """
        blog = self.db.blog.find_one({'_id': ObjectId(_id)})
        self.db.blog.update({'_id': ObjectId(_id)}, {
            '$set': {
                'is_active': not blog.get('is_active')
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

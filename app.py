import os
from datetime import datetime

from bson import ObjectId
from flask import Flask, render_template, current_app, request, redirect, url_for
from flask_login import LoginManager
from pymongo import MongoClient

from admin import admin
from lib.User import User

app = Flask(__name__)

client = MongoClient()
app.db = client.blog
app.secret_key = 'th1s1s5ec4etk3y'

UPLOAD_FOLDER = os.getcwd() + '/static/images/'
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

print('UPLOAD FOLDER ', UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.register_blueprint(admin, url_prefix="/admin")

login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def page_not_found(e):
    """
        Sayfa içerisinde olmayan bir url gidildiğinde gösterilecek sayfayı açar.
    :param e:
    :return:
    """
    print('404 error => ', e)
    return render_template('admin/404.html'), 404


@login_manager.user_loader
def load_user(user_id):
    """
        Flask-Login içi gerekli kullanıcı çekme yeri.
    :param user_id:
    :return:
    """
    return User.get_user(user_id)


@app.route('/')
def welcome():
    """
        Anasayfayı gösterir.
    :return:
    """
    images = current_app.db.gallery.find({'is_active': True})
    return render_template('index.html', images=images)


@app.route('/gallery/')
def gallery():
    """
        Galeri sayfasını gösterir.
    :return:
    """
    images = current_app.db.gallery.find({'is_active': True})
    return render_template('gallery.html', images=images)


@app.route('/archive/')
def archive():
    """
        Blog yazılarını gösterir.
    :return:
    """
    blogs = current_app.db.blog.find({'is_active': True})
    return render_template('archive.html', blogs=blogs)


@app.route('/archive/<_id>/')
def single_archive(_id):
    """
        Seçili blog yazısının detayını gösterir.
    :return:
    """
    blog = current_app.db.blog.find_one({'_id': ObjectId(_id)})
    return render_template('single.html', blog=blog)


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    """
        Sayfaya mesaj gönderir.
    :return:
    """
    if request.method == 'POST':
        posted_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'subject': request.form.get('subject'),
            'message': request.form.get('message'),
            '_created_at': datetime.now(),
            'is_active': True
        }
        current_app.db.contact.insert(posted_data)
        return redirect(url_for('contact'))
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)

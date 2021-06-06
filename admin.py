import os
from datetime import datetime

from bson import ObjectId
from flask import Flask, render_template, current_app, request, redirect, url_for, Blueprint, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename

import app
from lib.User import User

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        user = {
            'username': request.form.get('username'),
            'password': request.form.get('password')
        }
        u = User()
        login_status = u.login_user(user.get('username'), user.get('password'))
        if login_status.is_authenticated:
            login_user(login_status)
            return redirect(url_for('admin.contact'))
        else:
            return redirect(url_for('welcome'))

    return render_template('admin/login.html')


@admin.route('/contact/', methods=['GET'])
@login_required
def contact():
    contacts = current_user.get_contacts()
    return render_template('admin/contact.html', contacts=contacts)


@admin.route('/contact_read/<_id>/', methods=['GET'])
@login_required
def contact_read(_id):
    current_user.read_contact(_id)
    return redirect(url_for('admin.contact'))


@admin.route('/gallery/', methods=['GET'])
@login_required
def gallery():
    images = list(current_user.get_gallerys())
    return render_template('admin/gallery.html', images=images)


@admin.route('/image_activity/<_id>/', methods=['GET'])
@login_required
def image_activity(_id):
    current_user.image_activity(_id)
    return redirect(url_for('admin.gallery'))


@admin.route('/blog_activity/<_id>/', methods=['GET'])
@login_required
def blog_activity(_id):
    current_user.blog_activity(_id)
    return redirect(url_for('admin.blogs'))


@admin.route('/blog_remove/<_id>/', methods=['GET'])
@login_required
def blog_remove(_id):
    current_user.remove_blog(_id)
    return redirect(url_for('admin.blogs'))


@admin.route('/blogs/', methods=['GET'])
@login_required
def blogs():
    blogs = list(current_user.get_blogs())
    return render_template('admin/blog.html', blogs=blogs)


@admin.route('/blog/<_id>/', methods=['GET', 'POST'])
@login_required
def blog(_id):
    try:
        blog = current_user.get_blog(_id)
    except Exception as e:
        blog = None
        print('new blog')
    if request.method == 'POST':
        posted_blog = {
            'header': request.form.get('header'),
            'message': request.form.get('message'),
        }
        f = request.files['image']
        if f is not None:
            file_name = secure_filename(f.filename)
            f.save(os.path.join(app.UPLOAD_FOLDER, file_name))
            posted_blog['image'] = file_name
        if blog is not None:
            current_user.update_blog(_id, posted_blog)
        else:
            posted_blog['_created_at'] = datetime.now()
            posted_blog['is_active'] = True
            print('posted_blog')
            print(posted_blog)
            current_user.new_blog(posted_blog)
        return redirect(url_for('admin.blogs'))
    return render_template('admin/single-blog.html', blog=blog)


@admin.route("/logout/")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("admin.welcome"))

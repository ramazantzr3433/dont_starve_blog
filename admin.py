from bson import ObjectId
from flask import Flask, render_template, current_app, request, redirect, url_for, Blueprint, session
from flask_login import login_user, login_required, logout_user, current_user

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


@admin.route("/logout/")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("admin.welcome"))

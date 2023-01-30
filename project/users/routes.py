from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from .forms import LoginForm, RegistrationForm
from .services import allow_user_to_login, create_user

user = Blueprint('user',
                 __name__,
                 template_folder='templates',
                 static_folder='static')


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        create_user(form.email.data, form.password.data)
        return redirect(url_for('.login'))
    return render_template('users/register.html', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        current_user = allow_user_to_login(form.email.data, form.password.data)
        login_user(current_user)
        return redirect(url_for('network_interface.list_network_interfaces'))
    return render_template('users/login.html', form=form)


@user.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('user.login'))

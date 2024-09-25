from flask import Blueprint, render_template, redirect, request, url_for, flash

from ..forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user
from ..extensions import db, bcrypt
from ..models.user import User
from ..functions import save_picture


user = Blueprint('user', __name__)

@user.route('/user/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        avatar_img = save_picture(form.avatar.data)
        user = User(name=form.name.data, login=form.login.data, avatar=avatar_img, password=hashed_password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Поздравляем, {form.login.data}! Вы успешно зарегистрированы", "success")            
            return redirect(url_for('user.login'))
        except Exception as e:
            flash(f"При регистрации произошла ошибка", "danger")
            print(str(e))
                    
    else:
        print('Неверный формат вводимых данных')
               
    return render_template('user/registration.html', form = form)

@user.route('/user/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"Пользователь {form.login.data} успешно авторизован", "success")
            return redirect(next_page) if next_page else redirect(url_for('post.all'))
        else:
            flash(f"Ошибка входа, проверьте логин и пароль!", "danger")
    return render_template('user/login.html', form=form)

@user.route('/user/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('post.all'))
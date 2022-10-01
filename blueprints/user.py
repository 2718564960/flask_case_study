from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session, g
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
from datetime import datetime
from .form import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
import string
import random


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        print(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect("/")
            else:
                flash("邮箱和密码不匹配！")
                return redirect(url_for("user.login"))
        else:
            flash("邮箱和密码格式错误！")
            return redirect(url_for("user.login"))

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("user.login"))

@bp.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == "GET":
        print("2")
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        print(request.form)
        if form.validate():
            email = form.email.data
            password = generate_password_hash(form.password.data)
            user_name = form.user_name.data
            user = UserModel(email=email, user_name=user_name, password=password)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for("user.login"))
        else:
            flash(form.errors)
            print(form.password.data)
            print(form.password_confirm.data)
            return render_template("register.html")


@bp.route("/captcha", methods=["POST"])
def get_captcha():
    # GET,POST
    email = request.form.get("email")
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters,4))
    print(captcha)
    if email:
        message = Message(
            subject="user_test",
            recipients=[email],
            body=f"【知了问答】您的注册验证码是：{captcha}",
        )
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email = email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        return jsonify({"code": 200})
    else:
        # code:400
        return jsonify({"code": 400, "message":"请先传递邮箱"})
from flask import Blueprint, render_template, request, redirect, url_for, flash
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
from datetime import datetime
from .form import RegisterForm
from werkzeug.security import generate_password_hash
import string
import random


bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/login")
def login():
    return render_template("login.html")

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


@bp.route("/mail")
def get_captcha():
    # GET,POST
    email = request.args.get("email")
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
        return "success"
    else:
        return "no emails"

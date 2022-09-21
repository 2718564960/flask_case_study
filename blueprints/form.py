import wtforms
from wtforms.validators import length, email, EqualTo, DataRequired
from models import EmailCaptchaModel, UserModel
from flask import flash


class RegisterForm(wtforms.Form):
    user_name = wtforms.StringField('user_name',validators=[DataRequired(message="bitian"),length(min=3, max=20, message="3")])
    email = wtforms.StringField('email',validators=[email()])
    captcha = wtforms.StringField('captcha',validators=[DataRequired(message="bitian"),length(min=4, max=4, message="4")])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo("password",message="hahaha")])


    def captcha_validator(self, field):
        captcha = field.data
        email = self.email.data
        emailcaptcha = EmailCaptchaModel.query.filter_by(email=email).first()
        if not emailcaptcha or emailcaptcha.captcha.lower() != captcha.lower():
            raise wtforms.ValidationError("邮箱验证码错误！")

    def password_confirm_validator(self, field):
        password_confirm = field.data
        password = self.password.data
        if password != password_confirm:
            flash("两次密码不一致！")
            raise wtforms.ValidationError("两次密码不一致！")

    def email_validator(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email = email).first()
        if user_model:
            flash("邮箱已经注册！")
            raise wtforms.ValidationError("邮箱已经注册！")

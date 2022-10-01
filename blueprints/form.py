import wtforms
from wtforms.validators import length, email, EqualTo, DataRequired, InputRequired
from models import EmailCaptchaModel, UserModel
from flask import flash


class RegisterForm(wtforms.Form):
    user_name = wtforms.StringField('user_name',validators=[DataRequired(message="bitian"),length(min=3, max=20, message="用户名长度3-20个字")])
    email = wtforms.StringField('email',validators=[email()])
    captcha = wtforms.StringField('captcha',validators=[DataRequired(message="bitian"),length(min=4, max=4, message="验证码数量不正确")])
    password = wtforms.StringField(validators=[length(min=6, max=20, message="密码长度6-20个字")])
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

class LoginForm(wtforms.Form):
    email = wtforms.StringField('email',validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20,message="密码格式不正确")])

class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3, max=200)])
    content = wtforms.StringField(validators=[length(min=5)])

class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=5)])
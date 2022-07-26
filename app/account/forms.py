from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, length, Email, EqualTo, Regexp, ValidationError
from ..models import db, User


class LoginForm(FlaskForm):
    username = StringField('账号',
                           validators=[DataRequired('请输入学号/工号'),
                                       length(8, 8, "账号长度为8"),
                                       Regexp('^[0-9]', 0, "请输入数字")
                                       ],
                           render_kw={
                               'class': 'form-control input-lg',
                               'placeholder': '请输入学号/工号'
                           },
                           )
    password = PasswordField('密码', validators=[DataRequired("密码不能为空"), length(1, 64, "密码长度在64字符以内")],
                             render_kw={
                                 'class': 'form-control input-lg',
                                 'placeholder': '请输入密码'
                             },
                             )
    # remember_me = BooleanField('保持登录状态',)
    submit = SubmitField('登录',
                         render_kw={
                             'class': "btn btn-info btn-block btn-lg",
                             'placeholder': '登录'
                         })


class RegisterForm(FlaskForm):
    nickname = StringField(label="昵称", validators=[DataRequired("请输入昵称"), length(1, 64, "昵称长度在64字符以内")],
                           render_kw={
                               'class': 'form-control input-lg',
                               "placeholder": "请输入昵称",
                           })
    username = StringField(label="账号",
                           validators=[DataRequired("请输入学号/工号"),
                                       length(8, 8, "账号长度为8"),
                                       Regexp('^[0-9]', 0, "请输入数字")
                                       ],
                           render_kw={
                               'class': 'form-control input-lg',
                               "placeholder": "请输入学号/工号"
                           })
    password = PasswordField(label='密码',
                             validators=[DataRequired("密码不能为空"), length(1, 64, "密码长度在64字符以内"),
                                         EqualTo("password2", message="两次密码不一致")],
                             render_kw={
                                 'class': 'form-control input-lg',
                                 "placeholder": "请输入密码"
                             })
    password2 = PasswordField(label="确认密码", validators=[DataRequired("密码不能为空"), length(1, 64, "密码长度在64字符以内")],
                              render_kw={
                                  'class': 'form-control input-lg',
                                  "placeholder": "请再次输入密码"
                              })
    submit = SubmitField("注册",
                         render_kw={
                             "class": "btn btn-info btn-block btn-lg",

                         })

    def validate_nickname(self, field):
        user = User.query.filter_by(nickname=field.data).first()
        if user:
            raise ValidationError("该昵称已存在")

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError("该用户已存在")


class EditProfile(FlaskForm):
    nickname = StringField(label="昵称", validators=[DataRequired("请输入昵称"), length(1, 64, "昵称长度在64字符以内")],)
    signature = StringField(label="签名", validators=[length(0, 20, "签名长度在20字符以内")])
    school = StringField(label="学院", validators=[length(0, 12, "学院名长度在12字符以内")])
    sex = SelectField(label="性别", validators=[DataRequired("请选择")],
                      choices=[(1, "男"), (2, "女"), (3, "保密")],
                      coerce=int)
    submit = SubmitField("提交")

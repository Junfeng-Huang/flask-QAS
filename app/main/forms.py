from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired, length


class QuestionForm(FlaskForm):
    title = StringField(label="问题", validators=[DataRequired("请输入问题"),
                                                length(1, 64, "问题字符在64以内，请重新提问")],
                        render_kw={
                            "class": "form-control"
                        }
                        )
    desc = TextAreaField(label="问题描述",
                         render_kw={
                             "id": "editor"
                         })
    submit = SubmitField("提交")


class ArticleForm(FlaskForm):
    title = StringField(label="问题", validators=[DataRequired("请输入问题"),
                                                length(1, 64, "问题字符在64以内，请重新提问")],
                        render_kw={
                            "class": "form-control",
                            "placeholder": "请输入文章标题"
                        }
                        )
    body = TextAreaField(label="问题描述",
                         render_kw={
                             "id": "editor",
                             'placeholder': "请输入文章正文"
                         })
    submit = SubmitField("提交",
                         render_kw={
                             'class': "btn btn-info pull-right",

                         })


class AnswerForm(FlaskForm):
    body = TextAreaField(label="回答",
                         render_kw={
                             "id": "editor",
                             'placeholder': "请输入回答"
                         })
    submit = SubmitField("提交",
                         render_kw={
                             'class': "btn btn-info pull-right",

                         })


class CommentForm(FlaskForm):
    body = TextAreaField(label="评论",
                         render_kw={
                             "class": "form-control",
                             "placeholder": "写下你的评论..."
                         })
    submit = SubmitField("提交",
                         render_kw={
                             "class":"btn btn-default btn-grey",

                         })

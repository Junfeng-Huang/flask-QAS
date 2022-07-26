from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, current_user, logout_user
from ..email import send_email
from . import account
from ..models import *
from .forms import LoginForm, RegisterForm, EditProfile


@account.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # ref = request.values.get('ref', request.referrer)  # 用于解决点赞，收藏，关注等使用referrer参数的问题
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):  # next是flask-login的，如果用户访问未授权的URL时会显示登录页面，
                next = url_for('main.index')  # flask-login会把原URL保持在next参数中，且是相对路径。检查'/'是为了防止被恶意利用
            # if ref and "account/login" not in ref:
            #     next = ref
            return redirect(next)
        flash('错误的用户名或密码', category='danger')
    return render_template('account/login.html', form=form)


@account.route("/logout")
@login_required
def logout():
    logout_user()
    flash("退出成功", 'warning')
    return redirect(url_for("main.index"))


@account.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(nickname=form.nickname.data,
                    username=form.username.data,
                    password=form.password.data,
                    email=str(form.username.data) + "@hdu.edu.cn")
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(to=user.email,
                   subject="请确认你的邮箱",
                   template="account/email/confirm",
                   user=user,
                   token=token)
        # flash("注册确认邮件已发送到您的学校邮箱,请注意查收!", 'warning')
        return render_template("account/check_email.html")
    return render_template("account/register.html", form=form)


@account.route('/mine/<int:id>')
@login_required
def mine(id):
    user = User.query.filter_by(id=id).first()
    tag = request.args.get('tag', "follow_question")
    page = request.args.get('page', 1, type=int)
    if user:
        if tag == "article":
            pagination = user.articles.paginate(
                page, per_page=5, error_out=False
            )
        elif tag == "collection":
            pagination = user.collections.paginate(
                page, per_page=5, error_out=False
            )
        elif tag == "answer":
            pagination = user.answers.paginate(
                page, per_page=5, error_out=False
            )
        else:
            pagination = user.question_follow.paginate(
                page, per_page=5, error_out=False
            )
        return render_template("account/mine.html", user=user, id=id, tag=tag, pagination=pagination)
    else:
        abort(404)


@account.route('/edit-profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfile()
    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.signature = form.signature.data
        current_user.school = form.school.data
        if form.sex.data == 1:
            current_user.sex = False
        elif form.sex.data == 2:
            current_user.sex = True
        else:
            current_user.sex = None
        db.session.add(current_user._get_current_object())
        db.session.commit()
        return redirect(url_for('account.mine', id=current_user.id))
    form.nickname.data = current_user.nickname
    form.signature.data = current_user.signature
    form.school.data = current_user.school
    if current_user.sex == 0:
        form.sex.data = 1
    elif current_user.sex == 1:
        form.sex.data = 2
    else:
        form.sex.data = 3
    return render_template("account/edit_profile.html", form=form)


@account.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('邮件确认成功！', category="info")
    else:
        flash("此链接无效或已经过期", category="danger")
    return redirect(url_for('main.index'))


@account.route('/test')
@login_required
def test():
    return "test"


@account.route('/unconfirmed')
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('account/unconfirmed.html', current_user=current_user)


@account.route('/resend_confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认邮箱',
               'account/email/confirm', user=current_user, token=token)
    flash('新的邮件已经发送到您的邮箱.')
    return render_template("account/check_email.html")


@account.before_app_request
def before_request():
    if current_user.is_authenticated and \
            not current_user.confirmed and \
            request.blueprint != 'account' and \
            request.endpoint != 'static':  # current_user.is_authenticated一定要在最前面做判断
        return redirect(url_for('account.unconfirmed'))

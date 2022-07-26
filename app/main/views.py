import bdb
import os
import uuid
from flask import render_template, url_for, request, flash, \
    redirect, current_app, make_response, jsonify, abort, Response
from . import main
from flask_sqlalchemy import get_debug_queries
from flask_login import current_user, login_required
from .forms import QuestionForm, ArticleForm, AnswerForm, CommentForm
from werkzeug.utils import secure_filename
from ..models import *

ALLOWED_EXTENSIONS = {'png', 'jpg', 'gif', 'tif', 'psd', 'raw'}
INDEX_PER_PAGE = 5


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    question_form = QuestionForm()
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.order_by(Question.timestamp.desc()).paginate(
        page, per_page=INDEX_PER_PAGE, error_out=False
    )
    questions = pagination.items
    page_data = []
    for ques in questions:
        ans = ques.answers.first()
        page_data.append((ques, ans))
    return render_template("main/index.html",
                           question_form=question_form,
                           page_data=page_data,
                           pagination=pagination
                           )


@main.route('/index_article', methods=['GET', 'POST'])
@login_required
def index_article():
    question_form = QuestionForm()
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(
        page, per_page=INDEX_PER_PAGE, error_out=False
    )
    page_data = pagination.items
    return render_template("main/index_article.html",
                           question_form=question_form,
                           page_data=page_data,
                           pagination=pagination
                           )


@main.route('/detail/<int:id>', methods=['GET', 'POST'])
@login_required
def detail(id):
    ques = Question.query.filter_by(id=id).first()
    if not ques:
        abort(404)
    answer_form = AnswerForm()
    if answer_form.validate_on_submit():
        answer = Answer(body=answer_form.body.data)
        answer.author = current_user._get_current_object()
        answer.question = ques
        db.session.add(answer)
        db.session.commit()
        answer_form = AnswerForm(formdata=None)
    return render_template('main/detail.html', ques=ques, answer_form=answer_form)


@main.route('/detail_article/<int:id>', methods=['GET', 'POST'])
@login_required
def detail_article(id):
    article = Article.query.filter_by(id=id).first()
    if not article:
        abort(404)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment(body=comment_form.body.data)
        comment.author = current_user._get_current_object()
        comment.article = article
        db.session.add(comment)
        db.session.commit()
        comment_form = CommentForm(formdata=None)
    return render_template('main/detail_article.html', article=article, comment_form=comment_form)


@main.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    question_form = QuestionForm()
    if question_form.validate_on_submit():
        # print(question_form.desc.data)
        _question = Question(title=question_form.title.data,
                             desc=question_form.desc.data)
        _question.author = current_user._get_current_object()
        db.session.add(_question)
        db.session.commit()
        flash("发布问题成功", category='info')  # 应该转到问题详情页，并且自动关注问题
        return redirect(url_for("main.index"))
    for error in question_form.title.errors:
        flash(error, category="danger")
    return redirect(url_for("main.index"))


@main.route('/ans_like/<int:id>', methods=['GET'])
@login_required
def ans_like(id):
    ans = Answer.query.filter_by(id=id).first()
    next_url = request.args.get('next', url_for("main.index"))
    if not ans:
        abort(404)
    user = current_user._get_current_object()
    like = Like.query.filter_by(user_id=user.id, answer_id=ans.id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        return redirect(next_url)
    else:
        like = Like()
        like.user = current_user._get_current_object()
        like.answer = ans
        db.session.add(like)
        db.session.commit()
        return redirect(next_url)


@main.route('/article_like/<int:id>', methods=['GET'])
@login_required
def article_like(id):
    article = Article.query.filter_by(id=id).first()
    next_url = next_url = request.args.get('next', url_for("main.index"))
    if not article:
        abort(404)
    user = current_user._get_current_object()
    like = Like.query.filter_by(user_id=user.id, article_id=article.id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        return redirect(next_url)
    else:
        like = Like()
        like.user = current_user._get_current_object()
        like.article = article
        db.session.add(like)
        db.session.commit()
        return redirect(next_url)


@main.route('/collect_ans/<int:id>', methods=['GET'])
@login_required
def collect_ans(id):
    ans = Answer.query.filter_by(id=id).first()
    if not ans:
        abort(404)
    next_url = next_url = request.args.get('next', url_for("main.index"))
    collection = Collection.query.filter_by(user_id=current_user.id,
                                            answer_id=ans.id).first()
    if collection:
        db.session.delete(collection)
        db.session.commit()
        return redirect(next_url)
    else:
        collection = Collection(user_id=current_user.id,
                                answer_id=ans.id)
        db.session.add(collection)
        db.session.commit()
        return redirect(next_url)


@main.route('/collect_article/<id>')
@login_required
def collect_article(id):
    article = Article.query.filter_by(id=id).first()
    if not article:
        abort(404)
    next_url = next_url = request.args.get('next', url_for("main.index"))
    collection = Collection.query.filter_by(user_id=current_user.id,
                                            article_id=article.id).first()
    if collection:
        db.session.delete(collection)
        db.session.commit()
        return redirect(next_url)
    else:
        collection = Collection(user_id=current_user.id,
                                article_id=article.id)
        db.session.add(collection)
        db.session.commit()
        return redirect(next_url)


@main.route('/follow/<int:id>')
@login_required
def follow(id):
    user = User.query.filter_by(id=id)
    if not user:
        abort(404)
    follow = Follow.query.filter_by(follower_id=current_user.id,
                                    followed_id=id).first()
    next_url = next_url = request.args.get('next', url_for("main.index"))
    if follow:
        db.session.delete(follow)
        db.session.commit()
        return redirect(next_url)
    else:
        follow = Follow(follower_id=current_user.id,
                        followed_id=id)
        db.session.add(follow)
        db.session.commit()
        return redirect(next_url)


@main.route('/follow_question/<int:id>')
@login_required
def follow_question(id):
    ques = Question.query.filter_by(id=id)
    if not ques:
        abort(404)
    follow_ques = QuestionFollow.query.filter_by(user_id=current_user.id,
                                                 question_id=id).first()
    next_url = next_url = request.args.get('next', url_for("main.index"))
    if follow_ques:
        db.session.delete(follow_ques)
        db.session.commit()
        return redirect(next_url)
    else:
        follow_ques = QuestionFollow(user_id=current_user.id,
                                     question_id=id)
        db.session.add(follow_ques)
        db.session.commit()
        return redirect(next_url)


@main.route('/save_image', methods=['GET', 'POST'])
@login_required
def save_image():
    if request.method == 'POST':
        image = request.files['upload']
        file_name = secure_filename(image.filename)
        suffix = file_name.split('.')[-1]
        if suffix.lower() not in ALLOWED_EXTENSIONS:
            response = {
                'uploaded': False,
                'url': None
            }
            flash(message="图片格式仅支持'png', 'jpg', 'gif', 'tif', 'psd', 'raw'",
                  category="danger")
            return jsonify(response)
        file_name = str(uuid.uuid1()) + "." + suffix
        save_dir = os.path.join(current_app.config['UPLOAD_IMAGE_FOLDER'], file_name)
        image.save(save_dir)
        image_url = url_for('main.get_image', file_name=file_name)
        response = {
            'uploaded': True,
            'url': image_url
        }
        return jsonify(response)


@main.route('/get_image/<file_name>', methods=['GET'])
@login_required
def get_image(file_name):
    image_dir = os.path.join(current_app.config.get("UPLOAD_IMAGE_FOLDER"), file_name)
    if not os.path.exists(image_dir):
        return abort(404)
    with open(image_dir, 'rb') as file:
        img = file.read()
    response = make_response(img)
    return response


@main.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    article_form = ArticleForm()
    if article_form.validate_on_submit():
        if len(str(article_form.body.data)) == 0:
            flash("请输入正文", category='danger')
            return render_template("main/write.html", form=article_form)
        article = Article(title=article_form.title.data,
                          body=article_form.body.data)
        article.author = current_user._get_current_object()
        db.session.add(article)
        db.session.commit()
        flash("文章发布成功", category="info")
        return redirect(url_for("main.index"))
    return render_template("main/write.html", form=article_form)


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/test', methods=['GET', 'POST'])
def test():
    question_form = QuestionForm()
    if question_form.validate_on_submit():
        print(question_form.question.data)
        print(question_form.desc.data)
        print('ok')
    return render_template("editor.html", question_form=question_form)

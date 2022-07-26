from flask_mail import Message
from flask import render_template, current_app
from . import mail
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()  # 如果要异步则必须获取当前app对象，因为异步会再开一个线程
    to = to[0:8] + '<' + to + '>'
    msg = Message(subject,
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from config import config
from flask_mail import Mail
import pymysql
import os

pymysql.install_as_MySQLdb()

login_manager = LoginManager()
login_manager.login_view = 'account.login'
login_manager.login_message = "请先登录"
login_manager.login_message_category = 'info'

db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap()


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    basedir = os.path.dirname(__file__)
    app.config['UPLOAD_IMAGE_FOLDER'] = os.path.join(basedir, app.config['UPLOAD_IMAGE_FOLDER'])

    db.init_app(app)
    migrate = Migrate(app, db)

    mail.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    #性能分析
    # from werkzeug.middleware.profiler import ProfilerMiddleware
    # app.wsgi_app = ProfilerMiddleware(app.wsgi_app)

    from .account import account as acount_blueprint
    app.register_blueprint(acount_blueprint, url_prefix='/account')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .filter import html2text
    app.jinja_env.filters['html2text'] = html2text

    return app

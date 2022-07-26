import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "this is a secret key"
    MAIL_SERVER = os.environ.get("MAIL_SERVER",)
    MAIL_PORT = os.environ.get('MAIL_PORT', 465)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', False)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME',)
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD',)
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER',)

    ADMIN_MAIL = os.environ.get('ADMIN_MAIL',)

    SQLALCHEMY_RECORD_QUERIES = os.environ.get("SQLALCHEMY_RECORD_QUERIES", True)
    FLASKY_SLOW_DB_QUERY_TIME = os.environ.get("FLASKY_SLOW_DB_QUERY_TIME", 0.1)

    # database
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = os.environ.get('PASSWORD', )
    HOST = os.environ.get('HOST', )
    PORT = os.environ.get('PORT',)
    DATABASE = os.environ.get('DATABASE', 'flasky')
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    UPLOAD_IMAGE_FOLDER = os.environ.get("UPLOAD_IMAGE_FOLDER", "static/images")


config = {
    "default": Config
}
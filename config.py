import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    CSRF_ENABLED =True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER ='smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    JOKENIA_MAIL_SUBJECT_PREFIX = '[ Jokenia ]'
    JOKENIA_MAIL_SENDER = 'margaretrain.mo@gmail.com'
    JOKENIA_ADMIN = os.environ.get('JOKENIA_ADMIN')
    # the database am working with
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    JOKENIA_POSTS_PER_PAGE = 9
    JOKENIA_COMMENTS_PER_PAGE = 15
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app/static/images/uploads/')
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dev-data.db')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test-data.db')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}





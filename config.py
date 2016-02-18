# DEBUG = True

# import os
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite')
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'gffdfbfvdffd'
#     FLASKY_MAIL_SUBJECT_PREFIX ='[Riding sharing]'
#     FLASKY_MAIL_SENDER = 'Queue Admin <margaretrain.mo@gmail.com>'
#     FLASKY_Admin = os.environ.get('Queue_Admin')
    

DEBUG = True

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# the database am working with
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.sqlite')
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = True

# am using 2 application threads one to handle incomming requests another to perform background operations
THREADS_PER_PAGE = 2
# protection
CSRF_ENABLED = True
CSRF_SESSION_KEY = 'secret'
# key for signing cookies
SECRET_KEY = 'secret'

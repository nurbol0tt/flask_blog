import os

# from elasticsearch import Elasticsearch


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Nuru_141592@localhost/flask_blog'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True

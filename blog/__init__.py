from elasticsearch import Elasticsearch
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from blog.config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'
mail = Mail()
migrate = Migrate()
# es = connect_elasticserch
es = Elasticsearch(['http://localhost:9200'])


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from blog.user.views import user
    from blog.views import main
    from blog.post.views import post
    from blog.comment.views import comment

    app.register_blueprint(user)
    app.register_blueprint(post)
    app.register_blueprint(main)
    app.register_blueprint(comment)

    return app

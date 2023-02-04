from flask import Blueprint, render_template, request
from flask_login import current_user

from blog.models import Post, User

main = Blueprint('main', __name__, template_folder='templates')


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    if current_user.is_anonymous:
        print("*"*20)
        return render_template('index.html', posts=posts)
    else:
        user = User.query.filter_by(id=current_user.id).first()
        print(user.__dir__())
        return render_template('index.html', posts=posts, user=user)
    #
    # return render_template('index.html', posts=posts)

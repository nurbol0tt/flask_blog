from flask import render_template, flash, redirect, url_for, request, abort, Blueprint
from flask_login import current_user, login_required

from blog import db
from blog.post.forms import *

from blog.models import Post, Comment

post = Blueprint('post', __name__)


@post.route('/post/new', methods=['POST', 'GET'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form)


@post.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    reviews = Comment.query.filter_by(post_id=post_id)

    # print(reviews)
    post.views += 1
    db.session.commit()
    return render_template('post.html', title=post.title, post=post, reviews=reviews)


@post.route("/post/<int:post_id>/update", methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user.id:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post.post_detail', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@post.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

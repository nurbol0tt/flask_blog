import requests

from flask import Blueprint, render_template, request
from flask_login import current_user
from elasticsearch_dsl import connections, Search, Q
from elasticsearch import Elasticsearch

from blog.models import Post, User
from blog.forms import SearchForm

main = Blueprint('main', __name__, template_folder='templates')
es = Elasticsearch()


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    if current_user.is_anonymous:
        return render_template('index.html', posts=posts)
    else:
        user = User.query.filter_by(id=current_user.id).first()
        return render_template('index.html', posts=posts, user=user)


# @main.route("/search", methods=["GET"])
# def search():
#     query = request.args.get("q")
#     if query is None or query == "":
#         return "Please provide a valid search query", 400
#     s = Search(using=es, index="post").query("match", title=query)
#     print(s)
#     response = s.execute()
#     return [hit.to_dict() for hit in response], 200
#
#     print(query)
#     results = es.search(index="post", body={
#         "query": {
#             "bool": {
#                 "should": [
#                     {"match": {"title": query}},
#                     {"match": {"description": query}}
#                 ]
#             }
#         }
#     })
#     return results["hits"], 200


# documents = [
#     {"title": "Document 1", "description": "This is the first document"},
#     {"title": "Document 2", "description": "This is the second document"},
#     {"title": "Anime", "description": "naruto"}]
#
# for doc in documents:
#     es.index(index="post", body=doc)

@main.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@main.route('/search', methods=["GET", "POST"])
def search():
    form = SearchForm()
    posts = Post.query
    if form.validate_on_submit():
        # Get data from submitted form
        post_searched = form.searched.data

        if post_searched is None or post_searched == " ":
            print('*'*100)
            posts = Post.query.all()
            return render_template("search.html",
                                   form=form,
                                   posts=posts)
        else:
            posts = Post.query.filter(
                Post.title.like('%' + post_searched + '%')).all()
            results = es.search(index="post", body={
                "query": {
                    "bool": {
                        "should": [
                            {"match": {"title": post_searched}},
                            {"match": {"content": post_searched}}
                        ]
                    }
                }
            })

            return render_template("search.html",
                                   form=form,
                                   searched=results["hits"]["hits"],
                                   posts=posts,
                                   data=post_searched)
    else:
        return render_template("search.html", form=form, posts=posts)
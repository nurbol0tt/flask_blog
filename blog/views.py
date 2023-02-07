from elasticsearch import Elasticsearch
from flask import Blueprint, render_template, request
from flask_login import current_user

from blog import es
from blog.models import Post, User

main = Blueprint('main', __name__, template_folder='templates')


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    if current_user.is_anonymous:
        return render_template('index.html', posts=posts)
    else:
        user = User.query.filter_by(id=current_user.id).first()
        return render_template('index.html', posts=posts, user=user)


@main.route("/search", methods=["POST"])
def search():

    # query = request.args['q'].lower()
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"title": request.args['q'].lower()}},
                    # {"match": {"description": description}}
                ]
            }
        }
    }
    res = es.search(index="your_index", body=query)
    print(res)
    # tokens = query.split(' ')
    # print(tokens)
    # return ''


# @main.route('/search_get', methods=['GET'])
# def index():
#     results = es.get(index='contents', doc_type='title', id='my-new-slug')
#     print(results)
#     # return jsonify(results['_source'])
#
#
# @main.route('/insert_data', methods=['POST'])
# def insert_data():
#     title = request.form['title']
#     content = request.form['content']
#
#     body = {
#         'title': title,
#         'content': content,
#     }
#
#     result = es.index(index='contents', doc_type='title', body=body)
#     print(result)
#     # return jsonify(result)
#
#
# @main.route('/search', methods=['POST'])
# def search():
#     # keyword = request.form['keyword']
#     keyword = 'Синтаксис'
#     body = {
#         "query": {
#             "multi_match": {
#                 "query": keyword,
#                 "fields": ["content", "title"]
#             }
#         }
#     }
#
#     res = es.search(index="contents", doc_type="title", body=body)
#
#     print(res['hits']['hits'])

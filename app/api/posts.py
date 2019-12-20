from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Post, PostSchema
from . import api

# @api.route('/posts/')
# def get_posts():
#     page = request.args.get('page', 1, type=int)
#     pagination = Post.query.paginate(
#         page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
#         error_out=False)
#     posts = pagination.items
#     prev = None
#     if pagination.has_prev:
#         prev = url_for('api.get_posts', page=page-1)
#     next = None
#     if pagination.has_next:
#         next = url_for('api.get_posts', page=page+1)
#     return jsonify({
#         'posts': [post.to_json() for post in posts],
#         'prev': prev,
#         'next': next,
#         'count': pagination.total
#     })
post_schema = PostSchema(session=db.session)


@api.route('/posts/<string:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post_schema.dump(post))


@api.route('/posts/', methods=['POST'])
def new_post():
    post = post_schema.load(request.json)
    db.session.add(post)
    db.session.commit()
    return jsonify(post_schema.dump(post)), 201

# @api.route('/posts/<int:id>', methods=['PUT'])
# @permission_required(Permission.WRITE)
# def edit_post(id):
#     post = Post.query.get_or_404(id)
#     if g.current_user != post.author and \
#             not g.current_user.can(Permission.ADMIN):
#         return forbidden('Insufficient permissions')
#     post.body = request.json.get('body', post.body)
#     db.session.add(post)
#     db.session.commit()
#     return jsonify(post.to_json())
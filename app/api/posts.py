import marshmallow
from flask import jsonify, request, g, url_for, current_app

from app.exceptions import ValidationError
from .. import db
from ..models import Post, PostSchema
from . import api

post_schema = PostSchema(session=db.session)


@api.route('/posts/<string:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post_schema.dump(post))


@api.route('/posts/', methods=['POST'])
def new_post():
    try:
        post = post_schema.load(request.json)
    except Exception as err:
        raise ValidationError(str(err))

    if Post.query.filter_by(instagram_post_hash=post.instagram_post_hash).first():
        raise ValidationError('instagram_post_hash already registered.')
    db.session.add(post)
    db.session.commit()
    return jsonify(post_schema.dump(post)), 201


@api.route('/posts/<string:id>', methods=['PATCH'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(post, key, value)
    db.session.add(post)
    db.session.commit()
    return jsonify(post_schema.dump(post))

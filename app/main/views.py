from flask import render_template, flash, redirect, url_for

from app.main.forms import EditPostForm
from app.models import Post, User
from . import main
from .. import db


@main.route('/', methods=['GET'])
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@main.route('/user/<int:id>', methods=['GET'])
def user(id):
    user = User.query.get_or_404(id)
    return render_template('index.html', user=user)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = EditPostForm(obj=post)
    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    if not post.caption:
        form.caption.data = post.influencer_caption
    return render_template('post.html', post=post, form=form)

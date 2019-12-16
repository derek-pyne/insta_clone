from flask import render_template, flash, redirect, url_for

from app.main.forms import EditPostForm
from app.models import Post
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@main.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    post = Post.query.get_or_404(id)
    form = EditPostForm()
    if form.validate_on_submit():
        # post.body = form.body.data
        # db.session.add(post)
        # db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.caption.data = post.caption
    return render_template('edit_post.html', form=form)

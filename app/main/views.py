from flask import render_template, flash, redirect, url_for

from app.main.forms import EditPostForm, EditManagedInstagramAccountForm
from app.models import Post, User, ManagedInstagramAccount
from . import main
from .. import db


@main.route('/', methods=['GET'])
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@main.route('/user/<int:id>', methods=['GET'])
def user(id: int):
    user = User.query.get_or_404(id)
    return render_template('index.html', user=user)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id: int):
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


@main.route('/managed_instagram_account/', methods=['GET', 'POST'])
def create_managed_instagram_account():
    managed_instagram_account = ManagedInstagramAccount()
    form = EditManagedInstagramAccountForm(obj=managed_instagram_account)
    if form.validate_on_submit():
        form.populate_obj(managed_instagram_account)
        db.session.add(managed_instagram_account)
        db.session.commit()
        flash('The managed Instagram account has been updated.')
        return redirect(url_for('.managed_instagram_account', id=managed_instagram_account.id))
    return render_template('managed_instagram_account.html',
                           managed_instagram_account=managed_instagram_account, form=form)


@main.route('/managed_instagram_account/<int:id>', methods=['GET', 'POST'])
def managed_instagram_account(id: int):
    managed_instagram_account = ManagedInstagramAccount.query.get_or_404(id)
    form = EditManagedInstagramAccountForm(obj=managed_instagram_account)
    if form.validate_on_submit():
        form.populate_obj(managed_instagram_account)
        db.session.add(managed_instagram_account)
        db.session.commit()
        flash('The managed Instagram account has been updated.')
        return redirect(url_for('.managed_instagram_account', id=managed_instagram_account.id))
    return render_template('managed_instagram_account.html',
                           managed_instagram_account=managed_instagram_account, form=form)


@main.route('/managed_instagram_account/<int:id>/feed', methods=['GET'])
def managed_instagram_account_feed(id: int):
    managed_instagram_account = ManagedInstagramAccount.query.get_or_404(id)
    reposts = managed_instagram_account.posts
    return render_template('managed_instagram_account_feed.html',
                           managed_instagram_account=managed_instagram_account,
                           posts=reposts)

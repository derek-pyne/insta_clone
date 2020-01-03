from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from . import db, ma, login_manager


class AuditableMixin:
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class User(AuditableMixin, UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(), unique=True, index=True)
    username = db.Column(db.String(), unique=True, index=True)
    password_hash = db.Column(db.String())
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        dump_only = ['id', 'created_at', 'updated_at']


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


reposts = db.Table('reposts',
                   db.Column('post_id',
                             db.Integer,
                             db.ForeignKey('posts.id')),
                   db.Column('managed_instagram_account_id',
                             db.Integer,
                             db.ForeignKey('managed_instagram_accounts.id'))
                   )


class Post(AuditableMixin, db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    influencer = db.Column(db.String())
    img_file = db.Column(db.String())
    influencer_caption = db.Column(db.String())
    alt_text = db.Column(db.String())
    instagram_post_hash = db.Column(db.String())

    caption = db.Column(db.String())

    def __repr__(self) -> str:
        return '<id {}>'.format(self.id)


class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post
        dump_only = ['id', 'created_at', 'updated_at']

    managed_instagram_accounts = ma.List(ma.Nested('ManagedInstagramAccountSchema', exclude=('posts',)))


class ManagedInstagramAccount(AuditableMixin, db.Model):
    __tablename__ = 'managed_instagram_accounts'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    handle = db.Column(db.String(), unique=True)

    posts = db.relationship('Post',
                            secondary=reposts,
                            backref=db.backref('managed_instagram_accounts', lazy='dynamic'),
                            lazy='dynamic')

    def __repr__(self) -> str:
        return '<id {}, handle {}>'.format(self.id, self.handle)


class ManagedInstagramAccountSchema(ma.ModelSchema):
    class Meta:
        model = ManagedInstagramAccount
        dump_only = ['id', 'created_at', 'updated_at']

    posts = ma.List(ma.Nested(PostSchema, exclude=('managed_instagram_accounts',)))

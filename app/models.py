from . import db, ma


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    influencer = db.Column(db.String())
    img_file = db.Column(db.String())
    influencer_caption = db.Column(db.String())
    alt_text = db.Column(db.String())
    instagram_post_hash = db.Column(db.String())

    caption = db.Column(db.String())

    def __init__(self, instagram_post_hash, influencer, img_file, influencer_caption, alt_text) -> None:
        self.instagram_post_hash = instagram_post_hash
        self.influencer = influencer
        self.influencer_caption = influencer_caption
        self.img_file = img_file
        self.alt_text = alt_text

    def __repr__(self) -> str:
        return '<id {}>'.format(self.id)


class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post

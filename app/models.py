from . import db


class InfluencerPost(db.Model):

    __tablename__ = 'influencer_post'
    id = db.Column(db.String(), primary_key=True)
    influencer = db.Column(db.String())
    img_insta_url = db.Column(db.String())
    caption = db.Column(db.String())
    alt_text = db.Column(db.String())

    def __init__(self, id, influencer, img_insta_url, caption, alt_text) -> None:
        self.id = id
        self.influencer = influencer
        self.img_insta_url = img_insta_url
        self.caption = caption
        self.alt_text = alt_text

    def __repr__(self) -> str:
        return '<id {}>'.format(self.id)
from flask import render_template

from app.models import InfluencerPost
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    influencer_posts = InfluencerPost.query.all()
    return render_template('index.html', influencer_posts=influencer_posts)

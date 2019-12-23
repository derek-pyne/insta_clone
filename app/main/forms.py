from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms_components import read_only


class EditPostForm(FlaskForm):
    influencer_caption = StringField('Influencer caption:', validators=[DataRequired()])
    caption = StringField('Caption:', validators=[DataRequired()])
    alt_text = StringField('Alt Text:', validators=[DataRequired()])
    influencer = StringField('Influencer:', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)
        read_only(self.influencer)
        read_only(self.influencer_caption)

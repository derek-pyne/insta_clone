from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms_components import read_only


class EditPostForm(FlaskForm):
    influencer_caption = StringField('Influencer caption:', validators=[DataRequired()])
    caption = StringField('Caption:', validators=[DataRequired()])
    alt_text = StringField('Alt Text:')
    influencer = StringField('Influencer:', validators=[DataRequired()])
    managed_instagram_accounts = SelectMultipleField('Managed Instagram Accounts: ', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)
        read_only(self.influencer)
        read_only(self.influencer_caption)


class EditManagedInstagramAccountForm(FlaskForm):
    handle = StringField('Handle:', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(EditManagedInstagramAccountForm, self).__init__(*args, **kwargs)

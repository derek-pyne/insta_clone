from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class EditPostForm(FlaskForm):
    caption = StringField('Enter your caption', validators=[DataRequired()])
    submit = SubmitField('Submit')

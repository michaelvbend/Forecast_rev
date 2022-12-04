from wtforms import StringField, PasswordField,  EmailField, SubmitField, SelectField,FloatField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_wtf import FlaskForm

class upload_data(FlaskForm):
    campaign_id = SelectField("Campaign", validators=[DataRequired()])
    target_col = SelectField("Target", validators=[DataRequired()])
    eu_to_spend = FloatField("Euro")
    submit = SubmitField('Submit')



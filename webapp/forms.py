from wtforms import StringField, PasswordField,  EmailField, SubmitField, SelectField,FloatField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_wtf import FlaskForm
from model import User, Predictions

class upload_data(FlaskForm):
    @staticmethod
    def validate_user_id(prediction_name, user_id):
        predict = Predictions.query.filter_by(prediction_name=prediction_name, user_id=user_id).first()
        return False if predict else True

    prediction_name = StringField("Prediction_Name", validators=[DataRequired()])
    campaign_id = SelectField("Campaign", validators=[DataRequired()])
    target_col = SelectField("Target", validators=[DataRequired()])
    eu_to_spend = FloatField("Euro")
    submit = SubmitField('Submit')

class LoginUser(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterUser(FlaskForm):
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists! Please choose another one.')

    username = StringField("Username", validators=[DataRequired()])
    password1 = PasswordField("password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField("Register")


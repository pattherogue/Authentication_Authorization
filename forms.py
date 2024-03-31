# Import necessary modules and classes from WTForms and Flask-WTF
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email
from flask_wtf import FlaskForm

# Define LoginForm class for user login
class LoginForm(FlaskForm):
    """Login form."""
    # Define username field with validators
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    # Define password field with validators
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )

# Define RegisterForm class for user registration
class RegisterForm(FlaskForm):
    """User registration form."""
    # Define username field with validators
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    # Define password field with validators
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )
    # Define email field with validators
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )
    # Define first name field with validators
    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(max=30)],
    )
    # Define last name field with validators
    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(max=30)],
    )

# Define FeedbackForm class for adding feedback
class FeedbackForm(FlaskForm):
    """Add feedback form."""
    # Define title field with validators
    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=100)],
    )
    # Define content field with validators
    content = StringField(
        "Content",
        validators=[InputRequired()],
    )

# Define DeleteForm class for deleting feedback (empty form)
class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""

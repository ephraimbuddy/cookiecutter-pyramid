from wtforms import Form
from wtforms import StringField, PasswordField, validators


class LoginForm(Form):
    username = StringField(
        "Username",
        validators=[validators.DataRequired()]
    )
    password = PasswordField(
        "Password",
        validators=[validators.DataRequired()]
    )


class RegistrationForm(Form):
    username = StringField(
        "Username",
        validators=[validators.DataRequired(),
                    validators.Length(min=3, max=30)]
    )
    email = StringField(
        "Email",
        validators=[validators.DataRequired(),
                    validators.Email(message="invalid email address"),
                    validators.Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password",
        validators=[validators.DataRequired(),
                    validators.Length(min=6, max=40)]
    )


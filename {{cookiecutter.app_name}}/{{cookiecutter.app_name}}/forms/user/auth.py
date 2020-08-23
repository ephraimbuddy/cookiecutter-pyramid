from {{cookiecutter.app_name}}.forms import BaseForm, strip_filter
from wtforms import StringField, PasswordField, validators


class LoginForm(BaseForm):
    username = StringField(
        "Username",
        validators=[validators.DataRequired()],
        filters=[strip_filter]
    )
    password = PasswordField(
        "Password",
        validators=[validators.DataRequired()]
    )


class RegistrationForm(BaseForm):
    username = StringField(
        "Username",
        validators=[validators.DataRequired(),
                    validators.Length(min=3, max=30)]
    )
    email = StringField(
        "Email",
        validators=[validators.DataRequired(),
                    validators.Email(message="invalid email address"),
                    validators.Length(min=6, max=40)],
        filters=[strip_filter]
    )
    password = PasswordField(
        "Password",
        validators=[validators.DataRequired(),
                    validators.Length(min=6, max=40)]
    )


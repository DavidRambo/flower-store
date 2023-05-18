from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    FileField,
    IntegerField,
    PasswordField,
    StringField,
    SubmitField,
    FloatField,
)
from wtforms.validators import DataRequired, NumberRange, ValidationError

from flower_store.models import Flower


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class AddFlowerForm(FlaskForm):
    """Form to add a new flower to the catalog."""

    name = StringField("Name", validators=[DataRequired()])
    stock = IntegerField("stock", validators=[NumberRange(min=0, max=None)])
    image = FileField("image", validators=[FileAllowed("jpg", "png")])
    bloom_size = FloatField("Size of bloom in inches")
    height = FloatField("Height in feet")
    submit = SubmitField("Add to catalog")

    def validate_name(self, name):
        flower = Flower.query.filter_by(name=name.data).first()
        if flower:
            raise ValidationError("A flower by that name already exists.")


class UpdateFlowerForm(FlaskForm):
    """Form to modify an existing flower in the catalog.

    TODO: Find out how to get the primary_key id of the flower being updated.
    See FMT EditProfileForm in main.forms and /edit_profile route in main.routes.
    """

    name = StringField("name", validators=[DataRequired()])
    stock = IntegerField("stock", validators=[NumberRange(min=0, max=None)])
    image = FileField("image", validators=[FileAllowed("jpg", "png")])
    bloom_size = FloatField("Size of bloom in inches")
    height = FloatField("Height in feet")
    submit = SubmitField("Update")

    def validate_name(self, name):
        # TODO: Find a way to compare new name to current name and allow match.
        flower = Flower.query.filter_by(name=name.data).first()
        if flower:
            raise ValidationError("A flower by that name already exists.")

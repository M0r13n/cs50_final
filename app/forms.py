from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class UploadForm(FlaskForm):
    file = FileField(
        "Image",
        validators=[
            FileRequired(message="You need to pass a file!"),
            FileAllowed(["jpeg", "jpg"], "Only Jpeg's are allowed (.jpeg, .jpg)")
        ]
    )
    submit = SubmitField(
        "Convert"
    )

import datetime
from enum import Enum

from flask_uploads import UploadSet, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import RadioField, IntegerField, SubmitField
from wtforms.validators import DataRequired

from app import app, db
from app.domain import WordList, Rule, NONE_ENUM

EXTENSIONS = ('cap',)
TIMEOUT_HASHCAT_MINUTES = 120


def _wordlist_choices():
    return tuple(wordlist.value for wordlist in (WordList.ROCKYOU, WordList.PHPBB))


def _choices_from(*enums: Enum):
    choices = [(NONE_ENUM, '(None)')]
    for item in enums:
        choices.append((item.value, item.value))
    return choices


class UploadedTask(db.Model):
    __tablename__ = "uploads"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    filename = db.Column(db.String(128))
    wordlist = db.Column(db.String(128))
    rule = db.Column(db.String(128))
    uploaded_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    duration = db.Column(db.Interval, default=datetime.timedelta)
    status = db.Column(db.String(256), default="Scheduled")
    progress = db.Column(db.Float, default=0)
    found_key = db.Column(db.String(256))


class UploadForm(FlaskForm):
    wordlist = RadioField('Wordlist', choices=_choices_from(WordList.ROCKYOU, WordList.PHPBB), default=NONE_ENUM)
    rule = RadioField('Rule', choices=_choices_from(Rule.BEST_64), default=NONE_ENUM)
    timeout = IntegerField('Timeout (minutes)', validators=[DataRequired()], default=TIMEOUT_HASHCAT_MINUTES)
    capture = FileField('Capture',
                        validators=[FileRequired(), FileAllowed(EXTENSIONS, message='Airodump capture files only')])
    submit = SubmitField('Submit')


cap_uploads = UploadSet(name='files', extensions=EXTENSIONS, default_dest=lambda app: app.config['CAPTURES_DIR'])
configure_uploads(app, cap_uploads)

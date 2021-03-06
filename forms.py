from wtforms import (
	StringField,
	TextAreaField,
	PasswordField,
	BooleanField,
	SubmitField,
	Form,
	validators,
)
from wtforms.validators import (
	DataRequired,
	EqualTo,
	Length,
	ValidationError
)
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from models import Knot
from login.hash import encrypt_string
import re
from models import slugify, Post
from app import db


class RegistrationForm(FlaskForm):
	f_name = StringField('First name*', 
		validators=[DataRequired()], id='first name*')
	s_name = StringField('Last name*',
		validators=[DataRequired()], id='last name*')
	username = StringField('Username*',
		validators=[DataRequired()], id='username*')
	email = StringField('Email*',
		validators=[DataRequired()], id='email*')
	number = StringField('Phone number', id='phone number')
	password = PasswordField('New Password*',
		validators=[DataRequired()], id='password*')
	confirm = PasswordField('Repeat password*',
		validators=[DataRequired(),
					EqualTo('password', message='Passwords do not match')],
		id='repeat password*')
	#accept_tos = BooleanField('I accept the TOS',
	#	validators=[DataRequired()])

	def validate_email(form, email):
		try:
			email = re.match(r"^[a-zA-Z0-9_'+*/^&=?~{}\-](\.?[a-zA-Z0-9_'+*/^&=?~{}\-])*\@((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d{1,3})?)|(((([a-zA-Z0-9][a-zA-Z0-9\-]+[a-zA-Z0-9])|([a-zA-Z0-9]{1,2}))[\.]{1})+([a-zA-Z]{2,6})))$", email.data).string
			if Knot.query.filter_by(email=email).first() is not None:
				raise ValidationError('''This email number is reserved.''')
		except AttributeError:
			raise ValidationError('''Invalid email''')

	def validate_number(form, number):
		if number.data:
			try:
				num = re.match(r"^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$", number.data).string
				if Knot.query.filter_by(number=num).first() is not None:
					raise ValidationError('''This phone number is reserved.\n
						Please use another number.''')
			except AttributeError:
				raise ValidationError('''Invalid number''')
		else:
			pass

	def validate_username(form, username):
		if Knot.query.filter_by(username=username.data).first() is not None:
			raise ValidationError('Please use a different username.')
			# может следует добавить ссылку на инициалы узла 
			# который зарегистрирован под этим username

	#submit = SubmitField('register')

class LoginForm(FlaskForm):
	username = StringField('Username',
		validators=[DataRequired()])
	password = PasswordField('Password',
		validators=[DataRequired()])
	#remember_me = BooleanField('Remember me')

	def validate_username(form, username):
		if Knot.query.filter_by(username=username.data).first() is None:
			raise ValidationError('Invalid username')


	def validate_password(form, password):
		if Knot.query.filter_by(password=encrypt_string(password.data)).first() is None:
			raise ValidationError('Invalid password')
	

class PostForm(FlaskForm):
	title = StringField('Title',
		validators=[DataRequired(), Length(4, 78)])
	preview = StringField('Preview',
		validators=[DataRequired(), Length(50, 250)])
	body = CKEditorField('Body',
		validators=[DataRequired(), Length(250, 50000)])
	tags = StringField('Tag',
		validators=[DataRequired(), Length(3, 100)])

	
	def validate_tags(form, tags):
		invalid_chars = re.findall(r"[!@#$%^&*()~`\-+=\/?\|:\;'\"{}\\.\[\]]", str(tags._value()))
		invalid_tags = []
		if invalid_chars:
			for char in invalid_chars:
				for tag in str(tags._value()).split():
					if char in tag:
						invalid_tags.append(tag)
			raise ValidationError(f'\
				<span style="color: red;">Invalid char in {"tags" if len(invalid_tags) > 1 else "tag"}\
				</span> <span style="color: black;">\
				{" ".join(tag for tag in invalid_tags)}</span>:\
				<span style="color: red;">{", ".join(char for char in invalid_chars)}</span>')


class CommentForm(FlaskForm):
	text = TextAreaField('Text',
		validators=[DataRequired(), Length(1, 2000)])

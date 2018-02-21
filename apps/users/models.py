  # Inside models.py
from __future__ import unicode_literals
from django.db import models
from django.core.validators import EmailValidator

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email_address = models.CharField(max_length=255, validators=[EmailValidator], unique=True)	
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

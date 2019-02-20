from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    displayName = models.CharField(max_length=200)
    github = models.URLField(blank=True)
    bio = models.CharField(max_length=256, blank=True)


class Post(models.Model):
	CONTENTCHOICES = (
		("text/plain", "Plain"),
		("text/markdown", "Markdown"),
		("application/base64", "Base64"),
		("img/png;base64", "PNG"),
		("image/jpeg;base64", "JPEG")
	)

	VISIBILITY = (
		("PUBLIC", "Public"),
		("PRIVATE", "Private")
	)

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=200)
	source = models.URLField(blank=True)
	origin = models.URLField(blank=True)
	description = models.CharField(max_length=400)
	contentType = models.CharField(max_length=18, choices=CONTENTCHOICES, default="text/plain")
	content = models.BinaryField()
	published = models.DateTimeField(auto_now_add=True)
	visibility = models.CharField(max_length=7, choices=VISIBILITY, default="PUBLIC")
	unlisted = models.BooleanField(default=False)

	# missing author, comments, and categories


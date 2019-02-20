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
	PLAIN = "text/plain"
	MARKDOWN = "text/markdown"
	BASE64 = "application/base64"
	PNG = "image/png;base64"
	JPEG = "image/jpeg;base64"

	CONTENTCHOICES = (
		(PLAIN, "Plain"),
		(MARKDOWN, "Markdown"),
		(BASE64, "Base64"),
		(PNG, "PNG"),
		(JPEG, "JPEG")
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
	contentType = models.CharField(max_length=18, choices=CONTENTCHOICES, default=PLAIN)
	content = models.BinaryField()
	published = models.DateTimeField()
	visibility = models.CharField(max_length=7, choices=VISIBILITY, default="PUBLIC")
	unlisted = models.BooleanField(default=False)

	# missing author, comments, and categories


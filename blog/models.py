from django.db import models
from simblog import settings
import social_auth

class Author(models.Model):
	first_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)

	def __str__(self):
		return self.first_name + ' ' + self.last_name

class Post(models.Model):
	title = models.CharField(max_length=200)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(Author)
	text = models.TextField()
	
	def __str__(self):
		return self.title

class Comment(models.Model):
	post = models.ForeignKey(Post)
	reply_to = models.ForeignKey('self', blank=True, null=True)
	author = models.ForeignKey(Author)
	created = models.DateTimeField(auto_now_add=True)
	text = models.TextField()

class Tag(models.Model):
	name = models.TextField(max_length=32)
	def __str__(self):
		return self.name

class PostTag(models.Model):
	post = models.ForeignKey(Post)
	tag = models.ForeignKey(Tag)
	class Meta:
		unique_together = ["post", "tag"]
	def __str__(self):
		return str(self.post) + ' - ' + str(self.tag)
from django.db import models

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
	#modified = models.DateTimeField(auto_now=True)
	text = models.TextField()
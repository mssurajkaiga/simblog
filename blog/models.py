from django.db import models
from simblog import settings
from social_auth.models import UserSocialAuth

class Post(models.Model):
	title = models.CharField(max_length=200)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(UserSocialAuth)
	text = models.TextField()
	
	def __str__(self):
		return self.title

class Comment(models.Model):
	post = models.ForeignKey(Post)
	reply_to = models.ForeignKey('self', blank=True, null=True)
	author = models.ForeignKey(UserSocialAuth)
	created = models.DateTimeField(auto_now_add=True)
	text = models.TextField()

class Tag(models.Model):
	name = models.TextField(max_length=32)
	alt_name = models.TextField(max_length=32, null=True, blank=True)
	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if(self.alt_name==None or self.alt_name==''):
			self.alt_name = self.name.replace(' ', '_')
		if(self.alt_name.find(' ') != -1):
			self.alt_name = self.alt_name.replace(' ', '_')
		super(Tag, self).save(*args, **kwargs)

class PostTag(models.Model):
	post = models.ForeignKey(Post)
	tag = models.ForeignKey(Tag)
	class Meta:
		unique_together = ["post", "tag"]
	def __str__(self):
		return str(self.post) + ' - ' + str(self.tag)
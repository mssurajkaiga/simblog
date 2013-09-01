from django.db import models
from simblog import settings
from social_auth.models import UserSocialAuth
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import urllib, json

class Author(models.Model):
	user = models.OneToOneField(UserSocialAuth)
	provider_icon = models.CharField(max_length=32)
	link = models.CharField(max_length=200)

	def save(self, *args, **kwargs):
		if self.user.provider == 'google-oauth2':
			self.provider_icon = 'google'
			self.link = 'mailto:'+self.user.uid
		elif self.user.provider == 'facebook':
			self.provider_icon = 'facebook'
			u = urllib.urlopen('https://graph.facebook.com/{}'.format(self.user.uid));
			user_stream = json.loads(u.read())
			self.link = user_stream['link']
		elif self.user.provider == 'github':
			self.provider_icon = 'github'
			self.link = 'http://github.com/'+self.user.user.get_username()
						
		super(Author, self).save(*args, **kwargs)

	def __str__(self):  
		return "%s's profile" % self.user 

def create_author(sender, instance, created, **kwargs):
	print 'Created UserSocialAuth instance, Created = {}'.format(created)
	if created:  
		profile, created = Author.objects.get_or_create(user=instance)

post_save.connect(create_author, sender=UserSocialAuth)


class Post(models.Model):
	title = models.CharField(max_length=200)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(User)
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
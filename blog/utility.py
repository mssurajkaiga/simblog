from blog.models import *

def search_by_tag(tag):
	posttags = PostTag.objects.filter(tag=Tag.objects.get(alt_name=tag))
	posts = []
	for posttag in posttags:
		posts.append(posttag.post)

	return posts

def search_post_by_title(title):
	posts = Post.objects.filter(title=title)
	return posts

def search_post_by_created(created):
	posts = Post.objects.filter(created=created)
	return posts

def search_post_by_text(text):
	posts = Post.objects.filter(text__contains=text)
	return posts

def get_tags_by_posts(posts):
	tags = []
	for post in posts:
		for posttag in PostTag.objects.filter(post=post):
			tags.append(posttag.tag)
	tags = list(set(tags))
	return tags
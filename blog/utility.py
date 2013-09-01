from blog.models import *
from django.db.models import Q
from datetime import datetime

MAX_RECENT_POSTS = 3

def trim_data(posts):
	for post in posts:
		if len(post.text)>500:
			post.text = post.text[:500] + '<a href="/blog/post/{}">...[Read More]</a>'.format(post.id)
	return posts

def search_by_tag(tag):
	posttags = PostTag.objects.filter(tag=Tag.objects.get(alt_name=tag))
	posts = []
	for posttag in posttags:
		posts.append(posttag.post)

	return posts

def search_by_tags(tags):
	posttags = []
	for tag in tags:
		for posttag in PostTag.objects.filter(tag=tag):
			if posttag not in posttags:
				posttags.append(posttag)
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
	posts = Post.objects.filter(text__icontains=text)
	return posts

def get_tags_by_posts(posts):
	tags = []
	for post in posts:
		for posttag in PostTag.objects.filter(post=post):
			tags.append(posttag.tag)
	tags = list(set(tags))
	return tags

def search_all(data):
	dataset = data.split(' ')
	result_posts = []
	result_tags = []
	result_comments = []
	for data in dataset:
		result_posts.extend(Post.objects.filter(Q(title__icontains=data) | Q(text__icontains=data)))
		result_comments.extend(Comment.objects.filter(Q(text__icontains=data)))
		result_tags.extend(Tag.objects.filter(Q(name__icontains=data) | Q(alt_name__icontains=data)))

	result_posts = list(set(result_posts))
	result_comments = list(set(result_comments))
	result_tags = list(set(result_tags))
	result_posts = trim_data(result_posts)
	tags = get_tags_by_posts(result_posts)
	if (not (result_posts or result_comments or result_tags)):
		return None

	if (not (result_posts or result_comments) and result_tags):
		result_posts = search_by_tags(result_tags)
		tags = result_tags
		
	return {'result_posts': result_posts, 'result_tags': result_tags, 'result_comments': result_comments, 'tags': tags}

def get_all_posts():
	posts = Post.objects.order_by('created').all()
	recent_posts = []
	rev = list(reversed(posts))
	for post in rev[:3]:
		recent_posts.append(post)
	return [posts, recent_posts]

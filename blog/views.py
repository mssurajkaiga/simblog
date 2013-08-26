from django.http import HttpResponse
from django.shortcuts import render
from django.core.context_processors import csrf
from blog.models import *
from blog.forms import *
import re

from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages

from social_auth import __version__ as version
from social_auth.utils import setting

from blog.utility import *

def post(request, post_id):
	post = Post.objects.get(id = post_id)
	comments = Comment.objects.filter(post=post)
	word_count = len(re.findall("\w+", post.text))
	posttags = PostTag.objects.filter(post=post)
	tags = []
	for posttag in posttags:
		tags.append(posttag.tag)

	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			form.save()
			comment = Comment(post=post, reply_to=None)
			form = CommentForm(instance=comment)
			return render(request, 'post.html', {'post': post, 'comments':comments, 'word_count':word_count, 'form':form, 'tags':tags})
	else:
		comment = Comment(post=post, reply_to=None)
		form = CommentForm(instance=comment)
	print tags
	return render(request, 'post.html', {'post': post, 'comments':comments, 'word_count':word_count, 'form': form, 'tags':tags})

def posts(request, year):
	output = []
	form_is_saved = False
	if year=='all':
		posts = Post.objects.all()
	else:	
		posts = Post.objects.filter(created__year=year)

	for post in posts:
		if (request.method == 'POST' and not form_is_saved):
			form = CommentForm(request.POST)
			if form.is_valid():
				form.save()
				form_is_saved = True
				comment = Comment(post=post, reply_to=None)
				form = CommentForm(instance=comment)

		else:
			comment = Comment(post=post, reply_to=None)
			form = CommentForm(instance=comment)
		comments = Comment.objects.filter(post=post)
		output.append([post, comments, form])

	return render(request, 'posts.html', {'posts': output})

def posts_by_month(request, year, month):
	posts = Post.objects.filter(created__year=year, created__month=month)
	return render(request, 'posts.html', {'posts': posts})

def posts_by_day(request, year, month, day):
	posts = Post.objects.filter(created__year=year, created__month=month, created__day=day)
	return render(request, 'posts.html', {'posts': posts})

def posts_by_tag(request, tag):
	posttags = PostTag.objects.filter(tag=Tag.objects.get(alt_name=tag))
	tags = []
	posts = []
	for posttag in posttags:
		posts.append(posttag.post)
		for posttag2 in PostTag.objects.filter(post=posttag.post):
			tags.append(posttag2.tag)
	tags = list(set(tags))
	return render(request, 'posts.html', {'posts': posts, 'tags':tags})

#Search functionality
def search_by_text(request, text):
	posts = search_post_by_text(text)
	tags = get_tags_by_posts(posts)
	return render(request, 'posts.html', {'posts': posts, 'tags':tags})

@login_required
def complete(request):
    """Login complete view, displays user data"""
    print request
    return render(request, 'members.html')


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/blog/')

def index(request):
	return HttpResponse("Index Page")
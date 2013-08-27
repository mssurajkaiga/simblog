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
	if request.user.is_authenticated():
		request.user.logged_in = True
	else:
		request.user.logged_in = False
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
	return render(request, 'post.html', {'post': post, 'comments':comments, 'word_count':word_count, 'form': form, 'tags':tags})

def posts(request, year):
	if request.user.is_authenticated():
		request.user.logged_in = True
	else:
		request.user.logged_in = False
	output = []
	form_is_saved = False
	if year=='all':
		posts = Post.objects.all()
	else:	
		posts = Post.objects.filter(created__year=year)
	tags = get_tags_by_posts(posts)
	return render(request, 'posts.html', {'posts': posts, 'tags':tags})

def posts_by_month(request, year, month):
	if request.user.is_authenticated():
		request.user.logged_in = True
	else:
		request.user.logged_in = False
	posts = Post.objects.filter(created__year=year, created__month=month)
	tags = get_tags_by_posts(posts)
	return render(request, 'posts.html', {'posts': posts, 'tags':tags})

def posts_by_day(request, year, month, day):
	if request.user.is_authenticated():
		request.user.logged_in = True
	else:
		request.user.logged_in = False
	posts = Post.objects.filter(created__year=year, created__month=month, created__day=day)
	tags = get_tags_by_posts(posts)
	return render(request, 'posts.html', {'posts': posts, 'tags':tags})

def posts_by_tag(request, tag):
	if request.user.is_authenticated():
		request.user.logged_in = True
	else:
		request.user.logged_in = False
	posttags = PostTag.objects.filter(tag=Tag.objects.get(alt_name=tag))
	posts = []
	for posttag in posttags:
		posts.append(posttag.post)
	tags = get_tags_by_posts(posts)
	return render(request, 'posts.html', {'posts': posts, 'tags':tags})

#Search functionality
def search(request, data):
	if request.user.is_authenticated():
		request.user.logged_in = True
	else:
		request.user.logged_in = False
	result = search_all(data)
	if not result:
		return render(request, 'search.html', {'msg': 'Search returned no results!'})	
	return render(request, 'search.html', result)

@login_required
def complete(request):
	if request.user.is_authenticated():
		request.user.logged_in = True
	else:
		request.user.logged_in = False
	return render(request, 'members.html')


def logout(request):
	if request.user.is_authenticated():
		request.user.logged_in = True
	else:
		request.user.logged_in = False
	auth_logout(request)
	return HttpResponseRedirect('/blog/posts/all')

def index(request):
	if request.user.is_authenticated():
		request.user.logged_in = True
	else:
		request.user.logged_in = False
	return HttpResponseRedirect('/blog/posts/all')
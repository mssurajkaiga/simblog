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
	all_posts, recent_posts = get_all_posts()
	search_form = SearchForm()
	tags = []
	for posttag in posttags:
		tags.append(posttag.tag)

	if request.user.is_authenticated():
		if request.method == 'POST':
			form = CommentForm(request.POST)
			if form.is_valid():
				user = UserSocialAuth.objects.get(user_id=request.user.id)
				form.save(user)
				comment = Comment(post=post, reply_to=None)
				form = CommentForm(instance=comment)
				comments = Comment.objects.filter(post=post)
				return render(request, 'post.html', {'post': post, 'comments':comments, 'word_count':word_count, 'form':form, 'search_form':search_form, 'tags':tags, 'all_posts':all_posts, 'recent_posts':recent_posts})
		else:
			comment = Comment(post=post, reply_to=None)
			form = CommentForm(instance=comment)
			return render(request, 'post.html', {'post': post, 'comments':comments, 'word_count':word_count, 'form': form, 'search_form':search_form, 'tags':tags, 'all_posts':all_posts, 'recent_posts':recent_posts})
	else:
		request.user.logged_in = False
	return render(request, 'post.html', {'post': post, 'comments':comments, 'word_count':word_count, 'search_form':search_form, 'tags':tags, 'all_posts':all_posts, 'recent_posts':recent_posts})

def posts(request, year):
	if request.user.is_authenticated():
		request.user.logged_in = True
	else:
		request.user.logged_in = False
	output = []
	form_is_saved = False
	if year=='all':
		posts = Post.objects.all().order_by('-created')
		home = True
	else:	
		posts = Post.objects.filter(created__year=year).order_by('-created')
		home = False
	search_form = SearchForm()
	posts = trim_data(posts)
	tags = get_tags_by_posts(posts)
	all_posts, recent_posts = get_all_posts()
	return render(request, 'posts.html', {'posts': posts, 'tags':tags, 'all_posts':all_posts, 'recent_posts':recent_posts, 'search_form':search_form, 'home':home})

def posts_by_month(request, year, month):
	if request.user.is_authenticated():
		request.user.logged_in = True
	else:
		request.user.logged_in = False
	posts = Post.objects.filter(created__year=year, created__month=month).order_by('-created')
	search_form = SearchForm()
	tags = get_tags_by_posts(posts)
	posts = trim_data(posts)
	all_posts, recent_posts = get_all_posts()
	return render(request, 'posts.html', {'posts': posts, 'tags':tags, 'search_form':search_form, 'all_posts':all_posts, 'recent_posts':recent_posts})

def posts_by_day(request, year, month, day):
	if request.user.is_authenticated():
		request.user.logged_in = True
	else:
		request.user.logged_in = False
	posts = Post.objects.filter(created__year=year, created__month=month, created__day=day).order_by('-created')
	tags = get_tags_by_posts(posts)
	posts = trim_data(posts)
	search_form = SearchForm()
	all_posts, recent_posts = get_all_posts()
	return render(request, 'posts.html', {'posts': posts, 'tags':tags, 'search_form':search_form, 'all_posts':all_posts, 'recent_posts':recent_posts})

def posts_by_tag(request, tag):
	if request.user.is_authenticated():
		request.user.logged_in = True
	else:
		request.user.logged_in = False
	posttags = PostTag.objects.filter(tag=Tag.objects.get(alt_name=tag))
	posts = []
	for posttag in posttags:
		posts.append(posttag.post)
	posts = sorted(posts, key= lambda post: post.created, reverse=True)
	tags = get_tags_by_posts(posts)
	posts = trim_data(posts)
	search_form = SearchForm()
	all_posts, recent_posts = get_all_posts()
	return render(request, 'posts.html', {'posts': posts, 'tags':tags, 'search_form':search_form, 'all_posts':all_posts, 'recent_posts':recent_posts})

#Search functionality
def search(request):
	if request.user.is_authenticated():
		request.user.logged_in = True
	else:
		request.user.logged_in = False
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			result = search_all(form.cleaned_data['data'])
		else:
			result = None
			form = SearchForm()
	else:
		result = None
		form = SearchForm()	

	all_posts, recent_posts = get_all_posts()
	if not result:
		return render(request, 'search.html', {'msg': 'Search returned no results!', 'search_form':form, 'all_posts':all_posts, 'recent_posts':recent_posts})
	else:
		result = dict({'search_form':form, 'all_posts':all_posts, 'recent_posts':recent_posts}, **result)
	return render(request, 'search.html', result)

def about(request):
	if request.user.is_authenticated():
		request.user.logged_in = True
	else:
		request.user.logged_in = False
	all_posts, recent_posts = get_all_posts()
	search_form = SearchForm()
	return render(request, 'about.html', {'all_posts': all_posts, 'recent_posts': recent_posts, 'search_form':search_form})

def contact(request):
	if request.user.is_authenticated():
		request.user.logged_in = True
	else:
		request.user.logged_in = False
	all_posts, recent_posts = get_all_posts()
	search_form = SearchForm()
	return render(request, 'about.html', {'all_posts': all_posts, 'recent_posts': recent_posts, 'search_form':search_form})

@login_required
def complete(request):
	if request.user.is_authenticated():
		request.user.logged_in = True
	else:
		request.user.logged_in = False
	return HttpResponseRedirect('/blog/posts/all')

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
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

def post(request, post_id):
	post = Post.objects.get(id = post_id)
	comments = Comment.objects.filter(post=post)
	word_count = len(re.findall("\w+", post.text))
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			form.save()
			comment = Comment(post=post, reply_to=None)
			form = CommentForm(instance=comment)
			return render(request, 'post.html', {'post': post, 'comments':comments, 'word_count':word_count, 'form':form})
	else:
		comment = Comment(post=post, reply_to=None)
		form = CommentForm(instance=comment)
	return render(request, 'post.html', {'post': post, 'comments':comments, 'word_count':word_count, 'form': form})

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
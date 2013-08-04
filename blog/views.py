from django.http import HttpResponse
from django.shortcuts import render
from django.core.context_processors import csrf
from blog.models import *
from blog.forms import *

def post(request, post_id):
	post = Post.objects.get(id = post_id)
	comments = Comment.objects.filter(post=post)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			form.save()
			comment = Comment(post=post, reply_to=None)
			form = CommentForm(instance=comment)
			return render(request, 'post.html', {'post': post, 'comments':comments, 'form':form})
	else:
		comment = Comment(post=post, reply_to=None)
		form = CommentForm(instance=comment)
	return render(request, 'post.html', {'post': post, 'comments':comments, 'form': form})

def posts(request, year):
	output = []
	if year=='all':
		posts = Post.objects.all()
	else:	
		posts = Post.objects.filter(created__year=year)

	for post in posts:
			comments = Comment.objects.filter(post=post)
			output.append([post,comments])

	return render(request, 'posts.html', {'posts': output})

def posts_by_month(request, year, month):
	posts = Post.objects.filter(created__year=year, created__month=month)
	return render(request, 'posts.html', {'posts': posts})

def posts_by_day(request, year, month, day):
	posts = Post.objects.filter(created__year=year, created__month=month, created__day=day)
	return render(request, 'posts.html', {'posts': posts})


def index(request):
	return HttpResponse("Index Page")
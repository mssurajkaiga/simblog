#from django import forms

from django.forms import ModelForm, HiddenInput, Textarea
from blog.models import Comment

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ('created', )
		widgets = {
			'post': HiddenInput(),
			'reply_to': HiddenInput(),
			'text': Textarea(attrs={'cols':30, 'rows':4})
		}
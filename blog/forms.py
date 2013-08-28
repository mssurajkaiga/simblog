#from django import forms
from django.forms.formsets import formset_factory
from django.forms import ModelForm, HiddenInput, Textarea
from blog.models import Comment

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ('created', 'author')
		widgets = {
			'post': HiddenInput(),
			'reply_to': HiddenInput(),
			'text': Textarea(attrs={'style':'width:40%;', 'rows':2})
		}

	def save(self, user, *args, **kwargs):
		commit = kwargs.pop('commit', True)
		instance = super(CommentForm, self).save(*args, commit = False, **kwargs)
		instance.author = user 
		if commit:
		    instance.save()
		return instance
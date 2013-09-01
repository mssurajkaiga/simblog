#from django import forms
from django.forms.formsets import formset_factory
from django.forms import Form, CharField, ModelForm, HiddenInput, TextInput, Textarea
from blog.models import Comment, Author

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ('created', 'author')
		widgets = {
			'post': HiddenInput(),
			'reply_to': HiddenInput(),
			'text': Textarea(attrs={'type':"text",'placeholder':"Comment...", 'style':'width:70%; max-width: 80%; height: 20px; resize:none;', 'rows':1})
		}

	def save(self, user, *args, **kwargs):
		commit = kwargs.pop('commit', True)
		instance = super(CommentForm, self).save(*args, commit = False, **kwargs)
		instance.author = user.author
		if commit:
		    instance.save()
		return instance

class SearchForm(Form):
	data = CharField(max_length=100)
	widgets = {
			'data': TextInput(attrs={'class':'span2', 'id':'appendedInputButton', 'type':"text", 'placeholder':"Search..."})
		}

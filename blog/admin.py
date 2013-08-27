from django.contrib import admin
from blog.models import Post, Comment, Tag, PostTag
#from social_auth.models import UserSocialAuth

#admin.site.register(UserSocialAuth)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(PostTag)
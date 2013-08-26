import social_auth

from django.http import HttpResponseRedirect

def get_user(backend, details, response, social_user, uid,\
                    user, *args, **kwargs):
    url = None
    print backend, type(backend)
    print details, type(details)
    print social_user, type(social_user)
    print user, type(user)
from django.http.response import HttpResponseRedirect
from apps.mds_auth.models import Profile


def username(strategy, user=None, *args, **kwargs):
    if user:
        username = user.username
    else:
        username = strategy.session_get('saved_username')
    return {'username': username}

def redirect_to_form(strategy, *args, **kwargs):
    if strategy.session_get('saved_first_name'):
        return HttpResponseRedirect('/form2/')
    
def save_profile(backend, user, response, *args, **kwargs):
    '''
    Reads profile information from oauth resource provider and stores
    it in the user's profile.
    '''
    profile, created = Profile.objects.get_or_create(user=user)
    if backend.name == 'facebook':
        if 'gender' in response:
            profile.gender = response.get('gender')[0]
        profile.facebook = response.get('link')
        profile.save()
    if backend.name == 'google-oauth2':
        if 'gender' in response:
            profile.gender = response.get('gender')[0]
        profile.gplus = response.get('link')
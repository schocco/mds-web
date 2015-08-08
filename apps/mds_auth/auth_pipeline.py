import urllib
from django.http.response import HttpResponseRedirect
from apps.mds_auth.models import Profile

# due to security settings using custom url schemes or other hosts is restricted by django and PSA
# Using a param for the current host should work on all devices capable to intercept requests made by the browser engine
DEFAULT_DEVICE_REDIRECT_URI = "/access_token?token={0}"


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


def device_redirect(strategy, backend, uid, response, *args, **kwargs):
    # pop redirect value before the session is trashed on login(), but after
    # the pipeline so that the pipeline can change the redirect if needed
    data = backend.strategy.request_data()
    redirect_value = backend.strategy.session_get('next', '') or \
                     data.get('next', '')

    token = response['access_token']
    if redirect_value in ("/android", urllib.quote_plus("/android")):
        # TODO: document additional settings
        backend.strategy.session_set('next',
                                     (backend.setting('LOGIN_REDIRECT_URL_ANDROID') or
                                      DEFAULT_DEVICE_REDIRECT_URI).format(token))
        pass
    elif redirect_value in ("/ubuntu", urllib.quote_plus("/ubuntu")):
        backend.strategy.session_set('next',
                                     (backend.setting('LOGIN_REDIRECT_URL_UBUNTU') or
                                      DEFAULT_DEVICE_REDIRECT_URI).format(token))

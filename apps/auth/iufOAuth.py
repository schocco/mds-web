from social.backends.oauth import BaseOAuth2
# see http://psa.matiasaguirre.net/docs/backends/implementation.html

class IUFOAuth2(BaseOAuth2):
    """Github OAuth authentication backend"""
    name = 'github'
    AUTHORIZATION_URL = 'https://iufinc.org/login/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://iufinc.org/login/oauth/access_token'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Returns user details from IUF account"""
        return {'username': response.get('user'),
                'email': response.get('email') or '',
                'first_name': response.get('first_name')}
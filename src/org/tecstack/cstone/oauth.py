from flask import current_app, url_for, request, redirect, session
from rauth import OAuth1Service, OAuth2Service

import json

class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)


    @classmethod
    def get_provider(cls, provider_name):
        if cls.providers is None:
            cls. providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]


class FacebookSignIn(OAuthSignIn):

    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
                    scope='email',
                    response_type='code',
                    redirect_uri=self.get_callback_url()))

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data = {
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url()
            }
        )
        me = oauth_session.get('me').json()
        return (
            'facebook$' + me['id'],
            me.get('email').split('@')[0],
            me.get('email')
        )


class DoubanSignIn(OAuthSignIn):
    def __init__(self):
        super(DoubanSignIn, self).__init__('douban')
        self.service = OAuth2Service(
            name='douban',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://www.douban.com/service/auth2/auth',
            access_token_url='https://www.douban.com/service/auth2/token',
            base_url='http://api.douban.com/labs/bubbler/'
        )
    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(decoder=json.loads,
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()}
        )
        me = oauth_session.get('user/ahbei').json()
        # import pdb
        # pdb.set_trace()
        return (
            'douban$' + me['id'],
            me['uid'],
            me['homepage']
        )

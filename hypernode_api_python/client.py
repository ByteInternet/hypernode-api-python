from requests import Session

HYPERNODE_API_URL = 'https://api.hypernode.com'


class HypernodeAPIPython:
    def __init__(self, token, api_url=None):
        self.session = Session()
        self.token = token
        self.api_url = api_url if api_url else HYPERNODE_API_URL
        self.authorization_header = 'Token {}'.format(self.token)

    def requests(self, method, path, *args, **kwargs):
        kwargs.setdefault('headers', {}).update({
            'Accept': 'application/json',
            'Authorization': self.authorization_header,
            'Accept-Language': 'en-US'
        })
        return session.request(method, HYPERNODE_API_URL.rstrip('/') + path, *args, **kwargs)

    def get_app_flavor(self, app_name):
        return self.requests('GET', HYPERNODE_API_APP_FLAVOR_ENDPOINT.format(app_name))

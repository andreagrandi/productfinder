import requests
from django.conf import settings


def get_products(search_terms=None):
    if search_terms:
        api_root_url = getattr(settings, 'API_ROOT_URL', None)
        api_token = getattr(settings, 'API_TOKEN', None)

        if api_root_url and api_token:
            search_params = '+'.join(search_terms)
            url = '{0}{1}'.format(api_root_url, search_params)

            headers = {
                'Authorization':
                    'MSAuth apikey={0}'.format(
                        api_token
                    )}

            r = requests.get(url, headers=headers)

            if r.status_code == 200:
                return r.json()['search']['results']

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['allauth_ui', 'allauth_ui.templatetags']

package_data = \
{'': ['*'],
 'allauth_ui': ['locale/es/LC_MESSAGES/*',
                'locale/fr/LC_MESSAGES/*',
                'static/allauth_ui/*',
                'templates/account/*',
                'templates/socialaccount/*',
                'templates/socialaccount/snippets/*']}

install_requires = \
['django-rosetta>=0.10.0,<0.11.0', 'django-widget-tweaks>=1.4.12,<2.0.0']

setup_kwargs = {
    'name': 'django-allauth-ui',
    'version': '0.3.0',
    'description': '',
    'long_description': 'None',
    'author': 'Dani Hodovic',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.2',
}


setup(**setup_kwargs)

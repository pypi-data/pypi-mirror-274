from io import open
from setuptools import setup

"""
:authors: Alexander Laptev, CW
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2024 Alexander Laptev, CW
"""

version = "1.5.1"
'''
with open('', encoding='utf-8') as file:
    long_description = file.read()
'''

long_description = '''Python module for Business users in Telegram 
                   (For admin - business-person; Manager CW Bot API). 
                   Docs: https://docs.cwr.su/'''

setup(
    name='manager_cw_bot_api',
    version=version,

    author='Alexander Laptev, CW',
    author_email='cwr@cwr.su',

    description=(
            u'Python module for Business users in Telegram '
            u'(For admin - business-person; Manager CW Bot API). '
            u'Docs: https://docs.cwr.su/'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/cwr-su/manager_cw_bot_api',
    download_url='https://github.com/cwr-su/manager_cw_bot_api/archive/refs/heads/main.zip',

    license='Apache License, Version 2.0, see LICENSE file',

    packages=['manager_cw_bot_api'],
    install_requires=['PyMySQL', 'pyTelegramBotAPI', 'requests', 'telegram-types'],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
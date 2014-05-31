# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from setuptools import setup, find_packages

version = '1.0'

setup(
      name = 'apitest',
      version = version,

      scripts = ['console/apitest'],

      author = 'Dariusz Suchojad',
      author_email = 'dsuch at zato.io',
      url = 'https://zato.io/',
      description = 'API Testing for Humans',
      long_description = 'API Testing for Humans',
      platforms = ['OS Independent'],
      license = 'GNU Lesser General Public License v3 (LGPLv3)',

      package_dir = {'':b'src'},
      packages = find_packages(b'src'),

      namespace_packages = [b'zato'],

      zip_safe = False,

      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'Topic :: Education :: Testing',
        'Topic :: Internet',
        'Topic :: Internet :: Proxy Servers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Networking',
        'Topic :: Utilities',
        ],
)
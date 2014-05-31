# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
import random, uuid

random.seed()

def rand_string():
    return uuid.uuid4().hex

def rand_int(min=0, max=100):
    return random.choice(range(min, max))

def rand_float(min, max):
    return float(rand_int(min, max)) + random.random()
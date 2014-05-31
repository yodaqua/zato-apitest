# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
import datetime, operator, random, uuid
from datetime import timedelta

# Arrow
from arrow import api as arrow_api

# Dateutil
from dateutil.parser import parse as parse_dt

random.seed()

def rand_string():
    return uuid.uuid4().hex

def rand_int(min=0, max=100):
    return random.choice(range(min, max))

def rand_float(min, max):
    return float(rand_int(min, max)) + random.random()

def rand_date(format, start=None, stop=None):
    if not(start and stop):
        # Now is as random as any other date
        return now(format)

def now(format):
    return arrow_api.now().format(format)

def utcnow(format):
    return arrow_api.utcnow().format(format)

def date_after_before(base_date, format, direction, limit, needs_parse=True):
    if needs_parse:
        base_date = parse_dt(base_date)

    days=rand_int(0, abs(limit))
    return arrow_api.get(direction(base_date, timedelta(days=days))).format(format)

def date_after(base_date, format, limit=100000, needs_parse=True):
    return date_after_before(base_date, format, operator.add, limit, needs_parse)

def date_before(base_date, format, limit=100000, needs_parse=True):
    return date_after_before(base_date, format, operator.sub, limit, needs_parse)

def date_between(start_date, end_date, format):
    start_date = parse_dt(start_date)
    end_date = parse_dt(end_date)

    diff = int((start_date - end_date).days)
    func = date_after if end_date > start_date else date_before
    return func(start_date, format, diff, False)
# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Filip Kłosowski <filip at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# Originally part of Zato - open-source ESB, SOA, REST, APIs and cloud integrations in Python
# https://zato.io

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
from datetime import datetime
from dateutil.relativedelta import relativedelta
from unittest import TestCase

# Bunch
from bunch import Bunch

# Zato
from zato.apitest import util
from zato.apitest.steps import json, common

# ###############################################################################################################################

class GivenTestCase(TestCase):
    def setUp(self):
        self.ctx = Bunch()
        self.ctx.zato = util.new_context(None, util.rand_string(), {})
        self.format = common.given_format(self.ctx,'JSON')
        self.request = common.given_request_is(self.ctx, '{}')

    def test_given_json_pointer_in_request_is(self):
        path, value = util.rand_string(2)
        json.given_json_pointer_in_request_is(self.ctx, '/' + path, value)
        self.assertEquals(self.ctx.zato.request.data_impl[path], value)

    def test_given_json_pointer_in_request_is_an_integer(self):
        path = util.rand_string()
        value = util.rand_int()
        json.given_json_pointer_in_request_is_an_integer(self.ctx, '/' + path, value)
        self.assertEquals(self.ctx.zato.request.data_impl[path], int(value))

    def test_given_json_pointer_in_request_is_a_float(self):
        path = util.rand_string()
        value = util.rand_float()
        json.given_json_pointer_in_request_is_a_float(self.ctx, '/' + path, value)
        self.assertEquals(self.ctx.zato.request.data_impl[path], float(value))

    def test_given_json_pointer_in_request_is_a_list(self):
        path = util.rand_string()
        value = str(util.rand_string(2))
        json.given_json_pointer_in_request_is_a_list(self.ctx, '/' + path, value)
        self.assertEquals(self.ctx.zato.request.data_impl[path], util.parse_list(value))

    def test_given_json_pointer_in_request_is_a_random_string(self):
        path = util.rand_string()
        json.given_json_pointer_in_request_is_a_random_string(self.ctx, '/' + path)
        self.assertEquals(len(self.ctx.zato.request.data_impl[path]), 33)
        self.assertEquals(self.ctx.zato.request.data_impl[path][0], 'a')

    def test_given_json_pointer_in_request_is_a_random_integer(self):
        path = util.rand_string()
        json.given_json_pointer_in_request_is_a_random_integer(self.ctx, '/' + path)
        self.assertIs(type(self.ctx.zato.request.data_impl[path]), int)

    def test_given_json_pointer_in_request_is_a_random_float(self):
        path = util.rand_string()
        json.given_json_pointer_in_request_is_a_random_float(self.ctx, '/' + path)
        self.assertIs(type(self.ctx.zato.request.data_impl[path]), float)

    def test_given_json_pointer_in_request_is_one_of(self):
        path = util.rand_string()
        value = ''.join((path, util.rand_string()))
        json.given_json_pointer_in_request_is_one_of(self.ctx, '/' + path, value)
        self.assertEquals(self.ctx.zato.request.data_impl[path], util.any_from_list(value))

    def test_given_json_pointer_is_rand_date_default_format(self):
        path = util.rand_string()
        json.given_json_pointer_is_rand_date(self.ctx, '/' + path, 'default')
        assert datetime.strptime(self.ctx.zato.request.data_impl[path], '%Y-%m-%dT%H:%M:%S')

    def test_given_json_pointer_is_rand_date_non_default_format(self):
        path = util.rand_string()
        self.ctx.zato.date_formats['new'] = 'YY-DD-MM'
        json.given_json_pointer_is_rand_date(self.ctx, '/' + path, 'new')
        assert datetime.strptime(self.ctx.zato.request.data_impl[path], '%y-%d-%m')

    def test_given_json_pointer_is_utc_now(self):
        path = util.rand_string()
        json.given_json_pointer_is_utc_now(self.ctx, '/' + path, 'default')
        utc_now = datetime.strptime(self.ctx.zato.request.data_impl[path], '%Y-%m-%dT%H:%M:%S')
        timedelta_threshold = 50 # microseconds
        self.assertLessEqual((datetime.now() - utc_now).seconds * 10**-3, timedelta_threshold)

    def test_given_json_pointer_is_now(self):
        path = util.rand_string()
        json.given_json_pointer_is_now(self.ctx, '/' + path, 'default')
        utc_now = datetime.strptime(self.ctx.zato.request.data_impl[path], '%Y-%m-%dT%H:%M:%S')
        timedelta_threshold = 50 # microseconds
        self.assertLessEqual((datetime.now() - utc_now).seconds * 10**-3, timedelta_threshold)

    def test_given_json_pointer_is_rand_date_after(self):
        path = util.rand_string()
        rand_date = (datetime.now().strftime('%Y-%m-%d'))
        json.given_json_pointer_is_rand_date_after(self.ctx, '/' + path, rand_date, 'default')
        rand_date_after = datetime.strptime(self.ctx.zato.request.data_impl[path], '%Y-%m-%dT%H:%M:%S')
        self.assertGreater(rand_date_after, datetime.strptime(rand_date, '%Y-%m-%d'))

    def test_given_json_pointer_is_rand_date_before(self):
        path = util.rand_string()
        rand_date = (datetime.now().strftime('%Y-%m-%d'))
        json.given_json_pointer_is_rand_date_before(self.ctx, '/' + path, rand_date, 'default')
        rand_date_after = datetime.strptime(self.ctx.zato.request.data_impl[path], '%Y-%m-%dT%H:%M:%S')
        self.assertLess(rand_date_after, datetime.strptime(rand_date, '%Y-%m-%d'))

    def test_given_json_pointer_is_rand_date_between(self):
        path = util.rand_string()
        date_start = (datetime.now().strftime('%Y-%m-%d'))
        date_end = (datetime.now() + relativedelta(months=6)).strftime('%Y-%m-%d')
        json.given_json_pointer_is_rand_date_between(self.ctx, '/' + path, date_start, date_end, 'default')
        rand_date_between = datetime.strptime(self.ctx.zato.request.data_impl[path], '%Y-%m-%dT%H:%M:%S')
        self.assertLess(datetime.strptime(date_start, '%Y-%m-%d'), rand_date_between)
        self.assertGreater(datetime.strptime(date_end, '%Y-%m-%d'), rand_date_between)

class ThenTestCase(TestCase):
    def setUp(self):
        self.ctx = Bunch()
        self.ctx.zato = util.new_context(None, util.rand_string(), {})
        self.ctx.zato.response = Bunch()
        self.ctx.zato.response.data = Bunch()
        self.ctx.zato.response.data_impl = Bunch()

    def test_then_json_pointer_is(self):
        path, value = util.rand_string(2)
        self.ctx.zato.response.data_impl[path] = util.rand_string()
        self.assertRaises(AssertionError, json.then_json_pointer_is, self.ctx, '/' + path, value)

    def test_then_json_pointer_is_an_integer(self):
        path, value = util.rand_string(2)
        value = util.rand_int()
        self.ctx.zato.response.data_impl[path] = util.rand_int()
        self.assertRaises(AssertionError, json.then_json_pointer_is_an_integer, self.ctx, '/' + path, value)

    def test_then_json_pointer_is_a_float(self):
        path = util.rand_string()
        value = util.rand_float()
        self.ctx.zato.response.data_impl[path] = util.rand_float()
        self.assertRaises(AssertionError, json.then_json_pointer_is_a_float, self.ctx, '/' + path, value)

    def test_then_json_pointer_is_a_list(self):
        path, value = util.rand_string(2)
        self.ctx.zato.response.data_impl[path] = [util.rand_string]
        self.assertRaises(AssertionError, json.then_json_pointer_is_a_list, self.ctx, '/' + path, value)

    def test_then_json_pointer_is_empty(self):
        path = util.rand_string()
        self.ctx.zato.response.data_impl[path] = util.rand_string()
        self.assertRaises(AssertionError, json.then_json_pointer_is_empty, self.ctx, '/' + path)

    def test_then_json_pointer_isnt_empty(self):
        path = util.rand_string()
        self.ctx.zato.response.data_impl[path] = ''
        self.assertRaises(AssertionError, json.then_json_pointer_isnt_empty, self.ctx, '/')

    def test_then_json_pointer_is_one_of(self):
        path, value = util.rand_string(2)
        self.ctx.zato.response.data_impl[path] = util.rand_string()
        self.assertRaises(AssertionError, json.then_json_pointer_is_one_of, self.ctx, '/' + path, value)

    def test_then_json_pointer_isnt_one_of(self):
        path = util.rand_string()
        value = ','.join((path, util.rand_string()))
        self.ctx.zato.response.data_impl[path] = path
        self.assertRaises(AssertionError, json.then_json_pointer_isnt_one_of, self.ctx, '/' + path, value)

    def test_then_json_pointer_is_true(self):
        path = util.rand_string()
        self.ctx.zato.response.data_impl[path] = False
        self.assertRaises(AssertionError, json.then_json_pointer_is_true, self.ctx, '/' + path)

    def test_then_json_pointer_is_false(self):
        path = util.rand_string()
        self.ctx.zato.response.data_impl[path] = True
        self.assertRaises(AssertionError, json.then_json_pointer_is_false, self.ctx, '/' + path)
        
    def test_then_json_pointer_is_an_empty_list(self):
        path = util.rand_string()
        self.ctx.zato.response.data_impl[path] = util.rand_string(2)
        self.assertRaises(AssertionError, json.then_json_pointer_is_an_empty_list, self.ctx, '/' + path)

    def test_then_json_pointer_is_an_empty_dict(self):
        path = util.rand_string()
        self.ctx.zato.response.data_impl[path] = {}
        self.assertTrue(json.then_json_pointer_is_an_empty_dict(self.ctx, '/' + path))

    def test_then_json_pointer_isnt_a_string(self):
        path, value = util.rand_string(2)
        self.ctx.zato.response.data_impl[path] = value
        self.assertRaises(AssertionError, json.then_json_pointer_isnt_a_string, self.ctx, '/' + path, value)

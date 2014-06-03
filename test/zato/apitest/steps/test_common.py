# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
from json import loads
from unittest import TestCase

# Bunch
from bunch import Bunch

# lxml
from lxml import etree

# mock
from mock import patch

# Zato
from zato.apitest import util
from zato.apitest.steps import common
from zato.apitest.test import JSONEchoAdapter, xml_c14nize, XMLEchoAdapter

class WhenTestCase(TestCase):
    def test_when_the_url_is_invoked_xml(self):

        data = '<a><b>cc</b></a>'
        data_impl = etree.fromstring(data)
        data_c14n = xml_c14nize(data_impl)

        method = 'POST'
        address = 'http://{}.example.com'.format(util.rand_string())
        url_path = '/{}'.format(util.rand_string())
        qs = '?{}={}'.format(*util.rand_string(2))
        headers = {util.rand_string():util.rand_string(), util.rand_string():util.rand_string()}

        ctx = Bunch(zato=Bunch(request=Bunch()))

        ctx.zato.request.is_xml = True
        ctx.zato.request.data_impl = data_impl
        ctx.zato.request.method = method
        ctx.zato.request.address = address
        ctx.zato.request.url_path = url_path
        ctx.zato.request.qs = qs
        ctx.zato.request.headers = headers

        common.when_the_url_is_invoked(ctx, [XMLEchoAdapter(b'<dummy/>')])
        sent_request = loads(etree.fromstring(ctx.zato.response.data.text).xpath('/response')[0].text)

        # Confirms the headers we sent were received.
        for key, value in headers.items():
            self.assertEquals(sent_request['request']['headers'][key], value)

        # Confirms the body we sent was received.
        self.assertEquals(xml_c14nize(sent_request['request']['data']), data_c14n)

    def test_when_the_url_is_invoked_json(self):

        data_impl = {'a': {'b': 'cc'}}

        method = 'POST'
        address = 'http://{}.example.com'.format(util.rand_string())
        url_path = '/{}'.format(util.rand_string())
        qs = '?{}={}'.format(*util.rand_string(2))
        headers = {util.rand_string():util.rand_string(), util.rand_string():util.rand_string()}

        ctx = Bunch(zato=Bunch(request=Bunch()))

        ctx.zato.request.is_xml = False
        ctx.zato.request.is_json = True
        ctx.zato.request.data_impl = data_impl
        ctx.zato.request.method = method
        ctx.zato.request.address = address
        ctx.zato.request.url_path = url_path
        ctx.zato.request.qs = qs
        ctx.zato.request.headers = headers

        common.when_the_url_is_invoked(ctx, [JSONEchoAdapter({})])
        sent_request = loads(ctx.zato.response.data_impl['data'])

        # Confirms the headers we sent were received.
        for key, value in headers.items():
            self.assertEquals(sent_request['request']['headers'][key], value)

        # Confirms the body we sent was received.
        self.assertDictEqual(loads(sent_request['request']['data']), data_impl)

class GivenTestCase(TestCase):

    def setUp(self):
        self.ctx = Bunch()
        self.ctx.zato = util.new_context(None, util.rand_string())

    def test_given_address(self):
        value = util.rand_string()
        common.given_address(self.ctx, value)
        self.assertEquals(self.ctx.zato.request.address, value)

    def test_given_url_path(self):
        value = util.rand_string()
        common.given_url_path(self.ctx, value)
        self.assertEquals(self.ctx.zato.request.url_path, value)

    def test_given_http_method(self):
        value = util.rand_string()
        common.given_http_method(self.ctx, value)
        self.assertEquals(self.ctx.zato.request.method, value)

    def test_given_format(self):
        value = util.rand_string()
        common.given_format(self.ctx, value)
        self.assertEquals(self.ctx.zato.request.format, value)

    def test_given_user_agent_is(self):
        value = util.rand_string()
        common.given_user_agent_is(self.ctx, value)
        self.assertEquals(self.ctx.zato.request.headers['User-Agent'], value)

    def test_given_header(self):
        header, value = util.rand_string(2)
        common.given_header(self.ctx, header, value)
        self.assertEquals(self.ctx.zato.request.headers[header], value)

    def test_given_soap_action(self):
        value = util.rand_string()
        common.given_soap_action(self.ctx, value)
        self.assertEquals(self.ctx.zato.request.headers['SOAPAction'], value)

    def test_given_request_impl_xml(self):
        value = util.rand_string()
        data = '<abc>{}</abc>'.format(value)
        self.ctx.zato.request.format = 'XML'
        common.given_request_impl(self.ctx, data)

        self.assertEquals(self.ctx.zato.request.is_xml, True)
        self.assertEquals(self.ctx.zato.request.is_json, False)
        self.assertEquals(self.ctx.zato.request.data_impl.xpath('/abc')[0].text, value)

    def test_given_request_impl_json(self):
        value = util.rand_string()
        data = '{"abc":"%s"}' % value
        self.ctx.zato.request.format = 'JSON'
        common.given_request_impl(self.ctx, data)

        self.assertEquals(self.ctx.zato.request.is_xml, False)
        self.assertEquals(self.ctx.zato.request.is_json, True)
        self.assertEquals(self.ctx.zato.request.data_impl['abc'], value)

    def test_given_request_xml_no_data(self):

        class _RequestPath(object):
            def __init__(self):
                self.value = util.rand_string()

            def __nonzero__(self):
                return False

        _base_dir = util.rand_string()
        _format = 'XML'
        _request_path = _RequestPath()

        def get_full_path(base_dir, format, req_or_resp, request_path):
            self.assertEquals(base_dir, _base_dir)
            self.assertEquals(format, _format.lower())
            self.assertEquals(req_or_resp, 'request')
            self.assertEquals(request_path.value, _request_path.value)

        def get_file(*ignored_args, **ignored_kwargs):
            pass

        with patch('zato.apitest.util.get_full_path', get_full_path):
            with patch('zato.apitest.util.get_file', get_file):
                self.ctx.zato.request.format = 'XML'
                self.ctx.zato.environment_dir = _base_dir

                self.assertRaises(ValueError, common.given_request, self.ctx, _request_path)

    def test_given_request_xml(self):
        value = util.rand_string()

        _base_dir = util.rand_string()
        _format = 'XML'
        _request_path = util.rand_string()

        def get_full_path(base_dir, format, req_or_resp, request_path):
            self.assertEquals(base_dir, _base_dir)
            self.assertEquals(format, _format.lower())
            self.assertEquals(req_or_resp, 'request')
            self.assertEquals(request_path, _request_path)

        def get_file(*ignored_args, **ignored_kwargs):
            return '<abc>{}</abc>'.format(value)

        with patch('zato.apitest.util.get_full_path', get_full_path):
            with patch('zato.apitest.util.get_file', get_file):
                self.ctx.zato.request.format = _format
                self.ctx.zato.environment_dir = _base_dir

                common.given_request(self.ctx, _request_path)

                self.assertEquals(self.ctx.zato.request.is_xml, True)
                self.assertEquals(self.ctx.zato.request.is_json, False)
                self.assertEquals(self.ctx.zato.request.data_impl.xpath('/abc')[0].text, value)

    def test_given_request_json(self):
        value = util.rand_string()

        _base_dir = util.rand_string()
        _format = 'JSON'
        _request_path = util.rand_string()

        def get_full_path(base_dir, format, req_or_resp, request_path):
            self.assertEquals(base_dir, _base_dir)
            self.assertEquals(format, _format.lower())
            self.assertEquals(req_or_resp, 'request')
            self.assertEquals(request_path, _request_path)

        def get_file(*ignored_args, **ignored_kwargs):
            return '{"abc":"%s"}' % value

        with patch('zato.apitest.util.get_full_path', get_full_path):
            with patch('zato.apitest.util.get_file', get_file):
                self.ctx.zato.request.format = _format
                self.ctx.zato.environment_dir = _base_dir

                common.given_request(self.ctx, _request_path)

                self.assertEquals(self.ctx.zato.request.is_xml, False)
                self.assertEquals(self.ctx.zato.request.is_json, True)
                self.assertEquals(self.ctx.zato.request.data_impl['abc'], value)

    def test_given_request_is(self):
        _ctx, _data = util.rand_string(2)

        def given_request_impl(ctx, data):
            self.assertEquals(ctx, _ctx)
            self.assertEquals(data, _data)

        with patch('zato.apitest.steps.common.given_request_impl', given_request_impl):
            common.given_request_is(_ctx, _data)

    def test_given_query_string(self):
        value = util.rand_string()
        common.given_query_string(self.ctx, value)
        self.assertEquals(self.ctx.zato.request.query_string, value)

    def test_given_i_store_value_under_name(self):
        value, name = util.rand_string(2)
        common.given_i_store_value_under_name(self.ctx, value, name)
        self.assertEquals(self.ctx.zato.user_data[name], value)

class ThenTestCase(TestCase):

    def setUp(self):
        self.ctx = Bunch()
        self.ctx.zato = util.new_context(None, util.rand_string())
        self.ctx.zato.response = Bunch()
        self.ctx.zato.response.data = Bunch()
        self.ctx.zato.response.data.headers = {}

    def test_then_context_is_cleaned_up(self):
        _ctx = Bunch()
        _ctx.zato = util.rand_string()

        def new_context(ctx, environment_dir):
            self.assertDictEqual(ctx, _ctx)
            self.assertIsNone(environment_dir)

        with patch('zato.apitest.util.new_context', new_context):
            common.then_context_is_cleaned_up(_ctx)

    def test_then_status_is_ok(self):
        expected = actual = util.rand_int()
        self.ctx.zato.response.data.status_code = actual
        self.assertTrue(common.then_status_is(self.ctx, expected))

    def test_then_status_is_not_ok(self):
        expected, actual = util.rand_int(count=2)
        self.ctx.zato.response.data.status_code = actual
        self.assertRaises(AssertionError, common.then_status_is, self.ctx, expected)

    def test_then_status_is_needs_an_int(self):
        expected = util.rand_string()
        actual = util.rand_int()
        self.ctx.zato.response.data.status_code = actual
        self.assertRaises(ValueError, common.then_status_is, self.ctx, expected)

    def test_then_header_is_ok(self):
        name = util.rand_string()
        expected = actual = util.rand_string()
        self.ctx.zato.response.data.headers[name] = actual
        self.assertTrue(common.then_header_is(self.ctx, name, expected))

    def test_then_header_is_not_ok(self):
        name = util.rand_string()
        expected, actual = util.rand_string(2)
        self.ctx.zato.response.data.headers[name] = actual
        self.assertRaises(AssertionError, common.then_header_is, self.ctx, name, expected)

    def test_then_header_isnt_ok(self):
        name = util.rand_string()
        expected, actual = util.rand_string(2)
        self.ctx.zato.response.data.headers[name] = actual
        self.assertTrue(common.then_header_isnt(self.ctx, name, expected))

    def test_then_header_isnt_not_ok(self):
        name = util.rand_string()
        expected = actual = util.rand_string()
        self.ctx.zato.response.data.headers[name] = actual
        self.assertRaises(AssertionError, common.then_header_isnt, self.ctx, name, expected)

    def test_then_header_contains_ok(self):
        name = util.rand_string()
        substring = util.rand_string()
        actual = substring + util.rand_string()
        self.ctx.zato.response.data.headers[name] = actual
        self.assertTrue(common.then_header_contains(self.ctx, name, substring))

    def test_then_header_contains_not_ok(self):
        name = util.rand_string()
        substring = util.rand_string()
        actual = substring + util.rand_string()
        self.ctx.zato.response.data.headers[name] = actual
        self.assertRaises(AssertionError, common.then_header_contains, self.ctx, name, util.rand_string())

    def test_then_header_doesnt_contain_ok(self):
        name = util.rand_string()
        substring = util.rand_string()
        actual = substring + util.rand_string()
        self.ctx.zato.response.data.headers[name] = actual
        self.assertTrue(common.then_header_doesnt_contain(self.ctx, name, util.rand_string()))

    def test_then_header_doesnt_contain_not_ok(self):
        name = util.rand_string()
        substring = util.rand_string()
        actual = util.rand_string() + util.rand_string()
        self.ctx.zato.response.data.headers[name] = actual
        self.assertRaises(AssertionError, common.then_header_contains, self.ctx, name, substring)

    def test_then_header_exists_ok(self):
        name = util.rand_string()
        actual = util.rand_string()
        self.ctx.zato.response.data.headers[name] = actual
        self.assertTrue(common.then_header_exists(self.ctx, name))

    def test_then_header_exists_not_ok(self):
        name = util.rand_string()
        actual = util.rand_string()
        self.ctx.zato.response.data.headers[name] = actual
        self.assertRaises(AssertionError, common.then_header_exists, self.ctx, util.rand_string())

    def test_then_header_doesnt_exist_ok(self):
        name = util.rand_string()
        actual = util.rand_string()
        self.ctx.zato.response.data.headers[name] = actual
        self.assertTrue(common.then_header_doesnt_exist(self.ctx, util.rand_string()))

    def test_then_header_doesnt_exist_not_ok(self):
        name = util.rand_string()
        actual = util.rand_string()
        self.ctx.zato.response.data.headers[name] = actual
        self.assertRaises(AssertionError, common.then_header_doesnt_exist, self.ctx, name)

    def test_then_header_is_empty_ok(self):
        name = util.rand_string()
        actual = ''
        self.ctx.zato.response.data.headers[name] = actual
        self.assertTrue(common.then_header_is_empty(self.ctx, name))

    def test_then_header_is_empty_not_ok(self):
        name = util.rand_string()
        actual = util.rand_string()
        self.ctx.zato.response.data.headers[name] = actual
        self.assertRaises(AssertionError, common.then_header_is_empty, self.ctx, name)

    def test_then_header_isnt_empty_ok(self):
        name = util.rand_string()
        actual = util.rand_string()
        self.ctx.zato.response.data.headers[name] = actual
        self.assertTrue(common.then_header_isnt_empty(self.ctx, name))

    def test_then_header_isnt_empty_not_ok(self):
        name = util.rand_string()
        util.rand_string()
        actual = ''
        self.ctx.zato.response.data.headers[name] = actual
        self.assertRaises(AssertionError, common.then_header_isnt_empty, self.ctx, name)

    def test_then_header_starts_with_ok(self):
        name, prefix = util.rand_string(2)
        actual = prefix + util.rand_string()
        self.ctx.zato.response.data.headers[name] = actual
        self.assertTrue(common.then_header_starts_with(self.ctx, name, prefix))

    def test_then_header_starts_with_not_ok(self):
        name, prefix = util.rand_string(2)
        actual = prefix + util.rand_string()
        self.ctx.zato.response.data.headers[name] = actual
        self.assertRaises(AssertionError, common.then_header_starts_with, self.ctx, name, util.rand_string())

    def test_then_header_doesnt_starts_with_ok(self):
        name, prefix = util.rand_string(2)
        actual = prefix + util.rand_string()
        self.ctx.zato.response.data.headers[name] = actual
        self.assertTrue(common.then_header_doesnt_starts_with(self.ctx, name, util.rand_string()))

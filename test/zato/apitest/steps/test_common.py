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

        data = {'a': {'b': 'cc'}}

        method = 'POST'
        address = 'http://{}.example.com'.format(util.rand_string())
        url_path = '/{}'.format(util.rand_string())
        qs = '?{}={}'.format(*util.rand_string(2))
        headers = {util.rand_string():util.rand_string(), util.rand_string():util.rand_string()}

        ctx = Bunch(zato=Bunch(request=Bunch()))

        ctx.zato.request.is_xml = False
        ctx.zato.request.is_json = True
        ctx.zato.request.data = data
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
        self.assertDictEqual(loads(sent_request['request']['data']), data)

class GivenTestCase(TestCase):

    def setUp(self):
        self.ctx = util.new_context(None, util.rand_string())

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

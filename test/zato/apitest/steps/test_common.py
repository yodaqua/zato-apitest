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
from zato.apitest.test import xml_c14nize, XMLEchoAdapter

class CommonTestCase(TestCase):
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

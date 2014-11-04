# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Filip Kłosowski <filip at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# Originally part of Zato - open-source ESB, SOA, REST, APIs and cloud integrations in Python
# https://zato.io

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
from httplib import BAD_REQUEST
from StringIO import StringIO
from unittest import TestCase

# Bunch
from bunch import Bunch

# mock
from mock import patch, MagicMock, Mock

# Zato
from zato.apitest import util
from zato.apitest.steps import zato_

# ###############################################################################################################################

class GivenTestCase(TestCase):
    def setUp(self):
        self.ctx = Bunch()
        self.ctx.zato = util.new_context(None, util.rand_string(), {})

        self.fake_service_code = util.rand_string()

        conn_name = util.rand_string()
        cluster_id = util.rand_int()
        url_path = util.rand_string()
        username = util.rand_string()
        password = util.rand_string()
        zato_.given_i_store_zato_info_under_conn_name(self.ctx, cluster_id, url_path, username, password, conn_name)
        self.stored = self.ctx.zato.user_ctx[conn_name]

    def test_given_i_store_zato_info_under_conn_name(self):
        conn_name = util.rand_string()
        cluster_id = util.rand_int()
        url_path = util.rand_string()
        username = util.rand_string()
        password = util.rand_string()
        zato_.given_i_store_zato_info_under_conn_name(self.ctx, cluster_id, url_path, username, password, conn_name)
        stored = self.ctx.zato.user_ctx[conn_name]

        for key in stored:
            self.assertEquals(stored[key], eval(key))

    def test_when_i_upload_a_zato_service_from_path_to_conn_details_fails(self):
        file_mock = MagicMock(spec=file)
        file_mock.__enter__.return_value = StringIO(self.fake_service_code)

        with patch('__builtin__.open', create=True) as mock_open:
            mock_open.return_value = file_mock
            with patch('requests.get') as mock_requests:
                mock_requests.return_value = mock_response = Mock()
                mock_response.status_code = BAD_REQUEST
                self.assertRaises(
                    AssertionError, zato_.when_i_upload_a_zato_service_from_path_to_conn_details,self.ctx, './abc', self.stored)

# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
from unittest import TestCase

# Bunch
from bunch import Bunch

# Zato
from zato.apitest import version
from zato.apitest.util import context, new_context, rand_string

class UtilTest(TestCase):

    def _test_new_context(self, ctx_zato, environment_dir):
        self.assertEquals(ctx_zato.environment_dir, environment_dir)
        self.assertDictEqual(ctx_zato.user_data, {})
        self.assertDictEqual(ctx_zato.date_formats, {'default':'YYYY-MM-DDTHH:mm:ss'})
        self.assertDictEqual(ctx_zato.request.headers, {'User-Agent':'zato.apitest/{} (+https://zato.io)'.format(version)})
        self.assertDictEqual(ctx_zato.request.ns_map, {})
        self.assertDictEqual(context, ctx_zato)

    def test_new_context_from_old_ctx(self):

        # Done twice to ensure that util's context actually is wiped out.
        for x in range(2):
            environment_dir = rand_string()
            old_ctx = Bunch()
            old_ctx.zato = Bunch(environment_dir=environment_dir)
            ctx = new_context(old_ctx, None)
            self._test_new_context(ctx, environment_dir)

    def test_new_context_from_environment_dir(self):

        # Same comment as in test_new_context_from_old_ctx.
        for x in range(2):
            environment_dir = rand_string()
            ctx = new_context(None, environment_dir)
            self._test_new_context(ctx, environment_dir)

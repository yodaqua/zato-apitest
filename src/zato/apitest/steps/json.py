# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# Behave
from behave import given, then

# JSON Pointers
from jsonpointer import set_pointer

# Zato
from .. import util

# ################################################################################################################################

@given('JSON Pointer "{path}" in request is "{value}"')
def given_json_pointer_in_request_is(ctx, path, value):
    set_pointer(ctx.zato.request.data_impl, path, value)

@given('JSON Pointer "{path}" in request is an integer "{value}"')
def given_json_pointer_in_request_is_an_integer(ctx, path, value):
    set_pointer(ctx.zato.request.data_impl, path, int(value))

@given('JSON Pointer "{path}" in request is a float "{value}"')
def given_json_pointer_in_request_is_a_float(ctx, path, value):
    set_pointer(ctx.zato.request.data_impl, path, float(value))

@given('JSON Pointer "{path}" in request is a list "{value}"')
def given_json_pointer_in_request_is_a_list(ctx, path, value):
    set_pointer(ctx.zato.request.data_impl, path, util.parse_list(value))

@given('JSON Pointer "{path}" in request is a random string')
def given_json_pointer_in_request_is_a_random_string(ctx, path):
    set_pointer(ctx.zato.request.data_impl, path, util.rand_string())

@given('JSON Pointer "{path}" in request is a random integer')
def given_json_pointer_in_request_is_a_random_integer(ctx, path):
    set_pointer(ctx.zato.request.data_impl, path, util.rand_int())

@given('JSON Pointer "{path}" in request is any of "{value}"')
def given_json_pointer_in_request_is_any_of(ctx, path, value):
    set_pointer(ctx.zato.request.data_impl, path, util.any_from_list(value))

# ################################################################################################################################

@then('JSON Pointer "{path}" is "{value}"')
def then_json_pointer_is(ctx, path, value):
    pass

@then('JSON Pointer "{path}" is an integer "{value}"')
def then_json_pointer_is_an_integer(ctx, path, value):
    pass

@then('JSON Pointer "{path}" is a float "{value}"')
def then_json_pointer_is_a_float(ctx, path, value):
    pass

@then('JSON Pointer "{path}" is a list "{value}"')
def then_json_pointer_is_a_list(ctx, path, value):
    pass

@then('JSON Pointer "{path}" is empty')
def then_json_pointer_is_empty(ctx, path, value):
    pass

@then('JSON Pointer "{path}" is not empty')
def then_json_pointer_is_not_empty(ctx, path, value):
    pass

@then('JSON Pointer "{path}" is one of "{value}"')
def then_json_pointer_is_one_of(ctx, path, value):
    pass

@then('JSON Pointer "{path}" is not one of "{value}"')
def then_json_pointer_is_not_one_of(ctx, path, value):
    pass

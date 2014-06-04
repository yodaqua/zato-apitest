# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# Behave
from behave import given, then

# datadiff
from datadiff.tools import assert_equals

# jsonpointer
from jsonpointer import resolve_pointer as get_pointer, set_pointer

# Zato
from .. import util
from .. import INVALID

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

@given('JSON Pointer "{path}" in request is a random float')
def given_json_pointer_in_request_is_a_random_integer(ctx, path):
    set_pointer(ctx.zato.request.data_impl, path, util.rand_float())

@given('JSON Pointer "{path}" in request is one of "{value}"')
def given_json_pointer_in_request_is_one_of(ctx, path, value):
    set_pointer(ctx.zato.request.data_impl, path, util.any_from_list(value))

# ################################################################################################################################

@given('JSON Pointer "{path}" in request is a random date "{format}"')
def given_json_pointer_is_rand_date(ctx, path, format):
    set_pointer(ctx.zato.request.data_impl, path, util.rand_date(ctx.zato.date_formats[format]))

@given('JSON Pointer "{path}" in request is now "{format}"')
def given_json_pointer_is_now(ctx, path, format):
    set_pointer(ctx.zato.request.data_impl, path, util.now(format=ctx.zato.date_formats[format]))

@given('JSON Pointer "{path}" in request is UTC now "{format}"')
def given_json_pointer_is_utc_now(ctx, path, format):
    set_pointer(ctx.zato.request.data_impl, path, util.utcnow(format=ctx.zato.date_formats[format]))

@given('JSON Pointer "{path}" in request is a random date after "{date_start}" "{format}"')
def given_json_pointer_is_rand_date_after(ctx, path, date_start, format):
    set_pointer(ctx.zato.request.data_impl, path, util.date_after(date_start, ctx.zato.date_formats[format]))

@given('JSON Pointer "{path}" in request is a random date before "{date_end}" "{format}"')
def given_json_pointer_is_rand_date_before(ctx, path, date_end, format):
    set_pointer(ctx.zato.request.data_impl, path, util.date_before(date_end, ctx.zato.date_formats[format]))

@given('JSON Pointer "{path}" in request is a random date between "{date_start}" and "{date_end}" "{format}"')
def given_json_pointer_is_rand_date_between(ctx, path, date_start, date_end, format):
    set_pointer(ctx.zato.request.data_impl, path, util.date_between(date_start, date_end, ctx.zato.date_formats[format]))

# ################################################################################################################################

def assert_value(ctx, path, value, wrapper=None):
    value = wrapper(value) if wrapper else value
    actual = get_pointer(ctx.zato.response.data_impl, path)
    assert_equals(value, actual)
    return True

@then('JSON Pointer "{path}" is "{value}"')
def then_json_pointer_is(ctx, path, value):
    return assert_value(ctx, path, value)

@then('JSON Pointer "{path}" is an integer "{value}"')
def then_json_pointer_is_an_integer(ctx, path, value):
    return assert_value(ctx, path, value, int)

@then('JSON Pointer "{path}" is a float "{value}"')
def then_json_pointer_is_a_float(ctx, path, value):
    return assert_value(ctx, path, value, float)

@then('JSON Pointer "{path}" is a list "{value}"')
def then_json_pointer_is_a_list(ctx, path, value):
    return assert_value(ctx, path, value, util.parse_list)

@then('JSON Pointer "{path}" is empty')
def then_json_pointer_is_empty(ctx, path):
    return assert_value(ctx, path, '')

@then('JSON Pointer "{path}" isn\'t empty')
def then_json_pointer_isnt_empty(ctx, path):
    actual = get_pointer(ctx.zato.response.data_impl, path, INVALID)
    assert actual != INVALID, 'Path `{}` Should not be empty'.format(path)

@then('JSON Pointer "{path}" is one of "{value}"')
def then_json_pointer_is_one_of(ctx, path, value):
    actual = get_pointer(ctx.zato.response.data_impl, path)
    value = util.parse_list(value)
    assert actual in value, 'Expected for `{}` ({}) to be in `{}`'.format(actual, path, value)

@then('JSON Pointer "{path}" isn\'t one of "{value}"')
def then_json_pointer_isnt_one_of(ctx, path, value):
    actual = get_pointer(ctx.zato.response.data_impl, path)
    value = util.parse_list(value)
    assert actual not in value, 'Expected for `{}` ({}) not to be in `{}`'.format(actual, path, value)

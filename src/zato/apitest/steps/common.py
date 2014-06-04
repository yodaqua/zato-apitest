# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
import json

# Behave
from behave import given, when, then

# Bunch
from bunch import Bunch

# datadiff
from datadiff.tools import assert_equals

# jsonpointer
from jsonpointer import resolve_pointer as get_pointer

# lxml
from lxml import etree

# Request
from requests import api as req_api

# Zato
from .. import util
from .. import INVALID, NO_VALUE

# ################################################################################################################################

@when('the URL is invoked')
def when_the_url_is_invoked(ctx, adapters=None):
    adapters = adapters or []
    method = ctx.zato.request.get('method', 'GET')
    address = ctx.zato.request.get('address')
    url_path = ctx.zato.request.get('url_path')
    qs = ctx.zato.request.get('query_string', '')

    if ctx.zato.request.is_xml:
        data = etree.tostring(ctx.zato.request.data_impl)
    elif ctx.zato.request.is_json:
        data = json.dumps(ctx.zato.request.data_impl, indent=2)

    ctx.zato.response = Bunch()

    s = req_api.sessions.Session()
    for adapter in adapters:
        s.mount('http://', adapter)
        s.mount('https://', adapter)

    ctx.zato.response.data = s.request(
        method, '{}{}{}'.format(address, url_path, qs), data=data, headers=ctx.zato.request.headers)

    if ctx.zato.request.is_xml:
        ctx.zato.response.data_impl = etree.fromstring(ctx.zato.response.data.text.encode('utf-8'))

    elif ctx.zato.request.is_json:
        ctx.zato.response.data_impl = json.loads(ctx.zato.response.data.text)

# ################################################################################################################################

@given('address "{address}"')
def given_address(ctx, address):
    ctx.zato.request.address = address

@given('URL path "{url_path}"')
def given_url_path(ctx, url_path):
    ctx.zato.request.url_path = url_path

@given('HTTP method "{method}"')
def given_http_method(ctx, method):
    ctx.zato.request.method = method

@given('format "{format}"')
def given_format(ctx, format):
    ctx.zato.request.format = format

@given('user agent is "{value}"')
def given_user_agent_is(ctx, value):
    ctx.zato.request.headers['User-Agent'] = value

@given('header "{header}" "{value}"')
def given_header(ctx, header, value):
    ctx.zato.request.headers[header] = value

def given_request_impl(ctx, data):

    ctx.zato.request.data = data

    ctx.zato.request.is_xml = ctx.zato.request.format == 'XML'
    ctx.zato.request.is_json = ctx.zato.request.format == 'JSON'

    if ctx.zato.request.is_xml:
        ctx.zato.request.data_impl = etree.fromstring(ctx.zato.request.data)
    else:
        ctx.zato.request.data_impl = json.loads(ctx.zato.request.data)

@given('request "{request_path}"')
def given_request(ctx, request_path):
    return given_request_impl(ctx, util.get_data(ctx, 'request', request_path))

@given('request is "{data}"')
def given_request_is(ctx, data):
    return given_request_impl(ctx, data)

@given('query string "{query_string}"')
def given_query_string(ctx, query_string):
    ctx.zato.request.query_string = query_string

@given('date format "{name}" "{format}"')
def given_date_format(ctx, name, format):
    ctx.zato.date_formats[name] = format

# ################################################################################################################################

@given('I store "{value}" under "{name}"')
def given_i_store_value_under_name(ctx, value, name):
    ctx.zato.user_data[name] = value

# ################################################################################################################################

@then('context is cleaned up')
def then_context_is_cleaned_up(ctx):
    ctx.zato = util.new_context(ctx, None)

@then('status is "{expected_status}"')
def then_status_is(ctx, expected_status):
    expected_status = int(expected_status)
    assert ctx.zato.response.data.status_code == expected_status, 'Status expected `{!r}`, received `{!r}`'.format(
        expected_status, ctx.zato.response.data.status_code)
    return True

@then('header "{expected_header}" is "{expected_value}"')
def then_header_is(ctx, expected_header, expected_value):
    value = ctx.zato.response.data.headers[expected_header]
    assert value == expected_value, 'Expected for header `{}` to be `{}` instead of `{}`'.format(
        expected_header, expected_value, value)
    return True

@then('header "{expected_header}" isn\'t "{expected_value}"')
def then_header_isnt(ctx, expected_header, expected_value):
    value = ctx.zato.response.data.headers[expected_header]
    assert expected_value != value, 'Expected for header `{}` not to be equal to `{}`'.format(
        expected_header, expected_value)
    return True

@then('header "{expected_header}" contains "{expected_value}"')
def then_header_contains(ctx, expected_header, expected_value):
    value = ctx.zato.response.data.headers[expected_header]
    assert expected_value in value, 'Expected for header `{}` to contain `{}` in `{}`'.format(
        expected_header, expected_value, value)
    return True

@then('header "{expected_header}" doesn\'t contain "{expected_value}"')
def then_header_doesnt_contain(ctx, expected_header, expected_value):
    value = ctx.zato.response.data.headers[expected_header]
    assert expected_value not in value, 'Header `{}` shouldn\'t contain `{}` in `{}`'.format(
        expected_header, expected_value, value)
    return True

@then('header "{expected_header}" exists')
def then_header_exists(ctx, expected_header):
    value = ctx.zato.response.data.headers.get(expected_header, INVALID)
    assert value != INVALID, 'Header `{}` should be among `{}`'.format(expected_header, ctx.zato.response.data.headers)
    return True

@then('header "{expected_header}" doesn\'t exist')
def then_header_doesnt_exist(ctx, expected_header):
    value = ctx.zato.response.data.headers.get(expected_header, INVALID)
    assert value == INVALID, 'Header `{}` shouldn\'t be among `{}`'.format(expected_header, ctx.zato.response.data.headers)
    return True

@then('header "{expected_header}" is empty')
def then_header_is_empty(ctx, expected_header):
    value = ctx.zato.response.data.headers[expected_header]
    assert value == '', 'Header `{}` should be empty instead of `{}`'.format(expected_header, value)
    return True

@then('header "{expected_header}" isn\'t empty')
def then_header_isnt_empty(ctx, expected_header):
    value = ctx.zato.response.data.headers[expected_header]
    assert value != '', 'Header `{}` shouldn\'t be empty'.format(expected_header)
    return True

@then('header "{expected_header}" starts with')
def then_header_starts_with(ctx, expected_header, expected_value):
    value = ctx.zato.response.data.headers[expected_header]
    assert value.startswith(expected_value), 'Expected for header `{}` to start with `{}` but it\'s `{}`'.format(
        expected_header, expected_value, value)
    return True

@then('header "{expected_header}" doesn\'t start with')
def then_header_doesnt_starts_with(ctx, expected_header, expected_value):
    value = ctx.zato.response.data.headers[expected_header]
    assert not value.startswith(expected_value), 'Expected for header `{}` not to start with `{}` yet it\'s `{}`'.format(
        expected_header, expected_value, value)
    return True

@then('header "{expected_header}" ends with')
def then_header_ends_with(ctx, expected_header, expected_value):
    value = ctx.zato.response.data.headers[expected_header]
    assert value.endswith(expected_value), 'Expected for header `{}` to end with `{}` but it\'s `{}`'.format(
        expected_header, expected_value, value)
    return True

@then('header "{expected_header}" doesn\'t end with')
def then_header_doesnt_end_with(ctx, expected_header, expected_value):
    value = ctx.zato.response.data.headers[expected_header]
    assert not value.endswith(expected_value), 'Expected for header `{}` not to end with `{}` yet it\'s `{}`'.format(
        expected_header, expected_value, value)
    return True

# ################################################################################################################################

@then('I store "{path}" from response under "{name}", default "{default}"')
def then_store_path_under_name_with_default(ctx, path, name, default):
    if ctx.zato.request.is_xml:
        value = 1
    else:
        value = get_pointer(ctx.zato.response.data_impl, path)
        ctx.zato.user_data[name] = value

@then('I store "{path}" from response under "{name}"')
def then_store_path_under_name(ctx, path, name):
    return then_store_path_under_name_with_default(ctx, path, name, NO_VALUE)

# ################################################################################################################################

def needs_json(func):
    def inner(ctx, **kwargs):
        if not ctx.zato.request.format == 'JSON':
            raise TypeError('This step works with JSON only.')
        return func(ctx, **kwargs)
    return inner

def json_response_is_equal_to(ctx, expected):
    assert_equals(expected, ctx.zato.response.data_impl)
    return True

@then('response is equal to "{expected}"')
@needs_json
def then_response_is_equal_to(ctx, expected):
    return json_response_is_equal_to(ctx, json.loads(expected))

@then('response is equal to that from "{path}"')
@needs_json
def then_response_is_equal_to_that_from(ctx, path):
    return json_response_is_equal_to(ctx, json.loads(util.get_data(ctx, 'response', path)))

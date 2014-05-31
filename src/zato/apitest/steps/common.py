# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
import json, uuid

# Behave
from behave import given, when, then

# Bunch
from bunch import Bunch

# lxml
from lxml import etree

# Request
from requests import api as req_api

# Zato
from .. import util

# TODO TODO

# TODO TODO

# And user agent is

# TODO TODO

INVALID = 'invalid-{}'.format(uuid.uuid4().hex)

# ################################################################################################################################

@when('the URL is invoked')
def when_the_url_is_invoked(ctx):
    method = ctx.zato.request.get('method', 'GET')
    address = ctx.zato.request.get('address')
    url_path = ctx.zato.request.get('url_path')
    qs = ctx.zato.request.get('query_string', '')
    format = ctx.zato.request.get('format', 'JSON')

    if ctx.zato.request.is_xml:
        data = etree.tostring(ctx.zato.request.data_impl, pretty_print=True)
    elif ctx.zato.request.is_json:
        data = json.dumps(ctx.zato.request.data, indent=2)

    ctx.zato.response = Bunch()
    ctx.zato.response.data = req_api.request(
        method, '{}{}{}'.format(address, url_path, qs), data=data, headers=ctx.zato.request.headers)

    if ctx.zato.request.is_xml:
        ctx.zato.response.data_impl = etree.fromstring(ctx.zato.response.data.text.encode('utf-8'))
    elif ctx.zato.request.is_json:
        ctx.zato.response.data_impl = json.loads(ctx.zato.response.data.text)

# ################################################################################################################################

@given('address "{address}"')
def given_address(ctx, address):
    #raise Exception(ctx.zato)
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
def given_format(ctx, format):
    ctx.zato.request.headers['User-Agent'] = value

@given('header "{header}" "{value}"')
def given_header(ctx, header, value):
    ctx.zato.request.headers[header] = value

@given('SOAP action "{value}"')
def given_soap_action(ctx, value):
    ctx.zato.request.headers['SOAPAction'] = value

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
    full_path = util.get_full_path(ctx.zato.environment_dir, ctx.zato.request.format.lower(), 'request', request_path)
    data = util.get_file(full_path) if request_path else ''

    if ctx.zato.request.format == 'XML' and not data:
        raise ValueError('No request in `{}`'.format(full_path))

    return given_request_impl(ctx, data)

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

@then('context is cleaned up')
def then_context_is_cleaned_up(ctx):
    ctx.zato = util.new_context(ctx, None)

@then('status is "{expected_status}"')
def then_status_is(ctx, expected_status):
    expected_status = int(expected_status)
    assert ctx.zato.response.data.status_code == expected_status, 'Status expected `{!r}`, received `{!r}`'.format(
        expected_status, ctx.zato.response.data.status_code)

@then('header "{expected_header}" is "{expected_value}"')
def then_header_is(ctx, expected_header, expected_value):
    value = ctx.zato.response.data.headers[expected_header]
    assert value == expected_value, 'Expected for header `{}` to be `{}` instead of `{}`'.format(
        expected_header, expected_value, value)

@then('header "{expected_header}" isn\'t "{expected_value}"')
def then_header_isnt(ctx, expected_header, expected_value):
    value = ctx.zato.response.data.headers[expected_header]
    assert expected_value != value, 'Expected for header `{}` not to be equal to `{}`'.format(
        expected_header, expected_value)

@then('header "{expected_header}" contains "{expected_value}"')
def then_header_contains(ctx, expected_header, expected_value):
    value = ctx.zato.response.data.headers[expected_header]
    assert expected_value in value, 'Expected for header `{}` to contain `{}` in `{}`'.format(
        expected_header, expected_value, value)

@then('header "{expected_header}" doesn\'t contain "{expected_value}"')
def then_header_doesnt_contain(ctx, expected_header, expected_value):
    value = ctx.zato.response.data.headers[expected_header]
    assert expected_value not in value, 'Header `{}` shouldn\'t contain `{}` in `{}`'.format(
        expected_header, expected_value, value)

@then('header "{expected_header}" exists')
def then_header_doesnt_contain(ctx, expected_header):
    value = ctx.zato.response.data.headers.get(expected_header, INVALID)
    assert value != INVALID, 'Header `{}` should be among `{}`'.format(expected_header, ctx.zato.response.headers)

@then('header "{expected_header}" doesn\'t exist')
def then_header_doesnt_contain(ctx, expected_header):
    value = ctx.zato.response.data.headers.get(expected_header, INVALID)
    assert value == INVALID, 'Header `{}` shouldn\'t be among `{}`'.format(expected_header, ctx.zato.response.headers)

@then('header "{expected_header}" is empty')
def then_header_is_empty(ctx, expected_header):
    value = ctx.zato.response.data.headers[expected_header]
    assert value == '', 'Header `{}` should be empty instead of `{}`'.format(expected_header, value)

@then('header "{expected_header}" isn\'t empty')
def then_header_isnt_empty(ctx, expected_header):
    value = ctx.zato.response.data.headers[expected_header]
    assert value != '', 'Header `{}` shouldn\'t be empty'.format(expected_header)

@then('header "{expected_header}" starts with')
def then_header_starts_with(ctx, expected_header, expected_value):
    value = ctx.zato.response.data.headers[expected_header]
    assert value.startswith(expected_value), 'Expected for header `{}` to start with `{}` but it\'s `{}`'.format(
        expected_header, expected_value, value)

@then('header "{expected_header}" doesn\'t start with')
def then_header_doesnt_starts_with(ctx, expected_header, expected_value):
    value = ctx.zato.response.data.headers[expected_header]
    assert not value.startswith(expected_value), 'Expected for header `{}` not to start with `{}` yet it\'s `{}`'.format(
        expected_header, expected_value, value)

@then('header "{expected_header}" ends with')
def then_header_ends_with(ctx, expected_header, expected_value):
    value = ctx.zato.response.data.headers[expected_header]
    assert value.endswith(expected_value), 'Expected for header `{}` to end with `{}` but it\'s `{}`'.format(
        expected_header, expected_value, value)

@then('header "{expected_header}" doesn\'t end with')
def then_header_ends_with(ctx, expected_header, expected_value):
    value = ctx.zato.response.data.headers[expected_header]
    assert not value.endswith(expected_value), 'Expected for header `{}` not to end with `{}` yet it\'s `{}`'.format(
        expected_header, expected_value, value)

@then('header "{expected_header}" has "{expected_value}" at {idx_start}:{idx_end}')
def then_header_has_at(ctx, expected_header, expected_value, idx_start, idx_end):
    pass

# ################################################################################################################################

@then('response is equal to "{response}"')
def then_response_is_equal_to(ctx, response):
    pass

@then('response is equal to that from "{path}"')
def then_response_is_equal_to_that_from(ctx, path):
    pass
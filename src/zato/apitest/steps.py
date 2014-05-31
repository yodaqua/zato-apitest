# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
import csv, json, os, uuid
from random import choice

# Behave
from behave import given, when, then

# Bunch
from bunch import Bunch

# lxml
from lxml import etree

# Requests
from requests import api

# six
import six
from six.moves import cStringIO as StringIO

# Zato
from . import util

mod_dir = os.path.dirname(os.path.realpath(__file__))

INVALID = 'invalid-{}'.format(uuid.uuid4().hex)

# TODO TODO

# TODO TODO

# And user agent is

# TODO TODO

# ################################################################################################################################

def get_full_path(base_dir, *path_items):
    return os.path.normpath(os.path.join(base_dir, *path_items))

def get_file(path):
    return open(path).read()

# ################################################################################################################################

@when('the URL is invoked')
def when_the_url_is_invoked(ctx):
    method = ctx.zato.request.get('method', 'GET')
    address = ctx.zato.request.get('address')
    url_path = ctx.zato.request.get('url_path')
    qs = ctx.zato.request.get('query_string', '')
    format = ctx.zato.request.get('format', 'JSON')

    if ctx.zato.request.is_xml:
        data = etree.tostring(ctx.zato.request.data_xml, pretty_print=True)
    elif ctx.zato.request.is_json:
        data = json.dumps(ctx.zato.request.data, indent=2)

    ctx.zato.response = Bunch()
    ctx.zato.response.data = api.request(
        method, '{}{}{}'.format(address, url_path, qs), data=data, headers=ctx.zato.request.headers)

    if ctx.zato.request.is_xml:
        ctx.zato.response.data_xml = etree.fromstring(ctx.zato.response.data.text.encode('utf-8'))
    elif ctx.zato.request.is_json:
        ctx.zato.response.data_json = json.loads(ctx.zato.response.data.text)

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

@given('header "{header}" "{value}"')
def given_header(ctx, header, value):
    ctx.zato.request.headers[header] = value

@given('SOAP action "{value}"')
def given_soap_action(ctx, value):
    ctx.zato.request.headers['SOAPAction'] = value

@given('request "{request_path}"')
def given_request(ctx, request_path):
    ctx.zato.request.request_path = request_path
    full_path = get_full_path(ctx.zato.environment_dir, ctx.zato.request.format.lower(), 'request', request_path)
    ctx.zato.request.data = get_file(full_path) if request_path else ''

    ctx.zato.request.is_xml = ctx.zato.request.format == 'XML'
    ctx.zato.request.is_json = ctx.zato.request.format == 'JSON'

    if ctx.zato.request.is_xml:
        if ctx.zato.request.data:
            ctx.zato.request.data_xml = etree.fromstring(ctx.zato.request.data)
        else:
            raise ValueError('No request in `{}`'.format(full_path))

@given('query string "{query_string}"')
def given_query_string(ctx, query_string):
    ctx.zato.request.query_string = query_string

# ################################################################################################################################

def handle_xpath(is_request):
    def handle_xpath_impl(func, **ignored):
        def inner(ctx, **kwargs):
            xpath = kwargs.pop('xpath', kwargs.pop('elem', None))

            data = ctx.zato.request.data if is_request else ctx.zato.response.data.text
            data_xml = ctx.zato.request.data_xml if is_request else ctx.zato.response.data_xml

            elem = data_xml.xpath(xpath, namespaces=ctx.zato.request.ns_map)
            if not elem:
                raise ValueError('No `{}` path in `{}`'.format(xpath, data))

            if len(elem) > 1:
                raise ValueError('Path `{}` points to more than one element in `{}`'.format(xpath, data))

            elem = elem[0]
            if 'value' in kwargs:
                kwargs['value'] = kwargs['value'].encode('utf-8')

            return func(ctx, elem, **kwargs)
        return inner
    return handle_xpath_impl

@given('XPath "{xpath}" in request is set to "{value}"')
@handle_xpath(True)
def given_xpath_set_to_rand_string(ctx, elem, value, **ignored):
    elem.text = value

@given('XPath "{xpath}" in request is set to a random string')
@handle_xpath(True)
def given_xpath_set_to_rand_string(ctx, elem, **ignored):
    elem.text = util.rand_string()

@given('XPath "{xpath}" in request is set to a random integer')
@handle_xpath(True)
def given_xpath_set_to_rand_int(ctx, elem, **ignored):
    elem.text = str(util.rand_int())

@given('XPath "{xpath}" in request is set to a random float')
@handle_xpath(True)
def given_xpath_set_to_rand_float(ctx, elem, **ignored):
    elem.text = str(util.rand_float())

@given('XPath "{xpath}" in request is set to a random date')
@handle_xpath(True)
def given_xpath_set_to_rand_date(ctx, elem, **ignored):
    pass

@given('XPath "{xpath}" in request is set to a random date after {date_start}')
@handle_xpath(True)
def given_xpath_set_to_rand_date_after(ctx, elem, date_start, **ignored):
    pass

@given('XPath "{xpath}" in request is set to a random date before {date_end}')
@handle_xpath(True)
def given_xpath_set_to_rand_date_before(ctx, elem, date_end, **ignored):
    pass

@given('XPath "{xpath}" in request is set to a random date between {date_start} and {date_end}')
@handle_xpath(True)
def given_xpath_set_to_rand_date_between(ctx, elem, date_start, date_end, **ignored):
    pass

@given('XPath "{xpath}" in request is set to one of "{value}"')
@handle_xpath(True)
def given_xpath_set_to_one_of(ctx, elem, value, **ignored):
    elems = tuple(csv.reader(StringIO(value)))[0]
    elem.text = choice(tuple(elem.strip() for elem in elems if elem)).decode('utf-8')

# ################################################################################################################################

@given('namespace prefix "{prefix}" of "{namespace}"')
def given_namespace_prefix(ctx, prefix, namespace):
    ctx.zato.request.ns_map[prefix] = namespace

def _assert_xpath_value(ctx, elem, force_type=None, **kwargs):
    elem_text = elem.text
    value = expected_value = kwargs['value']

    if force_type:
        elem_text = force_type(elem_text)
        value = force_type(value)

    assert elem_text == value, '`{!r}` is `{!r}` instead of `{!r}` in `{!r}`'.format(
        elem, value, expected_value, etree.tostring(elem))

@then('XPath "{elem}" is "{value}"')
@handle_xpath(False)
def then_xpath_is(ctx, elem, **kwargs):
    return _assert_xpath_value(ctx, elem, force_type=None, **kwargs)

@then('XPath "{elem}" is an integer "{value}"')
@handle_xpath(False)
def then_xpath_is_an_integer(ctx, elem, **kwargs):
    return _assert_xpath_value(ctx, elem, force_type=int, **kwargs)

# ################################################################################################################################

@then('JSON Pointer "{xpath}" is "{expected_value}"')
def then_json_pointer_is(ctx, xpath, value):
    pass

@then('JSON Pointer "{xpath}" is an integer "{expected_value}"')
def then_json_pointer_is_an_integer(ctx, xpath, value):
    pass

@then('JSON Pointer "{xpath}" is a list "{expected_value}"')
def then_json_pointer_is_a_list(ctx, xpath, value):
    pass

# ################################################################################################################################

@then('response is equal to "{response}"')
def then_response_is_equal_to(ctx, response):
    pass

@then('response is equal to that from "{path}"')
def then_response_is_equal_to_that_from(ctx, path):
    pass

# ################################################################################################################################

@then('status is "{expected_status}"')
def then_status_is(ctx, expected_status):
    expected_status = int(expected_status)
    assert ctx.zato.response.status_code == expected_status, 'Status expected `{!r}`, received `{!r}`'.format(
        expected_status, ctx.zato.response.status_code)

@then('header "{expected_header}" is "{expected_value}"')
def then_header_is(ctx, expected_header, expected_value):
    value = ctx.zato.response.headers[expected_header]
    assert value == expected_value, 'Expected for header `{}` to be `{}` instead of `{}`'.format(
        expected_header, expected_value, value)

@then('header "{expected_header}" isn\'t "{expected_value}"')
def then_header_isnt(ctx, expected_header, expected_value):
    value = ctx.zato.response.headers[expected_header]
    assert expected_value != value, 'Expected for header `{}` not to be equal to `{}`'.format(
        expected_header, expected_value)

@then('header "{expected_header}" contains "{expected_value}"')
def then_header_contains(ctx, expected_header, expected_value):
    value = ctx.zato.response.headers[expected_header]
    assert expected_value in value, 'Expected for header `{}` to contain `{}` in `{}`'.format(
        expected_header, expected_value, value)

@then('header "{expected_header}" doesn\'t contain "{expected_value}"')
def then_header_doesnt_contain(ctx, expected_header, expected_value):
    value = ctx.zato.response.headers[expected_header]
    assert expected_value not in value, 'Header `{}` shouldn\'t contain `{}` in `{}`'.format(
        expected_header, expected_value, value)

@then('header "{expected_header}" exists')
def then_header_doesnt_contain(ctx, expected_header):
    value = ctx.zato.response.headers.get(expected_header, INVALID)
    assert value != INVALID, 'Header `{}` should be among `{}`'.format(expected_header, ctx.zato.response.headers)

@then('header "{expected_header}" doesn\'t exist')
def then_header_doesnt_contain(ctx, expected_header):
    value = ctx.zato.response.headers.get(expected_header, INVALID)
    assert value == INVALID, 'Header `{}` shouldn\'t be among `{}`'.format(expected_header, ctx.zato.response.headers)

@then('header "{expected_header}" is empty')
def then_header_is_empty(ctx, expected_header):
    value = ctx.zato.response.headers[expected_header]
    assert value == '', 'Header `{}` should be empty instead of `{}`'.format(expected_header, value)

@then('header "{expected_header}" isn\'t empty')
def then_header_isnt_empty(ctx, expected_header):
    value = ctx.zato.response.headers[expected_header]
    assert value != '', 'Header `{}` shouldn\'t be empty'.format(expected_header)

@then('header "{expected_header}" starts with')
def then_header_starts_with(ctx, expected_header, expected_value):
    value = ctx.zato.response.headers[expected_header]
    assert value.startswith(expected_value), 'Expected for header `{}` to start with `{}` but it\'s `{}`'.format(
        expected_header, expected_value, value)

@then('header "{expected_header}" doesn\'t start with')
def then_header_doesnt_starts_with(ctx, expected_header, expected_value):
    value = ctx.zato.response.headers[expected_header]
    assert not value.startswith(expected_value), 'Expected for header `{}` not to start with `{}` yet it\'s `{}`'.format(
        expected_header, expected_value, value)

@then('header "{expected_header}" ends with')
def then_header_ends_with(ctx, expected_header, expected_value):
    value = ctx.zato.response.headers[expected_header]
    assert value.endswith(expected_value), 'Expected for header `{}` to end with `{}` but it\'s `{}`'.format(
        expected_header, expected_value, value)

@then('header "{expected_header}" doesn\'t end with')
def then_header_ends_with(ctx, expected_header, expected_value):
    value = ctx.zato.response.headers[expected_header]
    assert not value.endswith(expected_value), 'Expected for header `{}` not to end with `{}` yet it\'s `{}`'.format(
        expected_header, expected_value, value)

@then('header "{expected_header}" has "{expected_value}" at {idx_start}:{idx_end}')
def then_header_has_at(ctx, expected_header, expected_value, idx_start, idx_end):
    pass
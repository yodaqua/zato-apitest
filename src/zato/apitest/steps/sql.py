# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Filip Kłosowski <filip at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# Originally part of Zato - open-source ESB, SOA, REST, APIs and cloud integrations in Python
# https://zato.io

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
import ast
from itertools import izip_longest

# Behave
from behave import given, then

# sqlalchemy
from sqlalchemy import create_engine

# Zato
from .. import util

# ################################################################################################################################

@given('I connect to "{sqlalchemy_url}" as "{conn_name}"')
@util.obtain_values
def given_i_connect_to_sqlalchemy_url_as_conn_name(ctx, sqlalchemy_url, conn_name):
    engine = create_engine(sqlalchemy_url)
    connection = engine.connect()
    ctx.zato.user_ctx[conn_name] = connection

@then('SQL "{sql}" is equal to "{value}", using "{conn_name}"')
@util.obtain_values
def then_sql_is_equal_to_value_using_conn_name(ctx, sql, value, conn_name):
    conn = conn_name.execute(sql)
    actual = conn.fetchall()
    expected_value = ast.literal_eval(value)
    assert actual == expected_value, 'Value `{}` is not equal to expected `{}`'.format(actual, expected_value)

@then('I disconnect from SQL "{conn_name}"')
@util.obtain_values
def then_i_disconnect_from_sql(ctx, conn_name):
    conn_name.close()

@given('I store SQL "{sql}" under "{name}", using "{conn_name}"')
@util.obtain_values
def given_i_store_sql_under_name(ctx, sql, name, conn_name):
    conn = conn_name.execute(sql)
    result = conn.fetchall()
    if len(result) == 1:
        ctx.zato.user_ctx[name] = result[0][0]
    else:
        ctx.zato.user_ctx[name] = result

# ###############################################################################################################################
def variable_is(variable, value):
    expected_value = ast.literal_eval(value)
    assert variable == expected_value, 'Value `{}` is not equal to expected `{}`'.format(variable, expected_value)

@then('variable "{variable}" is a list "{value}"')
@util.obtain_values
def and_variable_is_a_list(ctx, variable, value):
    variable_is(variable, value)

@then('variable "{variable}" is an empty list')
@util.obtain_values
def and_variable_is_an_empty_list(ctx, variable):
    assert variable == [], 'Value `{}` is not an empty list'.format(variable)

@then('variable "{variable}" is an integer "{value}"')
@util.obtain_values
def and_variable_is_an_integer(ctx, variable, value):
    variable_is(variable, value)

@then('variable "{variable}" is a float "{value}"')
@util.obtain_values
def and_variable_is_a_float(ctx, variable, value):
    variable_is(variable, value)

@then('variable "{variable}" is a string "{value}"')
@util.obtain_values
def and_variable_is_a_string(ctx, variable, value):
    assert variable == value, 'Value `{}` is not equal to expected `{}`'.format(variable, value)

@then('variable "{variable}" is True')
@util.obtain_values
def and_variable_is_true(ctx, variable):
    variable_is(variable, 'True')

@then('variable "{variable}" is False')
@util.obtain_values
def and_variable_is_false(ctx, variable):
    variable_is(variable, 'False')

# ###############################################################################################################################
def wrap_into_quotes(values):
    return '\'{}\''.format('\', \''.join(values.split(', ')))

def make_dict(*args):
    components = []
    phrases = {}
    for item in args:
        components.append([segment for segment in item.split(', ')])
    for items in izip_longest(*components):
        phrases[items[0]] = items[1:]
    return phrases

def build_filter(*args):
    comparison_operators = {'equal to': '=', 'not equal to': '!=', 'less than': '<', 'more than': '>', 'less or equal to': '<=', 'more or equal to': '>='}
    filter_dict = make_dict(*args)
    filter_ = ''
    for i, key in enumerate(filter_dict.keys()):
        operator = comparison_operators[filter_dict[key][0]]
        if i == 0:
            filter_ += "WHERE %s%s'%s' " % (key, operator, filter_dict[key][1])
        else:
            filter_ += "%s %s%s'%s' " % (filter_dict[key][2], key, operator, filter_dict[key][1])
    return filter_

@then('I insert "{values}" into following columns "{columns}" of "{tablename}", using "{conn_name}"')
@util.obtain_values
def then_i_insert_values_into_columns(ctx, tablename, values, columns, conn_name):
    insert = "INSERT INTO %s (%s) VALUES (%s)" % (tablename, columns, wrap_into_quotes(values))
    conn_name.execute(insert)
    return insert

@given('I store filter "{colname}" is "{sign}" "{colvalue}" "{operator}" under "{name}"')
def i_store_filter_under_name(ctx, colname, sign, colvalue, name, operator=None):
    criterion = build_filter(colname, sign, colvalue, operator)
    ctx.zato.user_ctx[name] = criterion

@then('I update "{columns}" of "{tablename}" set "{values}" filter by "{criterion}", using "{conn_name}"')
@util.obtain_values
def then_i_update_columns_setting_values(ctx, tablename, columns, values, conn_name, criterion=None):
    if not criterion:
        criterion = ''
    column_value = make_dict(columns, values)
    conn_name.execute('BEGIN TRANSACTION')
    for key in column_value.keys():
        insert = "UPDATE %s SET %s='%s' %s" %(tablename, key, column_value[key][0], criterion)
        conn_name.execute(insert)
    conn_name.execute('COMMIT')
    return insert

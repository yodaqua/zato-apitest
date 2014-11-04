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

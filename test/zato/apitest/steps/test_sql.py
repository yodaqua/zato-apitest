# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Filip Kłosowski <filip at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# Originally part of Zato - open-source ESB, SOA, REST, APIs and cloud integrations in Python
# https://zato.io

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
import os
from tempfile import NamedTemporaryFile
from unittest import TestCase

# Bunch
from bunch import Bunch

# sqlite3
import sqlite3
from sqlalchemy.engine.base import Connection

# Zato
from zato.apitest import util
from zato.apitest.steps import sql

# ###############################################################################################################################

class GivenTestCase(TestCase):
    def setUp(self):
        self.ctx = Bunch()
        self.ctx.zato = util.new_context(None, util.rand_string(), {})

        self.id = util.rand_int()
        self.name = util.rand_string()
        self.value = util.rand_string()
        self.temp_db = NamedTemporaryFile().name

        self.conn = sqlite3.connect(self.temp_db)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE TestDB (id integer, name text, value text)")
        self.cursor.execute("INSERT INTO TestDB (id, name, value) VALUES (?,?,?)", (self.id, self.name, self.value))
        self.conn.commit()

        self.sqlalchemy_url = 'sqlite:///' + self.temp_db
        general_conn_name = 'general_connn_name'
        sql.given_i_connect_to_sqlalchemy_url_as_conn_name(self.ctx, self.sqlalchemy_url, general_conn_name)
        self.general_conn = self.ctx.zato.user_ctx[general_conn_name]

    def test_given_i_connect_to_sqlalchemy_url_as_conn_name(self):
        current_conn_name = util.rand_string()
        sql.given_i_connect_to_sqlalchemy_url_as_conn_name(self.ctx, self.sqlalchemy_url, current_conn_name)
        current_conn = self.ctx.zato.user_ctx[current_conn_name]
        self.assertIsInstance(current_conn, Connection)
        sql.then_i_disconnect_from_sql(self.ctx, current_conn)

    def test_then_sql_is_equal_to_value_using_conn_name(self):
        q = 'SELECT name FROM TestDb'
        compare_to = str(util.rand_string(2))
        self.assertRaises(
            AssertionError, sql.then_sql_is_equal_to_value_using_conn_name,self.ctx, q, compare_to, self.general_conn
            )

    def test_given_i_store_sql_under_name_single_elem_list(self):
        q = 'SELECT name FROM TestDb'
        sql.given_i_store_sql_under_name(self.ctx, q, 'sql_result_single', self.general_conn)
        self.assertEquals(self.ctx.zato.user_ctx['sql_result_single'], self.name)

    def test_given_i_store_sql_under_name_multi_elem_list(self):
        id = util.rand_int()
        name = util.rand_string()
        value = util.rand_string()
        self.cursor.execute("INSERT INTO TestDB (id, name, value) VALUES (?,?,?)", (id, name, value))
        self.conn.commit()
        q = 'SELECT name FROM TestDb'
        sql.given_i_store_sql_under_name(self.ctx, q, 'sql_result_multi', self.general_conn)
        self.assertEquals(self.ctx.zato.user_ctx['sql_result_multi'], [(self.name,), (name,)])

    def test_variable_is(self):
        variable = str(util.rand_string(2))
        value = str(util.rand_string(2))
        self.assertRaises(AssertionError, sql.variable_is, variable, value)
        
    def test_and_variable_is_a_list(self):
        variable = str([util.rand_string(2)])
        value = str([util.rand_string(2)])
        self.assertRaises(AssertionError, sql.and_variable_is_a_list, self.ctx, variable, value)

    def test_and_variable_is_a_emptyn_list(self):
        variable = str([util.rand_string(2)])
        self.assertRaises(AssertionError, sql.and_variable_is_an_empty_list, self.ctx, variable)

    def test_and_variable_is_an_integer(self):
        variable = str(1)
        value = str([util.rand_string(2)])
        self.assertRaises(AssertionError, sql.and_variable_is_an_integer, self.ctx, variable, value)
        
    def test_and_variable_is_a_float(self):
        variable = str(1)
        value = str([util.rand_string(2)])
        self.assertRaises(AssertionError, sql.and_variable_is_a_float, self.ctx, variable, value)

    def test_and_variable_is_a_string(self):
        variable = str(1)
        value = str([util.rand_string(2)])
        self.assertRaises(AssertionError, sql.and_variable_is_a_string, self.ctx, variable, value)

    def test_and_variable_is_true(self):
        variable = "False"
        self.assertRaises(AssertionError, sql.and_variable_is_true, self.ctx, variable)

    def test_and_variable_is_false(self):
        variable = "True"
        self.assertRaises(AssertionError, sql.and_variable_is_false, self.ctx, variable)

    def tearDown(self):
        self.conn.close()
        os.remove(self.temp_db)
        sql.then_i_disconnect_from_sql(self.ctx, self.general_conn)

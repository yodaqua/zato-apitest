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
import random
from tempfile import NamedTemporaryFile
from StringIO import StringIO
from unittest import TestCase

# Bunch
from bunch import Bunch

# mock
from mock import patch

# SQLAlchemy
from sqlalchemy.engine.base import Connection

# sqlite3
import sqlite3

# Zato
from zato.apitest import util
from zato.apitest.steps import common, sql

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

    def comma_delimited_string(self, n):
            return ', '.join(util.rand_string(n))

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
            AssertionError, sql.then_sql_is_equal_to_value_using_conn_name, self.ctx, q, compare_to, self.general_conn
            )

    def test_given_i_store_sql_query_result_under_name_single_elem_list(self):
        q = 'SELECT name FROM TestDb'
        sql.given_i_store_sql_query_result_under_name(self.ctx, q, 'sql_result_single', self.general_conn)
        self.assertEquals(self.ctx.zato.user_ctx['sql_result_single'], self.name)

    def test_given_i_store_sql_query_result_under_name_multi_elem_list(self):
        id = util.rand_int()
        name = util.rand_string()
        value = util.rand_string()
        self.cursor.execute("INSERT INTO TestDB (id, name, value) VALUES (?,?,?)", (id, name, value))
        self.conn.commit()
        q = 'SELECT name FROM TestDb'
        sql.given_i_store_sql_query_result_under_name(self.ctx, q, 'sql_result_multi', self.general_conn)
        self.assertEquals(self.ctx.zato.user_ctx['sql_result_multi'], [(self.name,), (name,)])

    def test_variable_is(self):
        variable = str(util.rand_string(2))
        value = str(util.rand_string(2))
        self.assertRaises(AssertionError, common.variable_is, variable, value)

    def test_and_variable_is_a_list(self):
        variable = str([util.rand_string(2)])
        value = str([util.rand_string(2)])
        self.assertRaises(AssertionError, common.and_variable_is_a_list, self.ctx, variable, value)

    def test_and_variable_is_a_emptyn_list(self):
        variable = str([util.rand_string(2)])
        self.assertRaises(AssertionError, common.and_variable_is_an_empty_list, self.ctx, variable)

    def test_and_variable_is_an_integer(self):
        variable = str(1)
        value = str([util.rand_string(2)])
        self.assertRaises(AssertionError, common.and_variable_is_an_integer, self.ctx, variable, value)

    def test_and_variable_is_a_float(self):
        variable = str(1)
        value = str([util.rand_string(2)])
        self.assertRaises(AssertionError, common.and_variable_is_a_float, self.ctx, variable, value)

    def test_and_variable_is_a_string(self):
        variable = str(1)
        value = str([util.rand_string(2)])
        self.assertRaises(AssertionError, common.and_variable_is_a_string, self.ctx, variable, value)

    def test_and_variable_is_true(self):
        variable = "False"
        self.assertRaises(AssertionError, common.and_variable_is_true, self.ctx, variable)

    def test_and_variable_is_false(self):
        variable = "True"
        self.assertRaises(AssertionError, common.and_variable_is_false, self.ctx, variable)

    def test_wrap_into_quotes(self):
        value = util.rand_string()
        self.assertTrue(util.wrap_into_quotes(value).startswith('\''))
        self.assertTrue(util.wrap_into_quotes(value).endswith('\''))

    def test_mak_edict(self):
        n = random.randint(2,9)
        self.assertTrue(isinstance(util.make_dict(self.comma_delimited_string(n), self.comma_delimited_string(n)), dict))
        self.assertTrue(len(util.make_dict(self.comma_delimited_string(n), self.comma_delimited_string(n))) == n)

    def test_i_store_filter_under_name(self):
        colname = self.comma_delimited_string(2)
        signs = getattr(util, 'comparison_operators')
        sign = [random.choice(signs.keys()), random.choice(signs.keys())]
        colvalue = self.comma_delimited_string(2)
        name = 'filter'
        operator = 'AND'
        statement = 'WHERE %s%s\'%s\' %s %s%s\'%s\' ' % (
            colname.split(', ')[0], signs[sign[0]], colvalue.split(', ')[0], operator,
            colname.split(', ')[1], signs[sign[1]], colvalue.split(', ')[1])
        sql.i_store_filter_under_name(self.ctx, colname, ', '.join(sign), colvalue, name, operator)
        self.assertEquals(self.ctx.zato.user_ctx['filter'], statement)

    @patch('__builtin__.open')
    def test_i_insert_data_from_csv_file(self, open_mock):
        values = (util.rand_int(), util.rand_string(), util.rand_string())
        fake_csv = 'id, name, value\n%s, %s, %s' % values
        kwargs = {'filename': util.rand_string(),
                    'tablename': 'TestDB',
                    'conn_name': self.general_conn}

        open_mock.return_value = StringIO(fake_csv)
        sql.insert_csv(use_header=1, **kwargs)

        q = self.general_conn.execute('SELECT * FROM TestDB')
        result = q.fetchall()[1]
        self.assertEquals(result, values)

    @patch('__builtin__.open')
    def test_i_create_table_and_insert_data_from_csv_file(self, open_mock):
        values = (util.rand_string(), util.rand_string(), util.rand_string())
        fake_csv = '%s, %s, %s' % values
        kwargs = {'filename': util.rand_string(),
                    'tablename': util.rand_string(),
                    'conn_name': self.conn}

        open_mock.return_value = StringIO(fake_csv)
        sql.insert_csv(use_types='default', **kwargs)

        q = self.conn.execute('SELECT * FROM {tn}'.format(tn = kwargs['tablename']))
        result = q.fetchone()
        self.assertEquals(result, values)

    @patch('__builtin__.open')
    def test_i_create_table_and_insert_data_from_csv_file_using_types_and_header(self, open_mock):
        values = (util.rand_string(), util.rand_int(), util.rand_string())
        fake_csv = 'a-text, b:integer, c/varchar:30\n%s, %s, %s' % values
        kwargs = {'filename': util.rand_string(),
                    'tablename': util.rand_string(),
                    'conn_name': self.conn}

        open_mock.return_value = StringIO(fake_csv)
        sql.insert_csv(use_header=1, use_types=1, **kwargs)

        q = self.conn.execute('SELECT * FROM {tn}'.format(tn = kwargs['tablename']))
        result = q.fetchone()
        self.assertEquals(result, values)

    @patch('__builtin__.open')
    def test_i_create_table_and_insert_data_from_csv_file_using_header(self, open_mock):
        colnames = (tuple((element) for element in util.rand_string(5)))
        values = (util.rand_string(), util.rand_string(), util.rand_int(), round(util.rand_float(), 4), util.rand_string())
        t = colnames + values
        fake_csv = '%s, %s, %s, %s, %s\ntext, varchar:30, integer, float, char\n%s, %s, %s, %s, %s' % t
        kwargs = {'filename': util.rand_string(),
                    'tablename': util.rand_string(),
                    'conn_name': self.conn}

        open_mock.return_value = StringIO(fake_csv)
        sql.insert_csv(use_header=1, use_types=0, **kwargs)

        q = self.conn.execute('SELECT * FROM {tn}'.format(tn = kwargs['tablename']))
        result = q.fetchone()
        self.assertEquals(result, values)

    def tearDown(self):
        self.conn.close()
        os.remove(self.temp_db)
        sql.then_i_disconnect_from_sql(self.ctx, self.general_conn)

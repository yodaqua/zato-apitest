# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Filip Kłosowski <filip at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
from cassandra.cluster import Cluster
from StringIO import StringIO
from unittest import TestCase

# Bunch
from bunch import Bunch

# mock
from mock import patch

# pysandra-unit
import pysandraunit

# Zato
from zato.apitest import util
from zato.apitest.steps import cassandra_

# ###############################################################################################################################

class EmbeddedCassandraTestCase(TestCase):

    def __init__(self, methodName='runTest'):
        super(EmbeddedCassandraTestCase, self).__init__(methodName)
 
    def setUp(self):
        self.ctx = Bunch()
        self.ctx.zato = util.new_context(None, util.rand_string(), {})

        # setup initial Cassandra keyspace
        self.current_session_name = util.rand_string()
        self.columns = ['userid', 'fname', 'sname']
        self.values = util.rand_string(3)
        self.keyspace = util.rand_string()
        self.table = util.rand_string()
        data = (self.keyspace, self.table) + tuple(s for s in self.columns)
        keyspace_statement = (
            "CREATE KEYSPACE %s WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 }") % self.keyspace
        table_statement = ("CREATE TABLE %s.%s (%s text PRIMARY KEY, %s text, %s text)") % data

        self.embedded_cassandra = pysandraunit.PysandraUnit(native_transport_port=9042)
        self.embedded_cassandra.start()
        self.cluster = Cluster(protocol_version=1)
        self.session = self.cluster.connect()
        self.session.execute(keyspace_statement)
        self.session.execute(table_statement)
        self.cluster.shutdown()

        # setup Cassamdra ctx
        cassandra_.given_cassandra_contact_points(self.ctx, 'localhost')
        cassandra_.given_cassandra_protocol_version(self.ctx, 1)
        cassandra_.given_cassandra_port(self.ctx, '9042')
        cassandra_.given_i_connect_to_keyspace_as_session(self.ctx, self.keyspace, self.current_session_name)
 
    def tearDown(self):
        self.embedded_cassandra.stop()

class CassandraTestCase(EmbeddedCassandraTestCase):

    def test_given_i_connect_to_keyspace_as_conn_name(self):
        current_session = self.ctx.zato.user_ctx[self.current_session_name]
        self.assertEquals(type(current_session), type(self.session))

    def test_then_i_insert_values_into_columns_of_cassandra_table(self):
        current_session = self.ctx.zato.user_ctx[self.current_session_name]
        cassandra_.then_i_insert_values_into_columns_of_cassandra_table(
            self.ctx, self.table, ', '.join(self.values), ', '.join(self.columns), current_session)

        statement = "SELECT * FROM %s" % self.table
        cassandra_.given_i_store_cql_query_result_under_name(self.ctx, statement, 'cql_result', current_session)
        self.assertEquals(self.ctx.zato.user_ctx['cql_result'][0][0], self.values[0])
        self.assertEquals(self.ctx.zato.user_ctx['cql_result'][0][0:], tuple((item) for item in self.values))

    def test_then_i_update_columns_of_cassandra_table_setting_values(self):
        new_values = 'John, Doe'
        current_session = self.ctx.zato.user_ctx[self.current_session_name]
        criterion = "WHERE %s='%s'" % (self.columns[0], self.values[0])
        cassandra_.then_i_update_columns_of_cassandra_table_setting_values(
            self.ctx, self.table, ', '.join(self.columns[1:]), new_values, current_session, criterion)

        statement = "SELECT * FROM %s" % self.table
        cassandra_.given_i_store_cql_query_result_under_name(self.ctx, statement, 'cql_result', current_session)
        self.assertEquals(self.ctx.zato.user_ctx['cql_result'][0][0], self.values[0])
        self.assertEquals(self.ctx.zato.user_ctx['cql_result'][0][1], 'John')
        self.assertEquals(self.ctx.zato.user_ctx['cql_result'][0][2], 'Doe')

    def test_then_i_delete_from_cassandra_table(self):
        current_session = self.ctx.zato.user_ctx[self.current_session_name]
        criterion = "WHERE %s='%s'" % (self.columns[0], self.values[0])
        cassandra_.then_i_delete_from_cassandra_table(self.ctx, self.table, current_session, criterion)

        statement = "SELECT * FROM %s" % self.table
        cassandra_.given_i_store_cql_query_result_under_name(self.ctx, statement, 'cql_result', current_session)
        self.assertEquals(self.ctx.zato.user_ctx['cql_result'], [])

    @patch('__builtin__.open')
    def test_i_insert_data_from_csv_file_to_cassandra_table(self, open_mock):
        current_session = self.ctx.zato.user_ctx[self.current_session_name]
        values = (util.rand_string(), util.rand_string(), util.rand_string())
        fake_csv = 'userid, fname, sname\n%s, %s, %s' % values
        filename = util.rand_string()

        open_mock.return_value = StringIO(fake_csv)
        cassandra_.i_insert_data_from_csv_file_to_cassandra_table(self.ctx, filename, self.table, current_session)

        statement = "SELECT * FROM %s" % self.table
        cassandra_.given_i_store_cql_query_result_under_name(self.ctx, statement, 'cql_result', current_session)
        self.assertEquals(self.ctx.zato.user_ctx['cql_result'][0][0:], values)

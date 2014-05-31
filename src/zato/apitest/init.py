# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
import os

ENVIRONMENT = '''# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
import os

# Bunch
from bunch import Bunch

def before_feature(context, feature):
    context.zato = Bunch()
    context.zato.environment_dir = os.path.dirname(os.path.realpath(__file__))
    context.zato.request = Bunch()
    context.zato.request.headers = {}
    context.zato.request.ns_map = {}
    context.zato.request.date_formats = {}
'''

STEPS = '''# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# Zato
from zato.apitest import steps as default_steps
'''

BEHAVE_INI = """
[behave]
options=--format pretty --no-source --no-timings
"""

DEMO_FEATURE = """
Feature: zato.apitest demonstration

Scenario: *** REST JSON Demo ***

    Given address "http://localhost:17010"
    Given URL path "/demo/json"
    Given query string "?id=123"
    Given HTTP method "PUT"
    Given format "JSON"
    Given header "X-Custom-Header" "MyValue"
    Given request "demo.json"
    Given JSON Pointer "" in request is set to ""
    Given JSON Pointer "" in request is set to an integer ""
    Given JSON Pointer "" in request is set to a list ""
    Given JSON Pointer "" in request is set to a random string
    Given JSON Pointer "" in request is set to a random integer
    Given JSON Pointer "" in request is set to any of ""

    When the URL is invoked

    Then JSON Pointer "/action/message" is "OK, updated"
    And JSON Pointer "/action/code" is an integer "0"
    And JSON Pointer "/action/flow" is a list "Accepted, Done"
    And status is "200"
    And header "X-My-Header" is "Cool"
    And header "X-Another-Header" isn't "Foo"
    And header "X-Yet-Another-Header" contains "Baz"
    And header "X-Still-More" doesn't contain "Bar"
    And header "Connection" exists
    And header "X-Foo" doesn't exist
    And header "X-Should-Be-Empty" is empty
    And header "X-But-This-One-Should-Not" isn't empty

    # You can also compare responses directly inline ..
    And response is equal to "{"action":{"code":0, "msg":"Now, is that cool or is that cool?"}}"

    # .. or read them from disk.
    And response is equal to that from "demo.json"

Scenario: *** XML/SOAP Demo ***

    Given address "http://localhost:17010"
    Given URL path "/demo/xml"
    Given SOAP action "demo:xml"
    Given HTTP method "POST"
    Given format "XML"
    Given namespace prefix "demo" of "http://example.com/demo"
    Given request "demo.xml"
    Given XPath "//howdy" in request is set to "partner"
    Given XPath "//hello" in request is set to a random string
    Given XPath "//world" in request is set to a random integer
    Given XPath "//and-beyond" in request is set to one of "Arcturus, Ανδρομέδα, ほうおう座"

    When the URL is invoked

    Then XPath "//demo:action/demo:code" is an integer "0"
    And XPath "//demo:action/demo:msg" is "Now, is that cool or is that cool?"
""".encode('utf-8')

DEMO_JSON_REQ = """{"hello":"world"}"""
DEMO_JSON_RESP = """{"action":{"code":0, "msg":"Now, is that cool or is that cool?"}}"""

# No demo response for XML, we're not comparing them directly yet.
DEMO_XML_REQ = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Body>
      <howdy>Friend</howdy>
      <hello>Howdy</hello>
      <world>All good?</world>
      <and-beyond>Sweet</and-beyond>
   </soapenv:Body>
</soapenv:Envelope>"""

def handle(base_path):
    """ Sets up runtime directories and sample features.
    """
    # Top-level directory for tests
    features_dir = os.path.join(base_path, 'features')
    os.mkdir(features_dir)

    # Requests and responses
    request_json_dir = os.path.join(base_path, 'features', 'json', 'request')
    request_xml_dir = os.path.join(base_path, 'features', 'xml', 'request')

    response_json_dir = os.path.join(base_path, 'features', 'json', 'response')
    response_xml_dir = os.path.join(base_path, 'features', 'xml', 'response')

    os.makedirs(request_json_dir)
    os.makedirs(request_xml_dir)

    os.makedirs(response_json_dir)
    os.makedirs(response_xml_dir)

    # Demo feature
    open(os.path.join(features_dir, 'demo.feature'), 'w').write(DEMO_FEATURE)
    open(os.path.join(request_json_dir, 'demo.json'), 'w').write(DEMO_JSON_REQ)
    open(os.path.join(request_xml_dir, 'demo.xml'), 'w').write(DEMO_XML_REQ)
    open(os.path.join(response_json_dir, 'demo.json'), 'w').write(DEMO_JSON_RESP)

    # Add environment.py
    open(os.path.join(features_dir, 'environment.py'), 'w').write(ENVIRONMENT)

    # Add steps
    steps_dir = os.path.join(features_dir, 'steps')
    os.mkdir(steps_dir)
    open(os.path.join(steps_dir, 'steps.py'), 'w').write(STEPS)

    # User-provided CLI parameters, if any, passed to behave as they are
    config_dir = os.path.join(base_path, 'config')
    os.mkdir(config_dir)
    open(os.path.join(config_dir, 'behave.ini'), 'w').write(BEHAVE_INI)

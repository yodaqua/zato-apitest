zato-apitest - API Testing for Humans
=====================================

Introduction
------------

zato-apitest is a friendly command line tool for creating beautiful tests of HTTP-based REST, XML and SOAP APIs with as little
hassle as possible.

Tests are written in plain English, with no programming needed, and can be trivially extended in Python if need be.

Note that zato-apitest is meant to test APIs only. It's doesn't simulate a browser nor any sort of user interactions. It's meant
purely for machine-machine API testing.

Originally part of [Zato] (https://zato.io/docs/) - open-source ESB, SOA, REST, APIs and cloud integrations in Python.

In addition to HTTP Zato itself supports AMQP, ZeroMQ, WebSphere MQ, including JMS, Redis, FTP, OpenERP, SMTP, IMAP, SQL, Amazon S3,
OpenStack Swift and more so it's guaranteed zato-apitest will grow support for more protocols and transport layers with time.

Here's how a built-in demo test case looks like:

![zato-apitest demo run](https://raw.githubusercontent.com/zatosource/zato-apitest/master/docs/gfx/demo.png)

What it can do
--------------

- Invoke HTTP APIs

- Use [JSON Pointers] (https://zato.io/blog/posts/json-pointer-rfc-6901.html) or [XPath] (https://en.wikipedia.org/wiki/XPath)
  to set request's elements to strings, integers, floats, lists, random ones from a set of values, random strings, dates now/random/before/after/between.
  
- Check that JSON and XML elements, exist, don't exist,
  that an element is an integer, float, list, empty, non-empty, that it belongs to a list or doesn't.

- Set custom HTTP headers, user agent strings, method and SOAP action.

- Check that HTTP headers are or are not of expected value, that a header exists or not, contains a value or not, is empty or not,
  starts with a value or not and ends with a value or not.
  
- Read configuration from environment and config files.

- Store values extracted out of previous steps for use in subsequent steps, i.e. get a list of objects, pick ID of the first one
  and use this ID in later steps.
  
- Be integrated with JUnit

- Be very easily extended in Python

Download and install
--------------------

Newest releases are always available [on PyPI] (https://pypi.python.org/pypi/zato-apitest)
and can be installed with [pip] (https://pip.pypa.io/en/latest/installing.html).

```bash
$ sudo pip install zato-apitest
```

Run a demo test
---------------

Having installed the program, running ```apitest demo``` will set up a demo test case, run it against a live environment
and present the results, as on the screenshot in Introduction above.

Note that it may a good idea to check the demo closer, copy it over to a directory of your choice, and customize things to learn
by playing with an actual set of assertions.

Workflow
--------

1. Install zato-apitest
2. Initialize a test environment by running ```apitest init /path/to/an/empty/directory```
3. Update tests
4. Execute ```apitest run /path/to/tests/directory``` when you are done with updates
5. Jump to 3.

Tests and related resources
---------------------------

Let's dissect directories that were created after running ```apitest init```:

```
~/mytests
├── config
│   └── behave.ini
└── features
    ├── demo.feature
    ├── environment.py
    ├── json
    │   ├── request
    │   │   └── demo.json
    │   └── response
    │       └── demo.json
    ├── steps
    │   └── steps.py
    └── xml
        ├── request
        │   └── demo.xml
        └── response
```


 Path                              | Description
---------------------------------- | ----------------------------------------------------------------------------------------------------------------------
```./config/behave.ini```          | Low-level configuration that is passed to the underlying [behave] (https://pypi.python.org/pypi/behave) library as-is.
```./features/demo.feature```      | A set of tests for a single feature under consideration.
```./features/environment.py```    | Place to keep hooks invoked throughout a test case's life-cycle in.
```./features/json/request/*```    | JSON requests, if any, needed as input to APIs under tests.
```./features/json/response/*```   | JSON responses you expect for APIs to produce, used for smart comparison.
```./features/steps/steps.py```    | Custom assertions go here.
```./features/xml/request/*```     | XML requests (including SOAP), if any, needed as input to APIs under tests.
```./features/xml/response/*```    | *(Currently not used, future versions will allow for comparing XML/SOAP responses directly)*

Each set of related tests concerned with a particular feature is kept in its own *.feature file in /features.

For instance, if you test an API allowing one to create and update customers, you could have the following files:

```
└── features
    ├── cust-create.feature
    └── cust-update.feature
```

How you structure the tests is completely up to you as long as individual files end in *.feature.

Anatomy of a test
-----------------

Here's how a sample test kept in ```./features/cust-update.feature``` may look like. For comparison, it shows both SOAP and REST
assertions. This is the literal copy of a test, everything is in plain English:

```
Feature: Customer update

Scenario: SOAP customer update

    Given address "http://example.com"
    Given URL path "/xml/customer"
    Given SOAP action "update:cust"
    Given HTTP method "POST"
    Given format "XML"
    Given namespace prefix "cust" of "http://example.com/cust"
    Given request "cust-update.xml"
    Given XPath "//cust:name" in request is "Maria"
    Given XPath "//cust:last-seen" in request is a random date before "2015-03-17" "default"

    When the URL is invoked

    Then XPath "//cust:action/cust:code" is an integer "0"
    And XPath "//cust:action/cust:msg" is "Ok, updated"

    And context is cleaned up

Scenario: REST customer update

    Given address "http://example.com"
    Given URL path "/json/customer"
    Given query string "?id=123"
    Given HTTP method "PUT"
    Given format "JSON"
    Given header "X-Node" "server-test-19"
    Given request "cust-update.json"
    Given JSON Pointer "/name" in request is "Maria"
    Given JSON Pointer "/last-seen" in request is UTC now "default"

    When the URL is invoked

    Then JSON Pointer "/action/code" is an integer "0"
    And JSON Pointer "/action/message" is "Ok, updated"
    And status is "200"
    And header "X-My-Header" is "Cool"
```

- Each test begins with a ```Feature: ``` preamble which denotes what is being tested
- A test may have multiple scenarios - here one scenario has been created for each SOAP and REST
- Each scenario has 3 parts, corresponding to building a request, invoking an URL and running assertions on a response received:

  - One or more ```Given``` steps
  - Exactly one ```When``` step
  - One or more ```Then/And``` steps. There is no difference between how ```Then``` and ```And``` work, simply the first
    assertion is called ```Then``` and the rest of them is ```And```. Any assertion may come first.

- In both ```Given``` and ```Then/And``` the order of steps is always honored.

- Steps work by matching patterns that can be potentially parametrized between double quotation marks,
  for instance ```Given address "http://example.com"``` is an invocation of a ```Given address "{address}"``` pattern.


Available steps
---------------

<div style="font-size:10px">

Section | Part    | Pattern                                   | Notes                                                                                                                                                           | Details
--------|---------|-------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------
HTTP    | Given   | ```address "{address}"```                 | An address of the API to invoke                                                         | [Details] ()
HTTP    | Given   | ```URL path "{url_path}"```               | URL path to invoke
HTTP    | Given   | ```HTTP method "{method}"```              | HTTP method to use for invoking
HTTP    | Given   | ```format "{format}"```                   | Either 'JSON' or 'XML'
HTTP    | Given   | ```user agent is "{value}"```             | User-Agent string to use
HTTP    | Given   | ```header "{header}" "{value}"```         | Arbitrary HTTP header to provide to the API
HTTP    | Given   | ```request "{request_path}"```            | Name of a file the request is kept in.Depending on format, either ```./features/json/request``` or ```./features/xml/request``` will be prepended automatically.
HTTP    | Given   | ```request is "{data}"```                 | Request to use, inlined.
HTTP    | Given   | ```query string "{query_string}"```       | Query string parameters in format of ?a=1&b=2, including the question mark
Common  | Given   | ```date format "{name}" "{format}"```     | Stores a date format ```format``` under a label ```name``` for use in later assertions
Common  | Given   | ```I store "{value}" under "{name}"```    | Stores an arbitrary ```value``` under a ```name``` for use in later assertions

</div>


Where to keep configuration
---------------------------

Linking tests to form complex scenarios
---------------------------------------

Extending zato-apitest and adding custom assertions
---------------------------------------------------

License
-------
[LGPLv3] (./LICENSE.txt) - zato-apitest is free to use in open-source and proprietary programs.

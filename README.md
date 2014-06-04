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

All the default steps are listed below. You're also encouraged to [browse the usage examples] (./docs/steps).

Section | Part    | Pattern                                                                                                     | Notes                                                                                                                                                            | Details
--------|---------|-------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------
HTTP    | Given   | ```address "{address}"```                                                                                   | An address of the API to invoke                                                                                                                                  | [Details] ()
HTTP    | Given   | ```URL path "{url_path}"```                                                                                 | URL path to invoke                                                                                                                                               |
HTTP    | Given   | ```HTTP method "{method}"```                                                                                | HTTP method to use for invoking                                                                                                                                  |
HTTP    | Given   | ```format "{format}"```                                                                                     | Either 'JSON' or 'XML'                                                                                                                                           |
HTTP    | Given   | ```user agent is "{value}"```                                                                               | User-Agent string to use                                                                                                                                         |
HTTP    | Given   | ```header "{header}" "{value}"```                                                                           | Arbitrary HTTP header to provide to the API                                                                                                                      |
HTTP    | Given   | ```request "{request_path}"```                                                                              | Name of a file the request is kept in. Depending on format, either ```./features/json/request``` or ```./features/xml/request``` will be prepended automatically.|
HTTP    | Given   | ```request is "{data}"```                                                                                   | Request to use, inlined.|
HTTP    | Given   | ```query string "{query_string}"```                                                                         | Query string parameters in format of ?a=1&b=2, including the question mark|
Common  | Given   | ```date format "{name}" "{format}"```                                                                       | Stores a date format ```format``` under a label ```name``` for use in later assertions|
Common  | Given   | ```I store "{value}" under "{name}"```                                                                      | Stores an arbitrary ```value``` under a ```name``` for use in later assertions|
JSON    | Given   | ```JSON Pointer "{path}" in request is "{value}"```                                                         | Sets ```path``` to a string ```value``` in the request |
JSON    | Given   | ```JSON Pointer "{path}" in request is an integer "{value}"```                                              | Sets ```path``` to an integer ```value``` in the request |
JSON    | Given   | ```JSON Pointer "{path}" in request is a float "{value}"```                                                 | Sets ```path``` to a float ```value``` in the request |
JSON    | Given   | ```JSON Pointer "{path}" in request is a list "{value}"```                                                  | Sets ```path``` to a list ```value``` in the request|
JSON    | Given   | ```JSON Pointer "{path}" in request is a random string```                                                   | Sets ```path``` to a randomly generated string in the request |
JSON    | Given   | ```JSON Pointer "{path}" in request is a random float```                                                    | Sets ```path``` to a randomly generated float in the request |
JSON    | Given   | ```JSON Pointer "{path}" in request is a random integer```                                                  | Sets ```path``` to a randomly generated integer in the request |
JSON    | Given   | ```JSON Pointer "{path}" in request is one of "{value}"```                                                  | Sets ```path``` to a randomly chosen string out of ```value``` in the request |
JSON    | Given   | ```JSON Pointer "{path}" in request is a random date "{format}"```                                          | Sets ```path``` to a randomly generated date using format ```format``` |
JSON    | Given   | ```JSON Pointer "{path}" in request is now "{format}"```                                                    | Sets ```path``` to now in local timezone, using format ```format```|
JSON    | Given   | ```JSON Pointer "{path}" in request is UTC now "{format}"```                                                | Sets ```path``` to now in UTC, using format ```format```|
JSON    | Given   | ```JSON Pointer "{path}" in request is a random date after "{date_start}" "{format}"```                     | Sets ```path``` to a randomly generated date after ```date_start```, using format ```format``` |
JSON    | Given   | ```JSON Pointer "{path}" in request is a random date before "{date_end}" "{format}"```                      | Sets ```path``` to a randomly generated date before ```date_before```, using format ```format```  |
JSON    | Given   | ```JSON Pointer "{path}" in request is a random date between "{date_start}" and "{date_end}" "{format}"```  | Sets ```path``` to a randomly generated date between ```date_start``` and ```date_end```, using format ```format``` |
XML     | Given   | ```namespace prefix "{prefix}" of "{namespace}"```                                                          | For the duration of the test, stores ```prefix``` of a ```namespace``` to be used in XPath expressions|
XML     | Given   | ```SOAP action "{value}"```                                                                                 | Sets a request's SOAPaction header, if needed|
XML     | Given   | ```XPath "{xpath}" in request is "{value}"```                                                               | Sets ```xpath``` to a string ```value``` in the request |
XML     | Given   | ```XPath "{xpath}" in request is a random string```                                                         | Sets ```xpath``` to a randomly generated string in the request|
XML     | Given   | ```XPath "{xpath}" in request is a random integer```                                                        | Sets ```xpath``` to a randomly generated integer in the request|
XML     | Given   | ```XPath "{xpath}" in request is a random float```                                                          | Sets ```xpath``` to a randomly generated float in the request|
XML     | Given   | ```XPath "{xpath}" in request is a random date "{format}"```                                                | Sets ```xpath``` to a randomly generated date using format ```format```|
XML     | Given   | ```XPath "{xpath}" in request is now "{format}"```                                                          | Sets ```xpath``` to now in local timezone, using format ```format```|
XML     | Given   | ```XPath "{xpath}" in request is UTC now "{format}"```                                                      | Sets ```xpath``` to now in UTC, using format ```format``` |
XML     | Given   | ```XPath "{xpath}" in request is a random date after "{date_start}" "{format}"```                           | Sets ```xpath``` to a randomly generated date after ```date_start```, using format ```format```|
XML     | Given   | ```XPath "{xpath}" in request is a random date before "{date_end}" "{format}"```                            | Sets ```xpath``` to a randomly generated date before ```date_before```, using format ```format``` |
XML     | Given   | ```XPath "{xpath}" in request is a random date between "{date_start}" and "{date_end}" "{format}"```        | Sets ```xpath``` to a randomly generated date between ```date_start``` and ```date_end```, using format ```format```|
XML     | Given   | ```XPath "{xpath}" in request is one of "{value}"```                                                        | Sets ```xpath``` to a randomly chosen string out of ```value``` in the request|
HTTP    | When    | ```the URL is invoked```                                                                                    | Invokes the HTTP-based API under test|
HTTP    | Then    | ```status is "{status}"```                                                                                  | Asserts that the HTTP status code in response is ```status```|
HTTP    | Then    | ```header "{header}" is "{value}"```                                                                        | Asserts that a ```header``` exists and has value ```value``` |
HTTP    | Then    | ```header "{header}" isn't "{value}"```                                                                     | Asserts that a ```header``` exists and doesn't have value ```value``` |
HTTP    | Then    | ```header "{header}" contains "{value}"```                                                                  | Asserts that a ```header``` exists and contains substring ```value``` |
HTTP    | Then    | ```header "{header}" doesn\'t contain "{value}"```                                                          | Asserts that a ```header``` exists and doesn't contain substring ```value``` |
HTTP    | Then    | ```header "{header}" exists```                                                                              | Asserts that a ```header``` exists, regardless of its value|
HTTP    | Then    | ```header "{header}" doesn't exist```                                                                       | Asserts that a ```header``` doesn't exist|
HTTP    | Then    | ```header "{header}" is empty```                                                                            | Asserts that a ```header``` exists and is an empty string|
HTTP    | Then    | ```header "{header}" isn't empty```                                                                         | Asserts that a ```header``` exists and is any non-empty string|
HTTP    | Then    | ```header "{header}" starts with {value}```                                                                 | Asserts that a ```header``` exists and starts with substring ```value```|
HTTP    | Then    | ```header "{header}" doesn't start with  {value}```                                                         | Asserts that a ```header``` exists and doesn't start with substring ```value```|
HTTP    | Then    | ```header "{header}" ends with {value}```                                                                   | Asserts that a ```header``` exists and ends with substring ```value```|
HTTP    | Then    | ```header "{header}" doesn\'t end with {value}```                                                           | Asserts that a ```header``` exists and doesn't end with substring ```value```|
Common  | Then    | ```I store "{path}" from response under "{name}"```                                                         | Stores value of ``path``` from response under a label ```name``` for use in subsequent steps|
Common  | Then    | ```I store "{path}" from response under "{name}", default "{default}"```                                    | As above, but uses ```default``` if ```path``` is not found in the response|
Common  | Then    | ```context is cleaned up```                                                                                 | Cleans up request context configured through ```When``` steps.|
JSON    | Then    | ```response is equal to that from "{path}"```                                                               | Asserts that response received is equal to the one from ```path```. Note that ```./features/json/response``` will be prepended automatically. |
JSON    | Then    | ```response is equal to "{expected}"```                                                                     | Asserts that response received is equal to the one provided inline|
JSON    | Then    | ```JSON Pointer "{path}" is "{value}"```                                                                    | Asserts that a value under ```path``` is a string ```value``` |
JSON    | Then    | ```JSON Pointer "{path}" is an integer "{value}"```                                                         | Asserts that a value under ```path``` is an integer ```value```|
JSON    | Then    | ```JSON Pointer "{path}" is a float "{value}"```                                                            | Asserts that a value under ```path``` is a float ```value```|
JSON    | Then    | ```JSON Pointer "{path}" is a list "{value}"```                                                             | Asserts that a value under ```path``` is a list ```value```|
JSON    | Then    | ```JSON Pointer "{path}" is empty```                                                                        | Asserts that a value under ```path``` is an empty string|
JSON    | Then    | ```JSON Pointer "{path}" isn't empty```                                                                     | Asserts that a value under ```path``` is any non-empty string|
JSON    | Then    | ```JSON Pointer "{path}" is one of "{value}"```                                                             | Asserts that a value under ```path``` is a string element from list ```value```|
JSON    | Then    | ```JSON Pointer "{path}" isn't one of "{value}"```                                                          | Asserts that a value under ```path``` is not in a list provided in ```value```|
XML     | Then    | ```XPath "{xpath}" is "{value}"```                                                                          | Asserts that a value under ```path``` is a string ```value```|
XML     | Then    | ```XPath "{xpath}" is an integer "{value}"```                                                               | Asserts that a value under ```path``` is an integer ```value```|
XML     | Then    | ```XPath "{xpath}" is a float "{value}"```                                                                  | Asserts that a value under ```path``` is a float ```value```|
XML     | Then    | ```XPath "{xpath}" is empty```                                                                              | Asserts that a value under ```path``` is an empty string|
XML     | Then    | ```XPath "{xpath}" isn't empty```                                                                           | Asserts that a value under ```path``` is any non-empty string|
XML     | Then    | ```XPath "{xpath}" is one of "{value}"```                                                                   | Asserts that a value under ```path``` is a string element from list ```value```|
XML     | Then    | ```XPath "{xpath}" isn't one of "{value}"```                                                                | Asserts that a value under ```path``` is not in a list provided in ```value```|

Where to keep configuration
---------------------------

Linking tests to form complex scenarios
---------------------------------------

Extending zato-apitest and adding custom assertions
---------------------------------------------------

License
-------
[LGPLv3] (./LICENSE.txt) - zato-apitest is free to use in open-source and proprietary programs.

zato.apitest - API Testing for Humans
=====================================

Intro
-----

zato.apitest is a friendly command line tool for creating beautiful tests of HTTP-based REST, XML and SOAP APIs with as little
hassle as possible.

Tests are written in plain English, with no programming needed, and can be trivially extended in Python if need be.

Here's how a built-in demo test case looks like:

![zato.apitest demo run](https://raw.githubusercontent.com/zatosource/zato-apitest/master/docs/gfx/demo.png)

What it can do
--------------

Download and install
--------------------

Run a demo test
---------------

Having installed the program, running ```apitest demo``` will set up a demo test case, run it against a live environment
and present the results, as in the screenshot above.

Note that it may a good idea to check the demo closer, copy it over to a directory of your choice, and customize things to learn
by playing with an actual set of assertions.

Workflow
--------

1. Install zato.apitest
2. Initialize a test environment by running ```apitest init /path/to/an/empty/directory```
3. Update tests
4. Run ```apitest run /path/to/tests/directory``` when you are done with updates
5. Jump to 3.

Anatomy of a test
-----------------

Let's dissect directories that were created after running ```apitest init```

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


Available assertions
--------------------

Where to keep configuration
---------------------------

Linking tests to form complex scenarios
---------------------------------------

Extending zato.apitest and adding custom assertions
---------------------------------------------------

License
-------
[LGPLv3] (./LICENSE.txt) - zato.apitest is free to use in open-source and proprietary programs.


Given I store "{value}" under "{name}"
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Given I store "{value}" under "{name}"

    Given address "http://apitest-demo.zato.io"
    Given HTTP method "POST"
    Given URL path "/demo/json"
    Given I store "MyValue" under "name"

    When the URL is invoked

    Then JSON Pointer "/foo" is "#name"
```

Discussion
----------

Values stored under user-provided names can be referred to by prefixing them with a '#' sign.
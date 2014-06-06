
Given I store "{value}" under "{name}"
=============================================================================================================

Usage example
-------------

```
Feature: zato-apitest docs

Scenario: Given I store "{value}" under "{name}"

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/json"
    Given I store "MyValue" under "name"

    When the URL is invoked

    Then JSON Pointer "/foo" is "#name"
```

Discussion
----------

Values stored under user-provided names can be referred to by prefixing them with a '#' sign.

Given JSON Pointer "{path}" in request is one of "{value}"
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Given JSON Pointer "{path}" in request is one of "{value}"

    Given address "http://apitest-demo.zato.io"
    Given HTTP method "POST"
    Given URL path "/demo/json"
    Given JSON Pointer "/a" in request is one of "aa,bb,cc,dd"

    When the URL is invoked

    Then status is "200"
```

Discussion
----------

(None)
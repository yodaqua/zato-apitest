
Given JSON Pointer "{path}" in request is a random float
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Given JSON Pointer "{path}" in request is a random float

    Given address "http://apitest-demo.zato.io"
    Given HTTP method "POST"
    Given URL path "/demo/json"
    Given JSON Pointer "/a" in request is a random float

    When the URL is invoked

    Then status is "200"
```

Discussion
----------

(None)

Then JSON Pointer "{path}" is empty
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Then JSON Pointer "{path}" is empty

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/json"
    Given format "JSON"

    When the URL is invoked

    Then JSON Pointer "/action/code-empty" is empty
```

Discussion
----------

(None)
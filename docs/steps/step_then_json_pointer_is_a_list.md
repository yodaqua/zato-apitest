
Then JSON Pointer "{path}" is a list "{value}"
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Then JSON Pointer "{path}" is a list "{value}"

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/json"
    Given format "JSON"

    When the URL is invoked

    Then JSON Pointer "/action/list" is a list "q,w,e,r,t,y"
```

Discussion
----------

(None)
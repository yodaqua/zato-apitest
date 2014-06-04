
Given header "{header}" "{value}"
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Given format "{format}"

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/json"
    Given format "JSON"
    Given header "X-My-Header" "MyValue"

    When the URL is invoked

    Then status is "200"
```

Discussion
----------

(None)
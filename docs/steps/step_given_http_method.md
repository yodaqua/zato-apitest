
Given HTTP method "{method}"
=============================================================================================================

Usage example
-------------

```
Feature: zato-apitest docs

Scenario: Given HTTP method "{method}"

    Given address "http://apitest-demo.zato.io"
    Given HTTP method "POST"
    Given URL path "/demo/json"
    Given format "JSON"

    When the URL is invoked

    Then status is "200"
```

Discussion
----------

GET is used if not method is specified but it can be provided explicitly as well.
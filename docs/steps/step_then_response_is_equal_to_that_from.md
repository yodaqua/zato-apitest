
Then response is equal to that from "{path}"
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Then response is equal to that from "{path}"

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/json2"
    Given format "JSON"

    When the URL is invoked

    Then response is equal to "response-file.json"
```

Discussion
----------

(None)
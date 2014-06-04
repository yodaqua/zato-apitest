
Then header "{header}" is "{value}"
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Then header "{header}" is "{value}"

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/json"
    Given format "JSON"

    When the URL is invoked

    Then header "Connection" is "keep-alive"
```

Discussion
----------

(None)
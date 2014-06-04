
Then header "{header}" doesn't contain "{value}"
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Then header "{header}" doesn't contain "{value}"

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/json"
    Given format "JSON"

    When the URL is invoked

    Then header "Server" doesn't contain "IIS 3.0"
```

Discussion
----------

(None)
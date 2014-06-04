
Then header "{header}" starts with {value}
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Then header "{header}" starts with {value}

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/json"
    Given format "JSON"

    When the URL is invoked

    Then header "Connection" starts with "keep-"
```

Discussion
----------

(None)
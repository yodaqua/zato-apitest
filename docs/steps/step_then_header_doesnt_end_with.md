
Then header "{header}" doesn't end with {value}
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Then header "{header}" doesn't end with {value}

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/json"
    Given format "JSON"

    When the URL is invoked

    Then header "Content-Type" doesn't end with "soap"
```

Discussion
----------

(None)

Then header "{header}" doesn't start with {value}
=============================================================================================================

Usage example
-------------

```
Feature: zato-apitest docs

Scenario: Then header "{header}" doesn't start with {value}

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/json"
    Given format "JSON"

    When the URL is invoked

    Then header "Server" doesn't start with "WAS"
```

Discussion
----------

(None)
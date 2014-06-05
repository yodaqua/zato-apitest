
Then header "{header}" contains "{value}"
=============================================================================================================

Usage example
-------------

```
Feature: zato-apitest docs

Scenario: Then header "{header}" contains "{value}"

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/json"
    Given format "JSON"

    When the URL is invoked

    Then header "Accept-Ranges:" contains "bytes"
```

Discussion
----------

(None)
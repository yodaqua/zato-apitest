
Given SOAP action "{value}"
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Given SOAP action "{value}"

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/XML"
    Given format "XML"
    Given SOAP action "my:soap:action"

    When the URL is invoked

    Then status is "200"
```

Discussion
----------

(None)
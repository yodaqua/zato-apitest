
Given XPath "{xpath}" in request is "{value}"
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Given XPath "{xpath}" in request is "{value}"

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/XML"
    Given HTTP method "POST"
    Given format "XML"
    Given request "demo.xml"
    Given XPath "//howdy" in request is "partner"

    When the URL is invoked

    Then status is "200"
```

Discussion
----------

(None)
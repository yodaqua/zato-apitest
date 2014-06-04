
Given XPath "{xpath}" in request is now "{format}"
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Given XPath "{xpath}" in request is now "{format}"

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/XML"
    Given HTTP method "POST"
    Given format "XML"
    Given request "demo.xml"
    Given XPath "//howdy" in request is now "default"

    When the URL is invoked

    Then status is "200"
```

Discussion
----------

The format "default" is always available. Its value is "YYYY-MM-DDTHH:mm:ss".

Given XPath "{xpath}" in request is a random string
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Given XPath "{xpath}" in request is a random string

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/xml"
    Given HTTP method "POST"
    Given format "XML"
    Given request is "<req><howdy>foo</howdy></req>"
    Given XPath "//howdy" in request is a random string

    When the URL is invoked

    Then status is "200"
```

Discussion
----------

(None)
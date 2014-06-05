
Then XPath "{xpath}" is empty
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Then XPath "{xpath}" is empty

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/xml"
    Given HTTP method "POST"
    Given format "XML"
    Given request is "<req><howdy>foo</howdy></req>"

    When the URL is invoked

    Then XPath "//empty" is empty
```

Discussion
----------

(None)
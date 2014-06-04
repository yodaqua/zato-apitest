
Then XPath "{xpath}" is an integer "{value}
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Then XPath "{xpath}" is an integer "{value}

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/xml"
    Given HTTP method "POST"
    Given format "XML"
    Given request is "<req><howdy>foo</howdy></req>"

    When the URL is invoked

    Then XPath "//code" is an integer "0"
```

Discussion
----------

(None)

Given request is "{data}"
=============================================================================================================

Usage example
-------------

```
Feature: zatoapi-test docs

Scenario: Given request is "{data}"

    Given address "http://apitest-demo.zato.io"
    Given HTTP method "POST"
    Given URL path "/demo/json"
    Given format "JSON"
    Given request is "{"hi":"there"}"

    When the URL is invoked

    Then status is "200"
```

Discussion
----------

Specifies a JSON request inline. Use [Given request "{request_path}"] (./step_given_request.md) to make use of requests stored in 
dedicated files.
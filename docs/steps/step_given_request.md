
Given request "{request_path}"
=============================================================================================================

Usage example
-------------

```
Feature: zato-apitest docs

Scenario: Given request "{request_path}"

    Given address "http://apitest-demo.zato.io"
    Given HTTP method "POST"
    Given URL path "/demo/json"
    Given format "JSON"
    Given request "my-request.json"

    When the URL is invoked

    Then status is "200"
```

Discussion
----------

Specifies the path to a request, relative to the ./features/json/request directory.
Use [Given request is "{data}"] (step_given_request_is.md) to provide a request inline.
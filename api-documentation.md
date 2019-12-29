---
description: >-
  Confirm a user is a world_bank employee and create the user in the
  application.
---

# Confirm User emails

{% api-method method="get" host="https://carpoolingbackend.herokuapp.com/v1/apis/user\_auth/?apiKey={api\_key}&email={email}" path="" %}
{% api-method-summary %}
apis/v1/user\_auth/
{% endapi-method-summary %}

{% api-method-description %}
This endpoint allows you to confirm a user email from the WB database and also registers the user on the application.
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-headers %}
{% api-method-parameter name="Authentication" type="string" required=true %}
Authentication token to track down who sent the request.
{% endapi-method-parameter %}
{% endapi-method-headers %}

{% api-method-query-parameters %}
{% api-method-parameter name="apiKey" type="string" required=true %}
An API key to authenticate the user.
{% endapi-method-parameter %}

{% api-method-parameter name="email" type="string" required=true %}
The email to be used to login the user.
{% endapi-method-parameter %}
{% endapi-method-query-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
User exists on the WB database..and return the user object
{% endapi-method-response-example-description %}

```
  {
    "first_name": "Vick",
    "last_name": "Waichigo",
    "username": "vick",
    "phone_number": "0700000000",
    "email": "waichigovick@gmail.com"
  }
```
{% endapi-method-response-example %}

{% api-method-response-example httpCode=404 %}
{% api-method-response-example-description %}
Could not find a user with the email provided
{% endapi-method-response-example-description %}

```
[]



```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

> #### `User_auth example.`

![](.gitbook/assets/user_auth.png)

{% hint style="info" %}
Note you have to provide an authentication token on the headers for the request to be successful.
{% endhint %}

{% hint style="success" %}
A new user should now be registered of the request `status_code` is `200,` and a user object should be returned as the response.
{% endhint %}


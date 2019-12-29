---
description: Log in a user on the car pooling application
---

# Login a user

{% api-method method="post" host="https://carpoolingbackend.herokuapp.com/v1/apis/" path="auth/login/" %}
{% api-method-summary %}
/apis/v1/auth/login/
{% endapi-method-summary %}

{% api-method-description %}
This endpoint allows you to login users on the application.
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-body-parameters %}
{% api-method-parameter name="username" type="string" required=true %}
the username that the user was registered with. 
{% endapi-method-parameter %}

{% api-method-parameter name="password" type="string" required=true %}
the password key sent to the users email.
{% endapi-method-parameter %}
{% endapi-method-body-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}

{% endapi-method-response-example-description %}

```
{
  "key": "297023hn329cc55f04564fac377856396e9a505fa"
}
```
{% endapi-method-response-example %}

{% api-method-response-example httpCode=400 %}
{% api-method-response-example-description %}

{% endapi-method-response-example-description %}

```
{
"message" : "Bad request."
}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

#### `user login example`

![auth/login endpoint](../.gitbook/assets/login.png)

{% hint style="info" %}
A dictionary like the one below must be provided to the body of the POST request to log in a user.
{% endhint %}

```text
{
	"username":"vick",
	"password":" soRjJbZi"
}
```




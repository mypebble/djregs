djregs
======

djregs is a Django app designed to make your life easy when signing up new
users. This library provides:

* Models to handle the registration
* Views/forms to manage the sign-up process
* Email address activation

djregs supports Django 1.5 and 1.6. Django 1.4 is not supported.


How to Use
==========

Add the `registration` package to your `INSTALLED_APPS` and set
`AUTH_USER_MODEL` if it is not `auth.User`.

```python
INSTALLED_APPS = (
    ...
    'registration',
)

AUTH_USER_MODEL = 'main.MyUserProfile'
```

See the documentation for `django-registration` for more detailed usage.


Relationship to django-registration
===================================

This is a full fork of the django-registration app originally built by James
Bennett. This app uses the `registration` namespace, so cannot co-exist.

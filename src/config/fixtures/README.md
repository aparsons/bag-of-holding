### user_data.json
This file contains a user account for testing and development.

Load the user with the following command:
```
python manage.py loaddata config/fixtures/user_data.json
```

- Username: **dev**
- Password: **dev**

_Don't use this in production. Use the [createsuperuser](https://docs.djangoproject.com/en/1.9/ref/django-admin/#createsuperuser) command instead._

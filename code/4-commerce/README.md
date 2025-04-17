# Commerce Project

### To create a new project:
`django-admin startproject PROJECT_NAME`

### To create an app for the project:
`python manage.py startapp APP_NAME`

### Add app to settings.py
add 'APP_NAME', to `INSTALLED_APPS` list

### Add a route for the app in urls.py
import include:
`from django.urls import include, path`
add the route:
`path("app_name/", include("app_name.urls")),`

### Create the models in models.py
Create the model classes

### Make the migrations
`python manage.py makemigrations`
`python manage.py makemigrations your_app_name --empty --name migration_name`

### Apply the migrations
`python manage.py migrate`

### Add a urls.py file in the new app folder
```python
from django.urls import path

from . import views

urlpatters = [
]
```

### Create the admin account
`python manage.py createsuperuser`

### Add models to admin.py
```python
from .models import model

admin.site.register(model)
```

### Visit the admin interface
`127.0.0.1:8000/admin/`


### To enter the django shell
`python manage.py shell`

### To run the server:
python manage.py runserver
